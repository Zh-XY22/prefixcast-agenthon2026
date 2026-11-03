# Archived evaluation notes

This narrative is retained from the initial public release for provenance. It includes earlier experiments and internal labels; it is not the active description of the final method. See [current evaluation](../docs/EVALUATION.md). Relative links were adjusted after relocation.

# Evaluation: official Final result versus public historical experiments

## Official result, checked2026-11-03

[Agenthon official Final leaderboard](https://www.agenthon.net/#leaderboard): T2 Forecasting, HaHaHa, **2nd**, displayed **−0.9513**, higher-is-better. The owner confirms the actual submitted ZIP SHA256 in [FINAL_VERSION](../docs/FINAL_VERSION.md). A platform receipt/submission ID remains absent from the archive. Do not compare the negative rounded leaderboard display directly with the positive local M0 proxy means below.

## New source checks, without accuracy labels

Fresh pinned Python3.12.15 environment: one public EW40 case and one public B4 case passed G0–G3,500draws/threefiles, exits0, UID65534. B4 actually fitted twice on its task history. No realized labels or performance scores were produced. This is not a Docker rebuild result: the actual build attempt failed because no daemon was reachable. See [release checks](../docs/RELEASE_CHECKS.md).

## Historical evidence reused unchanged

Six existing host contracts: four native EW40, two numerical B4 fallback, exits0, official G0–G3 PASS. Two strict-runtime cases cover native EW40 and B4 and PASS. All these had no realized labels: they are compatibility checks, not predictive performance. gVisor NOT_TESTED; Development-like settings are not complete Final runtime certification. Public evidence/ACCEPTANCE_SUMMARY.json is a newly generated sanitized summary with raw-source hashes, not an original report.

Historical104 route audit: 0EW40 native,99B4,5R0 because original horizons start beyond this native1–4 range. It demonstrates fallback compatibility, not EW40 accuracy. No104 task was rerun in this export.

The fixed12-case evaluation produced36 valid predictions (12×candidate/B4/R0), with initial R0 extra-verb failures preserved and subsequently repaired. Seven tasks have legitimate reconstructed labels from already-observed public task history; five remain unscorable. Four scored original-horizon cases: candidate=B4 (bitwise fallback), means .6425739790 vs R0 .8609968596. Three scored short proxies: candidate1.0572471091, B4 1.1296258800, R0 1.6163108784. These are separate cohorts, not a pooled seven-task leaderboard. The three short cards contain only two distinct dates and two EUR targets share a path. Small selected retrospective cases cannot prove broad superiority. One short UST case was unscorable for missing exact target labels; no shifted targets or fake labels were inserted.

Raw CRPS/variogram/tail components came from locked official functions; reported composite is separately input-derived local M0 proxy normalization, not sealed official denominators or an official ranked score. The independent previous audit found21 scored rows matched existing official raw results and numerical proxy replay within2.22e-16; this export reuses that record and computes only arithmetic over existing metrics, no scoring functions. Raw cross-unit scales must not be mixed.

Prior EWMA40=1.214445, B4=1.265962, v5CPU=1.205895, EW/Toto=1.204957 etc refer to600 seen development cards/300 dates under their own versions. v5/v6 prefit CatBoost models are not bundled here. Paper-analysis outside this public directory preserves protocol-specific baselines, failures, approximate controls and caveats. The final programme has no offline neural/pretrained artifacts and no House/text effect claim. The official public Final leaderboard now independently lists HaHaHa at rank2, displayed score−0.9513; this is not one of these proxy experiments. No archived per-submission receipt or official per-task breakdown was recovered. Earlier user-reported2.6/2.9 remain unverified historical aggregates. No new significance/bootstrap was performed.
