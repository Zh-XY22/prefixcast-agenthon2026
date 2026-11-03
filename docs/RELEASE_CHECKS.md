# Source release checks

## Recorded execution: 2026-11-03

All 22 exact dependency pins were installed from PyPI into a fresh Python 3.12.15 virtual environment; `pip check` passed. The environment did not inherit system site-packages.

The same exported forecasting program ran as UID 65534 on CPU with sampling seed 1 for both cases:

| Official unit | Actual component | Cutoff | Shape | Gates | Runtime tree fits |
|---|---|---|---|---|---:|
| `t2-F1-curve-ust1y-001-ps1` | Exponentially weighted joint paths | 2019-01-07 | [500, 1, 2] | G0–G3 PASS | 0 |
| `t2-F1-fx-krw-011-ps1` | Autoregressive trees with residual block sampling | 2017-03-27 | [500, 1, 2] | G0–G3 PASS | 2 |

Both exited successfully and produced the three prescribed output files. Input dates, targets, and bytes were preserved. No realized labels or performance scoring were used.

[The machine-readable summary](../evidence/PUBLIC_REBUILD_CHECKS.json) retains the original route labels, input/output hashes, and gate results. Raw logs and task data are not part of this repository.

## Docker reconstruction

The recorded build command was:

```bash
docker build --platform linux/amd64 --pull=false -f docker/Dockerfile -t prefixcast:public-rebuild-20261103 .
```

Both attempts failed before building with:

```text
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

No new image ID or container-run result exists. The original submitted image was not changed. Follow [reproducibility](REPRODUCIBILITY.md) to validate the reconstruction on a machine with a working Docker daemon.

## Documentation and source integrity

The repository presentation uses descriptive component names and one shared example workflow. This documentation cleanup does not constitute another forecast or image run.

The 131 frozen runtime files, fixed method configuration, dependency lock, and submitted Dockerfile remain byte-identical. [The source map](../provenance/SOURCE_MAP.json) and [change manifest](../provenance/RELEASE_CHANGES.csv) track publication edits and relocated audit files.
