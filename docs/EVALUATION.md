# Results and validation

## Official competition result

| Competition | Track | Team | Final rank | Displayed score |
|---|---|---|---|---|
| Agenthon 2026 | Track 2 — Forecasting | HaHaHa | 2nd | −0.9513 |

Source: [official Final leaderboard](https://www.agenthon.net/#leaderboard), checked 2026-11-03. The displayed score is rounded to four decimal places and higher is better. This is the result of the final submitted system as a whole; no component-level contribution is inferred.

The submitted ZIP and image identifiers are recorded in [final version](FINAL_VERSION.md). The ZIP identity is owner-confirmed and matches the archived file; a per-submission platform receipt/ID has not been archived.

## Source execution checks

The final program was run in a fresh Linux/Python 3.12.15 environment after installing the exact pinned dependencies.

| Official public input | Actual component | Draws | Output files | Official output gates |
|---|---|---:|---:|---|
| US Treasury yield, 2019-01-07, horizons 2/3 | Exponentially weighted joint paths | 500 | 3 | G0–G3 PASS |
| Korean won, 2017-03-27, horizons 1/4 | Autoregressive trees with residual block sampling | 500 | 3 | G0–G3 PASS |

The tree case performed its two required fits on the current task history. No realized labels or new accuracy scores were used. These checks establish execution and output compatibility for those cases, not an independent reproduction of the sealed Final score.

Both cases contain one asset and two horizons. The official statistical fallback was not exercised by this pair. These examples do not measure route frequencies or attribute the competition result to a particular component.

## Remaining verification limits

- The new Docker recipe has not been built successfully because no Docker daemon was reachable in the validation environment.
- No new image execution or gVisor validation is claimed.
- The sealed Final data and per-task outcome breakdown are not included.
- Finite sampled predictions can differ across numerical backends; see [reproducibility](REPRODUCIBILITY.md).

Detailed source-check records are in [release checks](RELEASE_CHECKS.md). Earlier development comparisons and retrospective proxy results are retained in the [provenance archive](../provenance/README.md); they are not presented as results of additional released methods.
