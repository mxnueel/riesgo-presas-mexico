#!/usr/bin/env bash
# Descarga el Global Seismic Hazard Map del GEM Foundation (v2023.1, ~165 MB)
# que src/data_sources/peligro_sismico.py necesita para leer el PGA por
# coordenada. No se incluye en el repositorio por su tamaño (excede el
# límite de GitHub de 100 MB).
#
# Fuente: https://doi.org/10.5281/zenodo.8409647 (CC BY-NC-SA 4.0)

set -euo pipefail

DESTINO="data/raw/peligro_sismico_gem"
mkdir -p "$DESTINO"

curl -sL -o "$DESTINO/GEM-GSHM_PGA-475y-rock_v2023.zip" \
  "https://zenodo.org/records/8409647/files/GEM-GSHM_PGA-475y-rock_v2023.zip?download=1"

unzip -o "$DESTINO/GEM-GSHM_PGA-475y-rock_v2023.zip" -d "$DESTINO"
rm "$DESTINO/GEM-GSHM_PGA-475y-rock_v2023.zip"

echo "Listo: $DESTINO/v2023_1_pga_475_rock_3min.tif"
