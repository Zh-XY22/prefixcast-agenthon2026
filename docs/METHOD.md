# PrefixCast method

PrefixCast is one forecasting program with automatic routing. Its public component names describe the algorithms; historical labels are retained in the frozen code and output logs for submission traceability.

| Public component name | Label in the original implementation | Meaning |
|---|---|---|
| Exponentially weighted joint paths | `EW40`, `CurrentTaskEW40Joint` | Exponentially weighted covariance with a half-life of 40 historical increments. The number is a weighting parameter, not an experiment count or a 40-row window. |
| Autoregressive trees with residual block sampling | `B4`, `B4_CPU original` | An internal candidate label for the XGBoost-based numerical route; it is not a standard algorithm name or a user-facing version. |
| Official statistical fallback | `R0` | The bundled official statistical reference forecaster, used if the tree route fails. |
| Complete submitted system | `QuantPrefixEW40V3` | The preserved original submission/runtime identifier; the public method name is PrefixCast. |

The entry point tries joint paths on supported tasks, then the tree component if that attempt cannot run, and finally the official statistical fallback if the tree component fails. There is no command-line model selector. The public examples vary the input, not the implementation.

All 131 runtime source/resource files remain byte-identical to the verified export of the submitted image. This document describes that final runtime.

## Inputs, targets and entry

`runtime/forecast` sets PYTHONPATH to its directory plus `official/` and invokes `forecast.py`. Inside the submitted image it selects `/opt/numeric-runtime/bin/python` (Python3.12.15); otherwise set `T2_PYTHON`. `forecast.py:main` accepts the formal verb optionally, requires `--panels --text --asof --out`, locates card.toml/forecast_spec.json beside or inside panels, and reads Parquet via the vendored official `_read_panels`. It rejects `asof > provenance.data_cutoff` before numerical routing. No network, text parsing, retrieval, House endpoint or model server is called. `--text` is required interface input but unused.

Only supplied task history is used. Output is 500 complete joint samples `[N,A,H]`, flattened asset-major then horizon into `draw:int32, asset:string, horizon:int32, value:float64`. Metadata and rationale identify actual native/fallback route. `forecast.parquet`, `forecast_meta.json`, `forecast_rationale.md` are the only deliverables; stdout `RELEASE_META` is a controller log, not a fourth file. N is fixed500, not increased by ensemble tricks.

## Routing and time semantics

`forecast.py:predict`: native only when frequency is daily, metadata.asset_panel is `rates_daily` or `g10_fx_daily`, authored max(horizons)<=4, and `Axis.offsets()` support<=4. EM panel name `em_fx_ecb_daily` is outside this explicit whitelist and routes to the tree component. Assets/horizon counts are dynamic. The joint-path component is therefore used only within this scope; other tasks are routed automatically.

`quant_axis.py:Axis.build/offsets` preserves authored daily h for walk indices. Declared target_dates identify contract dates, not a reason to count the h-th nonmissing observation. Without declared dates it uses pandas BDay weekdays and explicitly does not infer source holiday calendars. A weekend/invalid explicit target causes refusal; it does not shift labels. This is a support limitation, not an exchange-calendar guarantee.

`quant_axis.py:suffix`: align supplied assets by date, sort, reject duplicates, cut after last nonfinite joint row or date gap>5 calendar days, keep<=601 rows, require>=101 rows and the last row exactly asof. There is no backfill or joining withheld-history segments. `_series` selects only dates<=asof. Any native exception is logged before numerical fallback.

## Exponentially weighted joint paths

`quant_axis.py:state` leaves level data additive, including negative yields. For target log_return the entry explicitly selects `input_kind='simple_return'`: requires values>-1 and forms cumulative log1p state; it subtracts the final historical cumulative state from output. It does NOT automatically detect FX price levels. Although Axis helper has a log-price branch, this entry does not select it. Contract semantics must therefore agree with this assumption; existing derived FX return tests supplied matching transformed input. Do not describe all price-level log-return contracts as proven supported.

`quant_features.py:base -> feature`: from selected state X use the last at most300 differences d. Weight recent innovations by w_i proportional to 2^{-(n-1-i)/40}, normalized to sum1. Let m=sum_i w_i*d_i. Estimate:

    C = sum_i w_i (d_i-m)(d_i-m)' / (1-sum_i w_i^2)
    C_shrunk = 0.9*C + 0.1*diag(diag(C)).

