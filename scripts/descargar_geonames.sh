#!/usr/bin/env bash
# Descarga las localidades pobladas de México de GeoNames (dominio público,
# ~70 MB descomprimido) que src/data_sources/poblacion.py necesita para
# estimar la exposición poblacional cerca de cada presa. No se incluye en el
# repositorio por su tamaño.
#
# Fuente: https://download.geonames.org/export/dump/MX.zip

set -euo pipefail

DESTINO="data/raw/geonames"
mkdir -p "$DESTINO"

curl -sL -o "$DESTINO/MX.zip" "https://download.geonames.org/export/dump/MX.zip"
unzip -o "$DESTINO/MX.zip" -d "$DESTINO"
rm "$DESTINO/MX.zip"

echo "Listo: $DESTINO/MX.txt"
