# PrefixCast

**Joint Financial Forecasting with EWMA Paths and Tree-Based Fallbacks**

Team **HaHaHa placed 2nd in Agenthon 2026 Track 2**. The official Final leaderboard displays **−0.9513** (higher is better), verified on 2026-11-03: [official Final results](https://www.agenthon.net/#leaderboard). Original competition identifier: **QuantPrefixEW40V3**; all runtime method IDs, parameters, routing and output semantics remain unchanged.

The owner confirms the actually submitted whole-ZIP SHA256 is `dedcc25dabb09e16304a4281e9feda5afa1e5a4b7cb5b7e391a75ef3737095ab`, matching the archived production ZIP. An archived platform receipt/submission ID remains **NOT_FOUND/UNKNOWN**. The public team ranking and the owner's ZIP confirmation are separate evidence; neither supplies a missing per-submission receipt. See [final identity](docs/FINAL_VERSION.md).

Current-task EW40 joint paths → original CPU B4 → official R0. No packaged learned weights, text/House calls or external model endpoint. Own code is MIT; vendored shared toolkit is CC-BY-NC-4.0: see [third-party notices](THIRD_PARTY_NOTICES.md).

## Reproduce from source

Python 3.12 required; the submitted numeric runtime was 3.12.15. This release installed every pinned dependency into a fresh Python 3.12.15 environment, passed `pip check`, and ran the two public cases below as UID65534. **Docker rebuild was attempted but BLOCKED by an unavailable daemon; no new source-built image was validated.** These checks are not performance scoring.

```bash
# From the contents of github-ready/, not the private export directory:
sh scripts/install.sh
# If Python is not on PATH: PYTHON=/path/to/python3.12 sh scripts/install.sh
T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast --help
mkdir -p out
T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast \
  --panels inputs/example/panels/ --text inputs/example/text/ \
  --asof YYYY-MM-DD --out out/forecast.parquet
.venv/bin/python scripts/check_output.py \
  --card inputs/example/card.toml --forecast out/forecast.parquet
```

Use the actual card cutoff in place of `YYYY-MM-DD`; never alter dates, targets or panels. Fetch permitted public historical inputs separately as in [public examples](docs/PUBLIC_EXAMPLE.md). Required layout:

```text
inputs/example/card.toml
inputs/example/forecast_spec.json   # only when provided
inputs/example/panels/*.parquet
inputs/example/text/
out/forecast.parquet
out/forecast_meta.json
out/forecast_rationale.md
```

Native EW40: daily `rates_daily`/`g10_fx_daily`, horizons and explicit path offsets ≤4, at least101 aligned continuous rows. Other panels, horizons or insufficient histories explicitly enter B4 or R0. Exactly500 joint draws; seed1 default, overridden by `QFBENCH_SEED`. Rationale/stdout identify the actual route. No realized labels are supplied to the example gates.

|New public-source check|Actual route|Draws|Official gates|Runtime B4 fits|
|---|---|---:|---|---:|
|t2-F1-curve-ust1y-001-ps1; 2019-01-07; h2/3|EW40 native|500|G0–G3 PASS|0|
|t2-F1-fx-krw-011-ps1; 2017-03-27; h1/4|B4 CPU fallback|500|G0–G3 PASS|2|

Both exited0 and wrote exactly the three prescribed outputs. Input bytes, dates and target definitions were preserved. [Check details](docs/RELEASE_CHECKS.md); these are fresh-venv runs, **not Docker or gVisor checks**.

## Public source image recipe

```bash
docker build --platform linux/amd64 -f docker/Dockerfile -t prefixcast:source .
mkdir -p out
chmod 777 out
docker run --rm --network=none --read-only --user 65534:65534 \
  --cap-drop=ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  --pids-limit 256 --ulimit nofile=1024:1024 --ulimit nproc=256:256 \
  --cpus 2 --memory 16G --memory-swap 16G -e QFBENCH_SEED=1 \
  -v "$PWD/inputs/example:/input:ro" -v "$PWD/out:/output" \
  prefixcast:source forecast --panels /input/panels/ --text /input/text/ \
  --asof YYYY-MM-DD --out /output/forecast.parquet
```

Use the actual card's resource limits. The example output directory is newly created and must be writable by UID65534. CPU inference does not require GPU computation. Construction needs network for the Python base, apt and pinned wheels; inference is offline. `docker/Dockerfile` is the **public reconstruction recipe**, not the submitted recipe. `docker/Dockerfile.submitted` is preserved. A rebuild is not promised to reproduce the original digest.

Original immutable image: `docker.io/xingyuzhang111/agenthon-t2@sha256:68b8c8bb61b27e44d1e70bfdc5aab28e701c342a078500c7e14d3c88ffa96055`. Previous full anonymous pull evidence is historical; this release did not pull, rebuild, change or publish that image.

See [method](docs/METHOD.md), [reproducibility](docs/REPRODUCIBILITY.md), [evaluation](docs/EVALUATION.md), [data/dependencies](docs/DATA_AND_DEPENDENCIES.md) and `SOURCE_MAP.json`. Upload only this public directory's contents to GitHub. Claims/proofs, production ZIPs, raw private logs, datasets, environments, image TARs and paper working archives are excluded. No GitHub repository was created or pushed.
