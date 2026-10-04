# Lector de certificados de discapacidad (svc-inclusion-pcd) para ECS Fargate.
# PyMuPDF, Pillow y ReportLab traen wheels precompiladas: no hacen falta paquetes
# del sistema. WeasyPrint y pdfkit están en requirements pero el código no los importa.

FROM python:3.12-slim AS build
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
COPY app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH=/opt/venv/bin:$PATH
RUN useradd --system --uid 10001 --home-dir /srv lector
COPY --from=build /opt/venv /opt/venv
WORKDIR /srv
COPY --chown=lector:lector app ./app
COPY --chmod=755 docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
USER lector
EXPOSE 8090
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8090/health', timeout=4).status == 200 else 1)"
# Dos workers como en el EC2. Los análisis viven en memoria por proceso: los
# clientes generan el PDF con POST /api/v1/analyses/pdf, no por id.
CMD ["/usr/local/bin/docker-entrypoint.sh"]
