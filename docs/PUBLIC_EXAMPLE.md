# Fixed public historical examples

Fetch separately under the source's terms; no panels, text or labels are redistributed in this code release. The two release smoke cases are from official Track2 commit `0ddb8896a942b9d44c64927f74755e7012c3e5f9`:

|Unit|Actual cutoff|Targets|Route|
|---|---|---|---|
|t2-F1-curve-ust1y-001-ps1|2019-01-07|UST_1Y level,h2/3|EW40|
|t2-F1-fx-krw-011-ps1|2017-03-27|KRW level,h1/4|B4|

The historical examples' source fetch commands were not rerun; existing verified public bytes were reused. New source forecasts were run with those unchanged inputs, not synthesized short horizons. See evidence/PUBLIC_REBUILD_CHECKS.json for card/spec hashes and output gates.

Run these Bash commands from the repository root after `sh scripts/install.sh` has completed. Clone the fixed official inputs once, then stage and run each case separately.

## EW40 native example

```bash
git clone --no-checkout https://github.com/Agenthon-2026/track2-forecasting-public official-track2
git -C official-track2 checkout 0ddb8896a942b9d44c64927f74755e7012c3e5f9
UNIT=t2-F1-curve-ust1y-001-ps1
mkdir -p "inputs/$UNIT/panels" "inputs/$UNIT/text"
cp "official-track2/units/$UNIT/card.toml" "inputs/$UNIT/card.toml"
cp "official-track2/units/$UNIT/forecast_spec.json" "inputs/$UNIT/forecast_spec.json"
cp official-track2/units/"$UNIT"/*.parquet "inputs/$UNIT/panels/"
cp -R "official-track2/units/$UNIT/text/." "inputs/$UNIT/text/"

mkdir -p "out/$UNIT"
T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast \
  --panels "inputs/$UNIT/panels/" \
  --text "inputs/$UNIT/text/" \
  --asof 2019-01-07 \
  --out "out/$UNIT/forecast.parquet"
.venv/bin/python scripts/check_output.py \
  --card "inputs/$UNIT/card.toml" \
  --forecast "out/$UNIT/forecast.parquet"
```

The expected route is native EW40. The output directory is `out/t2-F1-curve-ust1y-001-ps1/`.

## B4 CPU fallback example

Use the same official checkout and Python environment; this case has its own cutoff date and output directory.

```bash
UNIT=t2-F1-fx-krw-011-ps1
mkdir -p "inputs/$UNIT/panels" "inputs/$UNIT/text"
cp "official-track2/units/$UNIT/card.toml" "inputs/$UNIT/card.toml"
cp "official-track2/units/$UNIT/forecast_spec.json" "inputs/$UNIT/forecast_spec.json"
cp official-track2/units/"$UNIT"/*.parquet "inputs/$UNIT/panels/"
cp -R "official-track2/units/$UNIT/text/." "inputs/$UNIT/text/"

mkdir -p "out/$UNIT"
T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast \
  --panels "inputs/$UNIT/panels/" \
  --text "inputs/$UNIT/text/" \
  --asof 2017-03-27 \
  --out "out/$UNIT/forecast.parquet"
.venv/bin/python scripts/check_output.py \
  --card "inputs/$UNIT/card.toml" \
  --forecast "out/$UNIT/forecast.parquet"
```

The expected route is B4 CPU fallback, including its required runtime fitting. The output directory is `out/t2-F1-fx-krw-011-ps1/`.

Each run writes `forecast.parquet`, `forecast_meta.json` and `forecast_rationale.md`; inspect the rationale/stdout for the actual route. The checker runs gates only, without realized labels or performance scoring.

Original source layout can vary: if data is already in `panels/`, stage that directory instead of root Parquet. Verify the unit's source manifest and preserve each original file. Do not modify card dates/targets, fabricate forecast_spec, regenerate the original manifest or expose other units. This stages interface inputs; it is not original-manifest re-signing.

The method ignores text. A long-horizon fallback exemplar is also available at initial official commit `30c8019d997f930eab9ba569d089d12298d86d8c`, unit `t2-EXAMPLE-ust-curve-1m` (no forecast_spec supplied there). It was not rerun in this release.
