# Reproducibility and build scope

## Exact original image identity

`docker.io/xingyuzhang111/agenthon-t2@sha256:68b8c8bb61b27e44d1e70bfdc5aab28e701c342a078500c7e14d3c88ffa96055`
Config ID `sha256:f8a69b6b181bc4676668dba0dbebc391d3d8af71dca73a5920cd4616863c3192`. linux/amd64, user65534:65534, no VOLUME, interface2.0. Existing anonymous FULL crane pull verified accepted config identity; this export did not contact registry or repeat pulls. Preserve the original TAR externally for offline image backup; neither public ZIP nor private evidence archive embeds it.

The original Dockerfile is `docker/Dockerfile.submitted`, unchanged. Its base tag `agenthon-t2-base:python-f040863673ae-amd64` was a local pinned build reference; independently verifiable registry base digest UNKNOWN. It copies `/opt/numeric-runtime` (Python3.12.15) and runtime code. The outer base's inspect also contains Python3.13.16; the forecast shell selects the copied3.12 interpreter. Do not conflate it with the scoring/toolkit env3.13.16. Full original environment versions are in configs/submitted-environment.lock.json. Wheel provenance UNKNOWN where only installed dist-info remains; RECORD SHA is not a wheel SHA.

## Source-based reconstruction (not bit-for-bit image reproduction)

Run README install/build commands. All model/interface source is supplied under runtime, official package bytes preserved. The minimal runtime closure requirements are pinned; no unknown qfbench2 PyPI package is installed. All22 pinned runtime dependencies were fetched directly from PyPI and installed successfully in a fresh Python3.12.15 venv on2026-11-03; `pip check` passed. No version was changed. Docker source-rebuild base digest and apt libgomp package revision are UNKNOWN; network package fetching is a rebuild dependency. `docker/Dockerfile` and install/check scripts are EXPORT-ONLY non-algorithm adapters, not files from the submitted image. Original algorithm files unchanged. No claim that this recipe produces the same registry manifest digest.

The initial export was static-only. This revised release actually installed exact dependencies and ran two public source forecasts as UID65534: native EW40 and B4 CPU fallback, both500draws/three outputs and official G0–G3 PASS. There was no realized-label scoring. Docker build was attempted using only this public directory as context and failed before building because no daemon was reachable. No new image ID exists and no new image forecast is claimed. Historical six-case and two strict-runtime image checks were not repeated. See RELEASE_CHECKS.md and evidence/PUBLIC_REBUILD_CHECKS.json.

## Inputs and offline execution

Only the current task's files may be mounted. Inputs readonly; output writable by uid65534. tmpfs64MiB/noexec/nosuid/nodev, readonlyroot, capability drop, PID/FD limits are in the README example. Card-specific resources/deadlines take precedence. CPU numeric code does not compute on GPU; binding one allowed GPU in old host checks only establishes device exposure. No `--gpus all`.

Seed1 default/QFBENCH_SEED, 500 draws, nthread1. Cross-backend eigenvector sign differences can alter finite draws; original content identity does not establish universal numerical identity. Historical supplied-vintage labels are not rigorous real-time-vintage proof. Final ranked roster/performance not certified by Development-like checks.
