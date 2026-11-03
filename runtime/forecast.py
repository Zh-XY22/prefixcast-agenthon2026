"""QuantPrefixEW40V3 explicit-date level/log-return tree entry. Three files only."""
import argparse,json,os,pathlib,tomllib
import numpy as np,pandas as pd
from qfbench2_track_forecasting import cli as ref
from quant_axis import Axis,state,suffix
from quant_features import feature,base
import candidate_reference as b4
HERE=pathlib.Path(__file__).resolve().parent
def predict(frame,c,asof,seed,spec):
    t=c['targets'];assets=t['asset_ids'];hs=t['horizons'];panel=c.get('metadata',{}).get('asset_panel');target=t['target_type'];freq=t.get('target_frequency',c.get('metadata',{}).get('target_frequency','daily'))
    if freq!='daily' or panel not in ['rates_daily','g10_fx_daily'] or max(hs)>4:raise ValueError('outside registered 1–4 daily market scope')
    # Official factor/simple-return input semantics; no automatic log of yields.
    kind='simple_return' if target=='log_return' else 'level'
    target_dates=t.get('target_dates',spec.get('targets',{}).get('target_dates'));axis=Axis.build(asof,hs,target_dates=target_dates);steps=axis.offsets()
    if max(steps)>4:raise ValueError('explicit target dates exceed registered four-day support')
    series={a:ref._series(frame,a,asof) for a in assets};wide=pd.DataFrame({a:pd.Series(s.to_numpy(),index=pd.to_datetime(s.index)) for a,s in series.items()}).sort_index()[assets];wide=suffix(wide,asof,101);v,offset=state(wide.to_numpy(float),target=target,input_kind=kind)
    draws=base(v,steps,seed)
    if offset is not None:draws-=offset[None,:,None]
    return draws,dict(native=True,actual_model='CurrentTaskEW40Joint',target=target,input_kind=kind,
        target_dates=list(axis.target_dates),path_steps=steps,calendar_source=axis.calendar_source,
        continuous_rows=len(v),history_start=str(wide.index[0].date()),history_end=str(wide.index[-1].date()),
        covariance_half_life=40,correlation_shrinkage=.1,center='zero innovation',
        offline_artifact_loaded=False,fitted_artifacts=False,selection='fixed numerical code; no per-task model selection',
        information_source='current task input only; no outside historical vintage asserted')

def main(argv=None):
    import sys
    argv=list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0]=='forecast':argv=argv[1:]
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--panels',type=pathlib.Path,required=True);p.add_argument('--text',type=pathlib.Path,required=True);p.add_argument('--asof',required=True);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--seed',type=int,default=int(os.environ.get('QFBENCH_SEED','1')));a=p.parse_args(argv)
    card=next(x for x in [a.panels/'card.toml',a.panels.parent/'card.toml'] if x.is_file());c=tomllib.loads(card.read_text());specfile=next((x for x in [a.panels/'forecast_spec.json',a.panels.parent/'forecast_spec.json'] if x.is_file()),None);spec=json.loads(specfile.read_text()) if specfile else {};t=c['targets'];assets=t['asset_ids'];hs=t['horizons'];frame=ref._read_panels(a.panels);reason='';status='native'
    if pd.Timestamp(a.asof)>pd.Timestamp(c['provenance']['data_cutoff']):raise ValueError('asof exceeds task data cutoff')
    try:x,audit=predict(frame,c,a.asof,a.seed,spec)
    except Exception as e:
        reason=type(e).__name__+': '+str(e);status='numeric_fallback';monthly=t.get('target_frequency',c.get('metadata',{}).get('target_frequency'))=='monthly';ep=ref._monthly_inputs(frame,c,card,a.asof) if monthly else None
        try:
            os.environ['T2_XGB_DEVICE']='cpu';x,audit=b4.predict(frame,assets,hs,a.asof,500,a.seed,t['target_type'],ep,'B4',{'depth':2,'rounds':32,'lag':5});audit['fallback_method']='B4_CPU original'
        except Exception as e2:
            x,audit=ref._draw(frame,assets,hs,a.asof,500,a.seed,target_type=t['target_type'],panel_steps=ep);audit['fallback_method']='R0 official gap-aware';reason+='; B4: '+type(e2).__name__
    assert x.shape==(500,len(assets),len(hs)) and np.isfinite(x).all();a.out.parent.mkdir(parents=True,exist_ok=True);n,na,nh=x.shape
    pd.DataFrame(dict(draw=np.repeat(np.arange(n),na*nh).astype('int32'),asset=pd.Series(np.tile(np.repeat(assets,nh),n),dtype='string'),horizon=np.tile(hs,n*na).astype('int32'),value=x.ravel().astype('float64'))).to_parquet(a.out,index=False)
    method='QuantPrefixEW40V3';meta=dict(unit_id=c['task']['id'],asof=a.asof,representation='samples',asset_ids=assets,horizons=hs,n_draws=500,target=t['target_type'],rationale=dict(file='forecast_rationale.md',method=method+': '+status+'; '+audit.get('actual_model',audit.get('fallback_method',''))));(a.out.parent/'forecast_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
    rationale='# QuantPrefixEW40V3\n\n500 joint scenarios, seed='+str(a.seed)+'. Current task input only. Native: zero-innovation Gaussian paths, EW40 covariance and 10% diagonal shrinkage; no learned weights, offline calibration, endpoint, text, or cross-task state. Native daily rates/FX horizons 1-4 only. Level remains additive, including negative yields; simple return input becomes cumulative log1p paths. Unsupported/insufficient inputs use original task-local CPU B4 or official R0; monthly uses official publication-lag handling. Numerical fallback is not native success.\n\n'+json.dumps(dict(status=status,reason=reason,audit=audit),indent=2)+'\n' ;(a.out.parent/'forecast_rationale.md').write_text(rationale)
    print('RELEASE_META='+json.dumps(dict(method=method,status=status,reason=reason,audit=audit)),flush=True)
if __name__=='__main__':main()
