# Provenance archive

The active documentation describes one final system: [PrefixCast](../README.md).

This directory preserves the submitted implementation's provenance and earlier audit context. Internal experiment IDs, source paths, and legacy labels are retained here for traceability. They are not additional supported methods or required model-selection steps.

| File | Purpose |
|---|---|
| [SOURCE_MAP.json](SOURCE_MAP.json) | Published-file hashes and their original source/version relationships |
| [RELEASE_CHANGES.csv](RELEASE_CHANGES.csv) | Publication changes and file relocations |
| [LEGACY_PATH_AUDIT.json](LEGACY_PATH_AUDIT.json) | Why old workspace modules/configuration paths are not part of the final entry's dependencies |
| [ACCEPTANCE_SUMMARY.json](ACCEPTANCE_SUMMARY.json) | Earlier compatibility checks, preserved without changing their recorded labels |
| [HISTORICAL_PROXY_SUMMARY.csv](HISTORICAL_PROXY_SUMMARY.csv) | Separate retrospective proxy cohorts; not official Final scores |
| [HISTORICAL_EVALUATION.md](HISTORICAL_EVALUATION.md) | Archived evaluation narrative, including its small-sample limits and older research-version comparisons |

The runtime retains its original identifiers to match the verified submission. Human-readable names and their code-label mapping are defined in [the method specification](../docs/METHOD.md).

Start with [official results and validation](../docs/EVALUATION.md) for the final system. These archives are unnecessary for a normal installation or example run.
