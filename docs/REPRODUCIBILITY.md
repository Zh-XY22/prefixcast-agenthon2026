# Reproducibility

## Validated source environment

The source checks used Linux/x86_64, Python 3.12.15, and the exact 22 packages in [the runtime lock](../configs/requirements-runtime.lock). Installation and `pip check` passed in a fresh virtual environment.

Follow [the public example workflow](PUBLIC_EXAMPLE.md) for input acquisition, staging, prediction, and output checking. The same entry point automatically handles both example cases. The recorded runs used CPU, UID 65534, sampling seed 1, and read-only copies of the input files.

Each successful run produces 500 joint draws and the three documented output files. The default sampling seed is 1, configurable through `QFBENCH_SEED` or `--seed`. The tree component retains its fixed internal training seed of 1.

## Public Docker reconstruction

**This recipe has not been validated.** The recorded build attempts failed before building because the environment could not connect to a Docker daemon. There is no new image ID or image-run result.

On a machine with Docker, first prepare the selected public input and source environment using [the example workflow](PUBLIC_EXAMPLE.md), then run:

```bash
docker build --platform linux/amd64 -f docker/Dockerfile -t prefixcast:source .

UNIT=t2-F1-curve-ust1y-001-ps1
INPUT="inputs/$UNIT"
OUTPUT="out/docker/$UNIT"
ASOF=$(.venv/bin/python -c 'import pathlib, sys, tomllib; print(tomllib.loads(pathlib.Path(sys.argv[1]).read_text())["provenance"]["data_cutoff"])' "$INPUT/card.toml")
mkdir -p "$OUTPUT"
chmod 777 "$OUTPUT"

docker run --rm --network=none --read-only --user 65534:65534 \
  --cap-drop=ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  --pids-limit 256 --ulimit nofile=1024:1024 --ulimit nproc=256:256 \
  --cpus 2 --memory 16G --memory-swap 16G -e QFBENCH_SEED=1 \
  -v "$PWD/$INPUT:/input:ro" -v "$PWD/$OUTPUT:/output" \
  prefixcast:source forecast --panels /input/panels/ --text /input/text/ \
  --asof "$ASOF" --out /output/forecast.parquet

.venv/bin/python scripts/check_output.py \
  --card "$INPUT/card.toml" --forecast "$OUTPUT/forecast.parquet"
```

The dedicated output directory must be writable by UID 65534. Use each task card's applicable resource limits. Build-time downloads require network access; prediction is offline. GPU computation is not required.

The public Dockerfile installs pinned packages and the system OpenMP runtime. Its base-image digest and apt package revision are not locked, and its environment is not guaranteed to reproduce the original image byte for byte.

## Original submitted environment

Original immutable image reference:

```text
docker.io/xingyuzhang111/agenthon-t2@sha256:68b8c8bb61b27e44d1e70bfdc5aab28e701c342a078500c7e14d3c88ffa96055
```

The original image is Linux/amd64 and uses UID 65534. [Dockerfile.submitted](../docker/Dockerfile.submitted) is preserved. Its local base tag is a historical build reference, not a verified public registry dependency.

The submitted entry selects the copied Python 3.12.15 interpreter at `/opt/numeric-runtime/bin/python`. The outer base's Python version must not be confused with that numerical interpreter. [The submitted environment lock](../configs/submitted-environment.lock.json) records its packages.

Historical anonymous-pull evidence identifies the original image; it is not a current availability check. Neither the source repository nor its ZIP embeds the original image TAR. See [final version](FINAL_VERSION.md) for the image config and ZIP hashes.

## Numerical and validation limits

Different BLAS/eigensolver backends can change finite seeded draws, including through eigenvector sign differences. Source identity does not imply universal bitwise prediction equality.

The two recorded input cases are execution checks, not an independent reproduction of the sealed competition score. No new Docker or gVisor execution is claimed. Input cutoff checks do not independently establish every historical data vintage. See [evaluation](EVALUATION.md) and [release checks](RELEASE_CHECKS.md).
