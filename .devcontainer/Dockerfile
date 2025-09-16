FROM mambaorg/micromamba

# Install requirements into base environment
COPY env.yml /tmp/env.yml
RUN micromamba install -y -n base -f /tmp/env.yml \
 && micromamba clean --all --yes

# Setup nginx
COPY 4d-viewer-nginx.conf /opt/conda/etc/nginx/sites.d/4d-viewer-nginx.conf