Demeaning estimates covariance; it is NOT a forecast drift. scipy.linalg.eigh gives eigenvectors Q and values lambda, with lambda floored at1e-12; L=Q diag(sqrt(max(lambda,1e-12))). No canonical eigenvector sign correction is applied in this final implementation. With numpy.default_rng(seed), independent normal arrays `[500,max(h),A]` are multiplied by L'. Form one shared multistep path per draw `X_last+cumsum(innovation)`; select indices h-1 and transpose to `[500,A,H]`. Thus assets and horizons share path innovations, while draws are independent. Centre is zero change, not empirical m. No pretrained parameter, offline calibration or estimated lookup table is loaded.

The ten-column feature helper also computes lag/volatility summaries, but base only consumes its covariance. `TENORS` and `structure=True` features are unused by this entry; there are no event/curve features hidden behind the name.

## Autoregressive trees with residual block sampling

`forecast.py:main` catches native exceptions and forces `T2_XGB_DEVICE=cpu`, then calls `candidate_reference.predict(...,'B4',{'depth':2,'rounds':32,'lag':5})`. `candidate_reference.run` and other candidate families in that historical module are NOT called; no external configs.json/joint_v2 is read on this path. These dormant branches are preserved byte-for-byte for provenance, not advertised as enabled models.

History is resolved using official `_series`, monthly resolver and gap-aware differences; simple returns convert through official log_return_steps for cumulative log_return targets. Common anchors and>=60 joint steps are required. Cap120 monthly steps or504 daily. Refuse h path>512 and daily gaps>10 days; refuse a withheld-history gap after the latest realized differences. This component regresses innovation vectors z, not levels.

Feature at each training point is flattened previous5 innovation vectors plus last20 means, last20 standard deviations, last5 means. `fit_predict` requires adequate regression history and uses float32 features, XGBoost hist, CPU, depth2, 32 rounds, eta0.05, lambda10, squared-error objective, training seed1 and nthread1. Recursively predict each future innovation using its preceding predicted history. The caller's sampling seed controls residual resampling; it does not replace XGBoost's fixed training seed1.

Hold out final64 daily or24 monthly innovations: first fit before that tail, recursively predict the tail, compute synchronized multiasset residuals, subtract the residual sample mean; second fit uses the full current prefix. `block_paths` draws common start indices across all assets, block length5 daily/3 monthly, concatenates blocks across future steps. Add the recursive innovation centres and block residuals, accumulate from current level anchor (zero for cumulative returns), and select each cell's resolved endpoint. This is runtime two-fit residual calibration, not prepacked learned weights. The original finite residual-block behavior is preserved: mean-centred residual rows do not force every finite sampled block/path to have zero realised drift. No post-submission correction to this sampling behavior has been applied.

## Official statistical fallback

Any exception from the tree component is recorded and calls vendored `cli._draw`. It uses gap-aware complete historical innovations, requires>=30 rows, empirical std/correlation with a PSD nudge. Daily level centre is the last observation, return centre is empirical drift*h; each daily requested h gets a new joint asset-normal draw scaled sqrt(h), so its cross-horizon structure differs from the joint-path component. Monthly mode uses the official `_monthly_inputs`/horizons.py observation_periods and publication-lag resolver, shared monthly walk and original authored output h keys. It does not divide calendar-day h by21. Invalid monthly metadata is not fabricated; unresolved input errors can still exit nonzero. Fallback success is not native success, and no failure label is rewritten.

## Determinism, fit boundary, limitations

Default seed1, overridden by QFBENCH_SEED or --seed. Joint-path covariance, tree features, fitting and residual calibration use current input only; no cross-task state, late learned checkpoint or other task labels. No daily return/level unit rescaling is inferred beyond the specified transforms. Different BLAS/eigensolver backends may flip eigenvector signs and change finite seeded draws without changing covariance; do not promise cross-platform bitwise prediction equality. Dates/vintage assertions do not certify all historical data revisions were available then. Scope refusals, insufficient aligned history and numerical exceptions are observable in rationale/RELEASE_META. Output shape/finiteness is asserted; errors after fallback are not hidden.

The official Final result and current source-check scope are documented in [evaluation](EVALUATION.md). Earlier development comparisons remain in the [provenance archive](../provenance/README.md); they are not additional configurations of this released program.
