"""Configuración del área de estudio y rutas de datos."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"

CATALOGO_PRESAS_XLS = DATA_RAW_DIR / "0_Catalogo_de_presas.xls"
SERIES_PRESAS_DIR = DATA_RAW_DIR / "series_presas"

# Edad de diseño típica de una presa de tierra/enrocamiento antes de requerir
# rehabilitación mayor. Usada como umbral para el factor de antigüedad del
# índice de prioridad (ver src/models/indice_prioridad.py).
EDAD_DISENO_TIPICA_ANIOS = 50
