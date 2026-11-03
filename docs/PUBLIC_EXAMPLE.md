# Run PrefixCast on a public example

Both inputs below use the same `runtime/forecast` entry point and fixed configuration. The program selects its route automatically. The cases cover two execution paths of the final system; they are not competing model versions.

| Input case | Official unit ID | Cutoff | Requested target | Expected route |
|---|---|---|---|---|
| US Treasury yield | `t2-F1-curve-ust1y-001-ps1` | 2019-01-07 | UST_1Y level, horizons 2 and 3 | Exponentially weighted joint paths |
| Korean won | `t2-F1-fx-krw-011-ps1` | 2017-03-27 | KRW level, horizons 1 and 4 | Autoregressive trees with residual block sampling |

These IDs identify official input datasets. The original code labels seen in output logs are explained in [the method specification](METHOD.md).

## Install and fetch inputs once

Run from the repository root on the supported Linux/Python environment. The official data remain under their own terms and are not redistributed here.

```bash
sh scripts/install.sh
git clone --no-checkout https://github.com/Agenthon-2026/track2-forecasting-public official-track2
git -C official-track2 checkout 0ddb8896a942b9d44c64927f74755e7012c3e5f9
```

If Python is not on PATH, use `PYTHON=/path/to/python3.12 sh scripts/install.sh`. Reuse the checkout and environment for the second input.

## One prediction workflow

Choose a unit from the table by setting `UNIT`. The command reads the cutoff from that unit's original card, so no date or target needs to be edited.

```bash
UNIT=t2-F1-curve-ust1y-001-ps1
INPUT="inputs/$UNIT"
OUTPUT="out/$UNIT"

mkdir -p "$INPUT/panels" "$INPUT/text" "$OUTPUT"
cp "official-track2/units/$UNIT/card.toml" "$INPUT/card.toml"
cp "official-track2/units/$UNIT/forecast_spec.json" "$INPUT/forecast_spec.json"
cp official-track2/units/"$UNIT"/*.parquet "$INPUT/panels/"
cp -R "official-track2/units/$UNIT/text/." "$INPUT/text/"

ASOF=$(.venv/bin/python -c 'import pathlib, sys, tomllib; print(tomllib.loads(pathlib.Path(sys.argv[1]).read_text())["provenance"]["data_cutoff"])' "$INPUT/card.toml")

T2_PYTHON="$PWD/.venv/bin/python" ./runtime/forecast \
  --panels "$INPUT/panels/" --text "$INPUT/text/" \
  --asof "$ASOF" --out "$OUTPUT/forecast.parquet"

.venv/bin/python scripts/check_output.py \
  --card "$INPUT/card.toml" --forecast "$OUTPUT/forecast.parquet"
```

To exercise the tree route, change only `UNIT` to `t2-F1-fx-krw-011-ps1` and repeat this workflow. There is no model selector.

Each output directory contains `forecast.parquet`, `forecast_meta.json`, and `forecast_rationale.md`. The rationale/stdout reports the actual route. The official checker runs gates only, without realized labels or performance scoring.

## Validation scope

Both unchanged official inputs were used in the recorded source-run checks: each produced 500 draws and passed the official output gates. The two cases each contain one asset and two requested horizons; they do not establish complete coverage of every supported task.

The source-run check reused previously verified input bytes rather than downloading them again. The fixed repository directories were subsequently inspected to confirm the documented files exist. The documentation update unifies the commands; it does not claim a new prediction run. See [release checks](RELEASE_CHECKS.md) for the recorded executions.

Preserve original input bytes and source manifests. Copying files into this interface layout does not re-sign the original manifest. Do not change task dates, targets, or horizons.
