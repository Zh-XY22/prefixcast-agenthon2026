# Publication packaging

The algorithm and bundled official code under `runtime/` retain their original bytes. Parameters, routing, output identifiers, and the submitted Dockerfile are unchanged.

The public reconstruction recipe installs the pinned numerical environment instead of copying the original relocatable Python environment. It checks dependency compatibility and the forecast entry's executable permission. The installation helper accepts an explicit Python interpreter. These are packaging changes, not modifications to the forecasting method.

The source installation and two input cases were executed successfully as described in [release checks](RELEASE_CHECKS.md). The new Docker recipe remains unvalidated because the build environment could not reach a daemon. A source reconstruction is not expected to reproduce the original image digest byte for byte.

The public name is PrefixCast. Original implementation labels remain in the frozen code and generated output; [the method specification](METHOD.md) maps them to descriptive component names. Historical module branches that the final entry never calls remain in place to preserve the verified runtime bytes. Their names do not define supported model-selection options.

Historical path audits and export records are retained under [provenance](../provenance/README.md). They are not required by the forecast entry point.
