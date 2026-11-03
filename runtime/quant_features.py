"""Current-prefix financial features; dynamic assets, no future or task ID."""
import numpy as np
from scipy.linalg import eigh
TENORS={'UST_1M':1/12,'UST_2M':2/12,'UST_3M':.25,'UST_6M':.5,'UST_1Y':1,'UST_2Y':2,'UST_3Y':3,'UST_5Y':5,'UST_7Y':7,'UST_10Y':10,'UST_20Y':20,'UST_30Y':30}
def feature(values, hs, panel, assets, target='level', structure=False):
    d=np.diff(values,axis=0)[-300:];n,a=d.shape
    if n<60 or not np.isfinite(d).all():raise ValueError('insufficient complete history')
    w=np.exp2(-np.arange(n-1,-1,-1)/40);w/=w.sum();z=d-w@d
    C=(z*w[:,None]).T@z/(1-w@w);C=.9*C+.1*np.diag(np.diag(C));sd=np.sqrt(np.maximum(C.diagonal(),1e-12));corr=C/np.outer(sd,sd)
    f=np.stack([np.log(np.maximum(np.mean(d[-k:]**2,axis=0)/sd**2,.01)) for k in [5,20,80]]+
        [np.clip(d[-1]/sd,-8,8),np.clip(d[-5:].mean(0)/sd,-5,5),np.clip(d[-20:].mean(0)/sd,-5,5),np.mean(corr,axis=1),np.ones(a)*(panel=='rates_daily'),np.ones(a)*np.mean(np.abs(d[-5:]/sd)),np.ones(a)],axis=-1)
    f=np.repeat(f[:,None,:],len(hs),axis=1);f[:,:,-1]=np.asarray(hs)[None]/4
    if structure:
        tenor=np.array([TENORS.get(x,0.) for x in assets]);known=tenor>0
        # Symmetric asset-set statistics: order invariant; descriptive par curve only.
        level=float(np.mean(values[-1,known])) if known.any() else 0.
        slope=curvature=0.
        if known.sum()>=3:
            order=np.argsort(tenor[known]);v=values[-1,known][order];slope=float(v[-1]-v[0]);curvature=float(v[len(v)//2]-(v[0]+v[-1])/2)
        extra=np.stack([np.log1p(tenor),np.full(a,level),np.full(a,slope),np.full(a,curvature),np.full(a,target=='log_return')],axis=1)
        f=np.concatenate([f,np.repeat(extra[:,None],len(hs),axis=1)],axis=-1)
    return f.reshape(a*len(hs),-1),np.repeat(values[-1],len(hs)),(sd[:,None]*np.sqrt(hs)).ravel(),C

def base(values,hs,seed=1,draws=500):
    _,anchor,scale,C=feature(values,hs,'',list(range(values.shape[1])))
    v,q=eigh(C);L=q@np.diag(np.sqrt(np.maximum(v,1e-12)))
    rng=np.random.default_rng(seed);innov=rng.standard_normal((draws,max(hs),values.shape[1]))@L.T
    paths=values[-1]+np.cumsum(innov,axis=1)
    return paths[:,np.asarray(hs)-1].transpose(0,2,1)
