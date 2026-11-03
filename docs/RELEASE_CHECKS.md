# Publication release checks —2026-11-03

This release copies only the preceding public source tree into an independent directory. Display/docs/build-helper edits are listed in `RELEASE_CHANGES.csv`; runtime source, parameters, routing and output method IDs are unchanged. Production ZIP SHA is owner-confirmed; official team Final rank2/score−0.9513 was checked against the website. Archived platform receipt/submission ID is still missing.

## Actually executed

- All22 exact pins installed in fresh Python3.12.15 venv from direct PyPI, no paid proxy, no inherited site-packages; `pip check` passed.
- Public unit `t2-F1-curve-ust1y-001-ps1`, unchanged cutoff2019-01-07, level, UST_1Y,h2/3: native EW40;500draws; three prescribed outputs; exit0; official G0–G3 PASS.
- Public unit `t2-F1-fx-krw-011-ps1`, unchanged cutoff2017-03-27, level, KRW,h1/4: B4 CPU fallback;2 real runtime fits using XGBoost3.1.3,depth2/32rounds;500draws; three prescribed outputs; exit0; official G0–G3 PASS.
- Both ran exported `runtime/forecast` under UID65534, CPU only; read-only copies of original public inputs; no date/target edits, no realized labels and no performance scoring.
- Source syntax, hashes, executable modes, public archive boundaries and credential/proof exclusions are checked separately in the release manifest. Summaries preserve actual input/output hashes; raw logs and datasets stay outside the public directory.

## Docker rebuild BLOCKED

Actual command from this public-only build context:

```bash
docker build --platform linux/amd64 --pull=false -f docker/Dockerfile -t prefixcast:public-rebuild-20261103 .
```

Exit1: `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

Both the initial recipe and final wrapper-only recipe were actually attempted and failed before building. The final recipe adds `pip check`, an explicit executable check and a public-rebuild annotation; it remains unbuilt here. No daemon was installed or started, no socket/privilege workaround used, no original Final image modified. There is **no source-built image ID and no new Docker/gVisor smoke PASS**. To complete this gate, run the README build and these same two unmodified public cases on a Docker-capable machine. Old image success is historical evidence only.

## Scope

No tuning, research-model training,104-task rerun, GPU workload, new accuracy evaluation, registry push, GitHub push, team-key access or submission occurred. B4's two per-task fits are inference requirements and are not offline model retraining. Official team Final score is distinct from all local retrospective results.
