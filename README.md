# PrefixCast

**Joint Financial Forecasting with EWMA Paths and Tree-Based Fallbacks**

[中文说明](README_zh.md)

PrefixCast is the final forecasting system used by team **HaHaHa**, which placed **2nd in Agenthon 2026 Track 2**. The [official Final leaderboard](https://www.agenthon.net/#leaderboard) reports **−0.9513** (higher is better; checked 2026-11-03).

## Method

One forecasting entry point automatically routes each task through the following components:

| Component | Role in the final system |
|---|---|
| Exponentially weighted joint paths | For supported short-horizon daily rates and G10 FX tasks, estimate a covariance matrix with a 40-observation half-life and 10% diagonal shrinkage, then sample joint Gaussian increment paths. |
| Autoregressive trees with residual block sampling | For tasks outside that scope, or when the first component cannot run, fit XGBoost on the current task history and sample aligned residual blocks. |
| Official statistical fallback | If the tree component fails, use the bundled official statistical forecaster. Invalid inputs can still fail. |

Every successful forecast contains **500 joint samples** across the requested assets and horizons. The system uses the supplied historical prefix, runs on CPU, and needs no pretrained weights or external model service. The required text argument is retained for the competition interface; its contents are not used.

The route is selected by the program. Users do not select a model or combine predictions from separate experiments. See the [method specification](docs/METHOD.md) for scope, equations, and the mapping from descriptive names to the original code labels.

## Quick start

The validated source environment is Linux/x86_64 with Python 3.12.15 and the pinned dependencies.

```bash
sh scripts/install.sh
# If needed: PYTHON=/path/to/python3.12 sh scripts/install.sh
```

Follow the [public example workflow](docs/PUBLIC_EXAMPLE.md) to fetch a fixed official input and run the forecast. It provides one execution workflow and two optional input cases that exercise different routes of this same program.

For an input staged as described there, the prediction interface is:

```bash
T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast \
  --panels "$INPUT/panels/" --text "$INPUT/text/" \
  --asof "$ASOF" --out "$OUTPUT/forecast.parquet"
```

Each run writes `forecast.parquet`, `forecast_meta.json`, and `forecast_rationale.md`. The rationale and stdout identify the route actually used.

## Validation and reproduction

Fresh-environment source runs passed the official output gates on one joint-path case and one tree-model case. These are execution and output checks, not additional accuracy measurements. The public Docker recipe has **not been validated**: the build attempts could not connect to a Docker daemon.

- [Results and validation scope](docs/EVALUATION.md)
- [Environment, Docker commands, and reproducibility](docs/REPRODUCIBILITY.md)
- [Data and dependency sources](docs/DATA_AND_DEPENDENCIES.md)
- [Submitted version and immutable image identity](docs/FINAL_VERSION.md)

## Repository layout

| Directory | Contents |
|---|---|
| `runtime/` | The unchanged submitted forecasting implementation and bundled official interfaces |
| `configs/` | Dependency locks and a description of the fixed method parameters |
| `scripts/`, `docker/` | Installation, output checking, and image reconstruction |
| `docs/` | The final method and its reproduction instructions |
| `evidence/` | Submitted-version identity and source-run summaries |
| `provenance/` | File hashes and archived development/audit records; not alternative methods to run |

The original runtime identifier is preserved for submission traceability; PrefixCast is the public method name. Historical experiment labels and comparisons are documented only where needed to interpret the frozen implementation or archived evidence.

## License

Participant-authored code and release helpers use the [MIT license](LICENSE). Bundled third-party components retain their own licenses, including CC-BY-NC-4.0 for the shared official toolkit. See [third-party notices](THIRD_PARTY_NOTICES.md).
