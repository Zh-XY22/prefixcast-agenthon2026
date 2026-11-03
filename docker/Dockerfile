# Public source reconstruction recipe; NOT Dockerfile.submitted.
# Original runtime/ bytes and dependency versions are unchanged.
FROM python:3.12.15-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*
COPY configs/requirements-runtime.lock /tmp/requirements-runtime.lock
RUN python -m pip install --no-cache-dir --no-deps -r /tmp/requirements-runtime.lock && python -m pip check
COPY runtime /opt/final-focus
RUN test -x /opt/final-focus/forecast
ENV PATH="/opt/final-focus:$PATH" HOME=/tmp PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
LABEL qfbench2.interface_version="2.0" qfbench2.track="forecasting" org.opencontainers.image.title="PrefixCast public source rebuild"
WORKDIR /tmp
USER 65534:65534
CMD ["forecast","--help"]
