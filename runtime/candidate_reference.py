"""Runtime-fitted numerical research candidates; no weights, labels, text or network."""
import json
import os
import time

import numpy as np
import pandas as pd
from qfbench2_track_forecasting import cli as reference
from qfbench2_track_forecasting.targets import log_return_steps


def features(history, lag=5):
    h = np.asarray(history)
    return np.r_[h[-lag:].ravel(), h[-20:].mean(0), h[-20:].std(0),
                 h[-5:].mean(0)].astype(np.float32)


def block_paths(residual, draws, steps, rng, block):
    """One block start per draw shared by all assets and successive horizons."""
    residual = np.asarray(residual, float)
    if len(residual) < block:
        raise ValueError('insufficient joint residual history')
    parts = []
    for _ in range((steps + block - 1) // block):
        starts = rng.integers(0, len(residual) - block + 1, size=draws)
        parts.append(residual[starts[:, None] + np.arange(block)])
    return np.concatenate(parts, axis=1)[:, :steps]


def fit_predict(z, length, method, config, monthly, audit):
    """Fit only supplied prefix, produce a joint matrix of deterministic step centres."""
    n, assets = z.shape
    if method in ('B2a', 'B2b'):
        from statsforecast.models import AutoTheta, AutoARIMA
        paths = []
        for ai in range(assets):
            model = (AutoTheta(season_length=config.get('monthly_season', 1) if monthly else 1,
                               decomposition_type='additive') if method == 'B2a'
                     else AutoARIMA(seasonal=False, season_length=1, max_p=config['order'],
                                    max_q=config['order'], start_p=1, start_q=1,
                                    max_order=4, nmodels=12, approximation=False))
            model.fit(np.asarray(z[:, ai], dtype=np.float64))
            paths.append(model.predict(h=length)['mean'])
            audit['fit_calls'] += 1
            audit['predict_calls'] += 1
        return np.column_stack(paths)
    lag = config.get('lag', 5)
    if n < max(40, lag + 25):
        raise ValueError('insufficient regression prefix')
    if method == 'B3':
        mean, sd = z.mean(0), np.maximum(z.std(0), 1e-8)
        scaled = (z - mean) / sd
        x = np.array([scaled[i-lag:i].ravel() for i in range(lag, n)])
        y = scaled[lag:]
        x = np.column_stack([np.ones(len(x)), x])
        penalty = np.eye(x.shape[1]) * config['alpha']; penalty[0, 0] = 0
        coef = np.linalg.solve(x.T @ x + penalty, x.T @ y)
        # Recursive VAR stability belongs to the training prefix, never the holdout.
        for _ in range(40):
            companion = np.zeros((lag * assets, lag * assets))
            companion[:assets] = np.hstack([coef[1:].reshape(lag, assets, assets)[j].T
                                           for j in range(lag-1, -1, -1)])
            if lag > 1: companion[assets:, :-assets] = np.eye((lag-1)*assets)
            radius = float(np.max(np.abs(np.linalg.eigvals(companion))))
            if radius <= .98: break
            coef[1:] *= .9
        if radius > .98: raise ValueError('unstable VAR after shrinkage')
        audit.setdefault('spectral_radii', []).append(radius)
        history = scaled.tolist(); predicted = []
        for _ in range(length):
            v = np.r_[1., np.array(history[-lag:]).ravel()] @ coef
            history.append(v.tolist()); predicted.append(v * sd + mean)
        audit['fit_calls'] += 1; audit['predict_calls'] += 1
        return np.array(predicted)
    if method != 'B4': raise ValueError('unknown candidate')
    import xgboost as xgb
    allowed = {'GPU-ff6cada3-c329-a5dd-5bd4-153c4e1e0509',
               'GPU-0a4b0d1b-db13-6b7c-4502-13994f4c93da',
               'GPU-2b69b76f-1ab2-99ba-a4d2-4c66c9b77774',
               'GPU-303410c4-3bf8-2e24-1a71-0ed6593bf685'}
    device = os.environ.get('T2_XGB_DEVICE', 'cuda')
    if device == 'cuda' and os.environ.get('CUDA_VISIBLE_DEVICES') not in allowed:
        raise ValueError('B4 requires exactly one audited allowed GPU UUID')
    x = np.array([features(z[:i]) for i in range(20, n)])
    y = z[20:]
    dm = xgb.DMatrix(x, label=y)
    model = xgb.train({'device':device, 'tree_method':'hist', 'max_depth':config['depth'],
                       'eta':.05, 'lambda':10, 'seed':1, 'nthread':1,
                       'objective':'reg:squarederror'}, dm, num_boost_round=config['rounds'])
    actual = json.loads(model.save_config())['learner']['generic_param']['device']
    if device == 'cuda' and not actual.startswith('cuda'):
        raise RuntimeError('CUDA request silently fell back to '+actual)
    audit.setdefault('xgboost_devices', []).append(actual)
    audit['xgboost_version'] = xgb.__version__
    audit['cuda_build'] = xgb.build_info().get('USE_CUDA')
    audit['gpu_uuid'] = os.environ.get('CUDA_VISIBLE_DEVICES') if device == 'cuda' else None
    history = z.tolist(); predicted = []
    for _ in range(length):
        v = np.asarray(model.predict(xgb.DMatrix(features(history)[None]))).reshape(assets)
        history.append(v.tolist()); predicted.append(v)
    audit['fit_calls'] += 1; audit['predict_calls'] += length
    return np.array(predicted)


def predict(panels, assets, horizons, asof, draws, seed, target, panel_steps, method, config):
    rng = np.random.default_rng(seed)
    monthly = panel_steps is not None
    hist = {a: reference._series(panels, a, asof) for a in assets}
    audit = {'method':method, 'config':config, 'fit_calls':0, 'predict_calls':0,
             'native_success':True, 'fallback':False, 'seed':seed}
    if monthly:
        hist = {a:reference._monthly_series(s) for a, s in hist.items()}
    anchors = [str(s.index[-1]) for s in hist.values()]
    if len(set(anchors)) != 1:
        raise ValueError('candidate requires common observation anchors; reference fallback')
    steps = pd.DataFrame({a: pd.Series(log_return_steps(s), index=s.index) if target == 'log_return'
                          else s.diff().where(np.r_[False, np.diff(s.index.asi8) == 1]) if monthly
                          else reference._diff_without_gaps(s) for a, s in hist.items()}).dropna()
    if len(steps) < 60: raise ValueError('candidate needs 60 joint historical steps')
    if method in ('B2a','B2b','B3','B4') and str(steps.index[-1]) != anchors[0]:
        raise ValueError('latest anchor follows a withheld-history gap; reference fallback')
    cap = 120 if monthly else 504
    steps = steps.iloc[-cap:]
    delta = steps.to_numpy(float)
    endpoint = np.asarray(panel_steps, int) if monthly else np.tile(horizons, (len(assets), 1))
    max_steps = int(endpoint.max())
    if max_steps > 512: raise ValueError('candidate horizon exceeds bounded path budget')
    anchor = np.zeros(len(assets)) if target == 'log_return' else np.array([s.iloc[-1] for s in hist.values()])
    audit.update(history_rows=len(delta), history_end=anchors[0], panel_steps=endpoint.tolist())
    if method in ('B1g', 'B1b'):
        half = config['half_life_monthly' if monthly else 'half_life_daily']
        w = np.exp2(-np.arange(len(delta)-1, -1, -1) / half); w /= w.sum()
        mean = w @ delta if target == 'log_return' else np.zeros(len(assets))
        centered = delta - w @ delta
        cov = (centered * w[:, None]).T @ centered / (1 - w @ w)
        shrink = config['shrinkage']
        cov = (1-shrink)*cov + shrink*np.diag(np.diag(cov))
        vals, vecs = np.linalg.eigh(cov)
        factor = vecs @ np.diag(np.sqrt(np.maximum(vals, 1e-12)))
        if method == 'B1g':
            innovation = rng.standard_normal((draws, max_steps, len(assets))) @ factor.T
        else:
            # Whiten and recolour synchronous residual blocks to the recent shrunken covariance.
            old = np.cov(centered, rowvar=False); old = np.atleast_2d(old)
            v, q = np.linalg.eigh(old)
            white = centered @ q @ np.diag(1/np.sqrt(np.maximum(v, 1e-12)))
            innovation = block_paths(white, draws, max_steps, rng, 3 if monthly else 5) @ factor.T
        paths = anchor + np.cumsum(mean + innovation, axis=1)
    else:
        # Forecast centres for levels; per-step log returns for factor targets.
        if not monthly:
            dates = pd.to_datetime(steps.index)
            if np.max(np.diff(dates).astype('timedelta64[D]').astype(int)) > 10:
                raise ValueError('discontinuous history; reference gap-aware fallback')
        z = delta if target == 'log_return' or method in ('B3','B4') else pd.DataFrame(hist).loc[steps.index].to_numpy(float)
        tail = 24 if monthly else 64
        if len(z)-tail < 40: raise ValueError('insufficient prefix for time-out calibration')
        prior = fit_predict(z[:-tail], tail, method, config, monthly, audit)
        if target == 'level' and method in ('B2a','B2b'):
            error = z[-tail:] - prior
            residual = np.diff(np.vstack([np.zeros((1, len(assets))), error]), axis=0)
            centre = fit_predict(z, max_steps, method, config, monthly, audit)
            noise = np.cumsum(block_paths(residual-residual.mean(0), draws, max_steps, rng, 3 if monthly else 5), axis=1)
            paths = centre[None] + noise
        else:
            residual = z[-tail:] - prior
            centre = fit_predict(z, max_steps, method, config, monthly, audit)
            innovation = block_paths(residual-residual.mean(0), draws, max_steps, rng, 3 if monthly else 5)
            paths = anchor + np.cumsum(centre[None] + innovation, axis=1)
        audit['calibration_rows'] = tail
        audit['calibration_fit_end'] = str(steps.index[-tail-1])
    out = np.stack([paths[:, endpoint[ai]-1, ai] for ai in range(len(assets))], axis=1)
    if out.shape != (draws, len(assets), len(horizons)) or not np.isfinite(out).all():
        raise ValueError('invalid candidate joint samples')
    return out, audit


def run(args, card, forwarded):
    began = time.monotonic()
    reference.main(forwarded)  # Exact schema and explicit safe R0 fallback are already implemented.
    meta_path = args.out.parent/'forecast_meta.json'
    meta = json.loads(meta_path.read_text())
    config = json.loads(os.environ.get('T2_CANDIDATE_CONFIG', '{}'))
    if not config:
        from pathlib import Path
        from joint_v2 import METHODS, config_for
        if args.method in METHODS: config = config_for(args.method,args.asof)
        else:
            configs = json.loads((Path(__file__).resolve().parents[1]/'experiments/baseline_v1/configs.json').read_text())
            config = configs[args.method][0]
    panels = reference._read_panels(args.panels)
    import pathlib
    card_path = pathlib.Path(forwarded[forwarded.index('--card')+1])
    steps = reference._monthly_inputs(panels, card, card_path, args.asof)
    try:
        from joint_v2 import METHODS, predict as joint_predict
        predict_fn = joint_predict if args.method in METHODS else predict
        samples, audit = predict_fn(panels, meta['asset_ids'], meta['horizons'], args.asof,
                                meta['n_draws'], args.seed, meta['target'], steps, args.method, config)
        n, a, h = samples.shape
        pd.DataFrame({'draw':np.repeat(np.arange(n), a*h),
                      'asset':np.tile(np.repeat(meta['asset_ids'], h), n),
                      'horizon':np.tile(meta['horizons'], n*a),
                      'value':samples.ravel()}).to_parquet(args.out, index=False)
        meta['rationale']['method'] = args.method+' runtime fit; joint paths; no text'
        meta_path.write_text(json.dumps(meta, indent=2)+'\n')
    except Exception as exc:
        audit = {'method':args.method, 'config':config, 'native_success':False,
                 'fallback':True, 'fallback_reason':type(exc).__name__+': '+str(exc)[:500]}
    audit['seconds'] = time.monotonic()-began
    text = '# Numerical research candidate '+args.method+'\n\n'
    text += ('Native joint-path forecast. All fitting, transformations and time-out residual '
             'calibration use the supplied cutoff prefix. No text read, no House call.\n\n'
             if audit['native_success'] else 'Candidate refused this input; unchanged official numeric R0 fallback.\n\n')
    text += 'Audit:\n```json\n'+json.dumps(audit, indent=2)+'\n```\n'
    if not audit['native_success']:
        text += '\n'+(args.out.parent/'forecast_rationale.md').read_text()
    (args.out.parent/'forecast_rationale.md').write_text(text)
    print('T2_CANDIDATE_META='+json.dumps(audit))
    return 0
