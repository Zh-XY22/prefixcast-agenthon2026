# Data and dependencies

## Public example inputs

The documented examples use the official Track 2 repository at commit `0ddb8896a942b9d44c64927f74755e7012c3e5f9`. Follow [the example workflow](PUBLIC_EXAMPLE.md) to obtain and stage a single task.

Task panels, text, and realized labels are not redistributed in this code repository. Their source terms apply separately from the code license. Preserve the source files and their manifests; mount only the selected task's inputs for inference.

The final method estimates its numerical quantities from the supplied task prefix. It does not load pretrained weights, offline calibration tables, cross-task caches, or external model services. Input cutoff checks do not independently certify the historical vintage of every supplied observation.

## Software

- [Runtime dependency lock](../configs/requirements-runtime.lock): the packages needed by the public source installation.
- [Submitted environment record](../configs/submitted-environment.lock.json): the original numerical environment.
- [Dependency provenance](../configs/DEPENDENCY_PROVENANCE.csv): recorded package versions and license metadata.
- [Local wheel inventory](../configs/LOCAL_WHEEL_INVENTORY.csv): historical file hashes where available; this is not a list of additional required packages.

All 22 exact runtime pins installed from PyPI into a fresh Linux/x86_64 Python 3.12.15 environment on 2026-11-03, and `pip check` passed. No dependency versions were substituted. This does not verify installation on every operating system.

The exact bundled official sources retain their Track 2 MIT and shared-toolkit CC-BY-NC-4.0 notices. See [third-party notices](../THIRD_PARTY_NOTICES.md) and the [official source version record](ORIGINAL_OFFICIAL_VERSION_LOCK.json). The original official repository also contains the dataset licensing and provenance documents referenced by its notices.

## Network and system requirements

Package installation and Docker reconstruction require network access. Inference itself runs offline on CPU and needs no API key or team credentials. The Docker recipe installs the system OpenMP runtime `libgomp1`; a source installation also needs a compatible system runtime available.

No package wheels, virtual environments, CUDA libraries, datasets, or image TAR files are distributed here. See [reproducibility](REPRODUCIBILITY.md) for the original image and reconstruction limits.
