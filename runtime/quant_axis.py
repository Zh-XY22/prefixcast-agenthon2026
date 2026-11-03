"""Shared date/target contract. No observed-row compression or imputed labels."""
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class Axis:
    asof: str
    horizons: tuple
    target_dates: tuple
    calendar_source: str

    @classmethod
    def build(cls, asof, horizons, *, target_dates=None, frequency='daily', observation_periods=None):
        hs=tuple(map(int,horizons))
        if not hs or min(hs)<1 or len(set(hs))!=len(hs): raise ValueError('invalid horizons')
        if frequency=='monthly':
            if observation_periods is None: raise ValueError('monthly requires official observation_periods resolver')
            dates=tuple(str(pd.Period(x,freq='M')) for x in observation_periods)
            if len(dates)!=len(hs):raise ValueError('observation_periods mismatch')
            return cls(str(asof),hs,dates,'official observation_periods; publication lag resolved by caller')
        if target_dates is None:
            dates=tuple(str((pd.Timestamp(asof)+pd.offsets.BDay(h)).date()) for h in hs)
            source='explicit weekday proxy / official business-day convention; no inferred source holidays'
        else:
            dates=tuple(str(pd.Timestamp(d).date()) for d in target_dates)
            source='explicit contract target_dates'
        if len(dates)!=len(hs) or any(d<=str(asof)[:10] for d in dates):raise ValueError('invalid target dates')
        return cls(str(asof)[:10],hs,dates,source)

    def offsets(self):
        dates=pd.DatetimeIndex(self.target_dates)
        if any(d.dayofweek>=5 for d in dates):raise ValueError('non-weekday target requires explicit supported calendar')
        if any(dates[i]>=dates[i+1] for i in range(len(dates)-1)) and list(self.horizons)==sorted(self.horizons):
            raise ValueError('target dates conflict with ascending daily horizons')
        # Official daily grid uses the authored trading-day horizon. Explicit dates
        # locate labels; weekday distance can include market holidays and is not a walk step.
        return list(self.horizons)

    def labels(self, frame, *, target='level', input_kind='level'):
        """Require the actual calendar cells, including every intermediate return."""
        f=frame.copy();f.index=pd.to_datetime(f.index)
        if target=='level':out=f.reindex(pd.to_datetime(self.target_dates)).to_numpy(float).T
        elif target=='log_return':
            anchor=f.reindex([pd.Timestamp(self.asof)]).to_numpy(float)[0]
            if input_kind=='level':
                future=f.reindex(pd.to_datetime(self.target_dates)).to_numpy(float)
                if np.any(anchor<=0) or np.any(future<=0):raise ValueError('log level requires positive prices, not interest yields')
                out=np.log(future/anchor).T
            elif input_kind=='simple_return':
                dates=pd.bdate_range(pd.Timestamp(self.asof)+pd.offsets.BDay(1),max(self.target_dates))
                values=f.reindex(dates).to_numpy(float)
                if np.any(values<=-1):raise ValueError('invalid simple return')
                cum=np.cumsum(np.log1p(values),axis=0)
                out=cum[dates.get_indexer(pd.to_datetime(self.target_dates))].T
            else:raise ValueError('unknown input kind')
        else:raise ValueError('unsupported target')
        if not np.isfinite(out).all():raise ValueError('missing actual target/intermediate return; no label fill')
        return out

def state(values, *, target='level', input_kind='level'):
    values=np.asarray(values,float)
    if not np.isfinite(values).all():raise ValueError('state requires valid continuous suffix or native mask')
    if target=='level':return values,None
    if target!='log_return':raise ValueError('unsupported target')
    if input_kind=='simple_return':
        if np.any(values<=-1):raise ValueError('invalid simple return')
        z=np.cumsum(np.log1p(values),axis=0)
    elif input_kind=='level':
        if np.any(values<=0):raise ValueError('log price requires positive FX, not negative yields')
        z=np.log(values)
    else:raise ValueError('unknown input kind')
    return z,z[-1].copy()

def suffix(frame, asof, minimum=101):
    f=frame.loc[:asof].sort_index()
    if f.index.has_duplicates:raise ValueError('duplicate dates')
    bad=~np.isfinite(f.to_numpy(float)).all(axis=1)
    gap=np.r_[False,np.diff(f.index.to_numpy()).astype('timedelta64[D]').astype(int)>5]
    cuts=np.flatnonzero(bad|gap);start=int(cuts[-1]+bool(bad[cuts[-1]])) if len(cuts) else 0
    f=f.iloc[start:].tail(601)
    if len(f)<minimum or str(f.index[-1].date())!=str(asof)[:10]:raise ValueError('short/unaligned continuous suffix')
    return f

def selftest():
    idx=pd.bdate_range('2020-01-01',periods=12);p=pd.DataFrame({'FX':np.exp(np.arange(12)*.01)},index=idx)
    r=p.pct_change();a=Axis.build(str(idx[5].date()),[1,4],target_dates=[idx[6],idx[9]])
    assert np.allclose(a.labels(p,target='log_return'),a.labels(r,target='log_return',input_kind='simple_return'))
    missing=p.drop(idx[6])
    try:a.labels(missing)
    except ValueError:pass
    else:raise AssertionError('missing target silently compressed')
    holidays=Axis.build(str(idx[5].date()),[1],target_dates=[idx[7]])
    assert holidays.offsets()==[1]
    s,last=state(r.iloc[1:6],target='log_return',input_kind='simple_return');assert np.allclose(np.diff(s,axis=0),np.log1p(r.iloc[2:6]))
    assert state(np.array([[-.1],[.01]]))[1] is None
    print('AXIS_LEVEL_LOG_RETURN_MISSING_EXPLICIT_DATE_PASS')
if __name__=='__main__':selftest()
