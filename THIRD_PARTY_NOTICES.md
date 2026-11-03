# Attribution and license boundaries

* Original method code and export-only helpers: MIT, based on the owner's prior explicit release declaration and frozen release.json. No new rights are asserted for third-party material.
* `runtime/official/qfbench2_track_forecasting`: Agenthon Track2 reference/interface source, MIT; preserve `runtime/licenses/T2-LICENSE` and `T2-THIRD-PARTY-NOTICES.md`.
* `runtime/official/qfbench2_common`: Copyright2026 Pawel Polak, **CC-BY-NC-4.0**, preserved in `runtime/licenses/TOOLKIT-LICENSE`. This restricts that component to noncommercial use; the whole repository is not uniformly MIT/OSI-open-source. Original attribution/source revision is in docs/ORIGINAL_OFFICIAL_VERSION_LOCK.json. Do not strip this notice when redistributing or modifying toolkit code.
* NumPy/pandas/SciPy/PyArrow/XGBoost and installed dependencies are not redistributed as binaries in this source archive. Exact recorded versions and metadata-license strings appear in configs/DEPENDENCY_PROVENANCE.csv; their own distribution licenses remain applicable.
* No task panels, corpus, market dataset, learned model, pretrained neural weight or wheel is included. Public availability is not a grant to redistribute data. Fetch permitted official historical inputs from the pinned source under their own terms.

The unchanged upstream `runtime/licenses/T2-THIRD-PARTY-NOTICES.md` contains relative links to its original `DATA-LICENSE.md` and `data/PROVENANCE.md`. Those dataset documents are not bundled in this data-free code release; consult the fixed official source checkout described in docs/DATA_AND_DEPENDENCIES.md. They are not inference imports. The original notice and its SHA256 remain unchanged.
