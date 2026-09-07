"""Localidades pobladas de México, de GeoNames (dominio público / CC-BY 4.0).

Fuente: https://download.geonames.org/export/dump/MX.zip
Descargado el 2026-09-06. No requiere llave de acceso.

Se usa para estimar la exposición poblacional cerca de cada presa: cuántas
personas viven en un radio dado, como proxy simple de "qué tan grave sería
una falla" (no es un análisis de zona de inundación real con DEM, que
requeriría datos y tiempo adicionales — ver limitaciones en el README).
"""

import pandas as pd

from src.config import DATA_RAW_DIR

GEONAMES_MX_PATH = DATA_RAW_DIR / "geonames" / "MX.txt"

_COLUMNAS = [
    "geonameid", "nombre", "nombre_ascii", "nombres_alternos",
    "latitud", "longitud", "clase", "codigo_feature",
    "pais", "cc2", "admin1", "admin2", "admin3", "admin4",
    "poblacion", "elevacion", "dem", "timezone", "fecha_mod",
]


def cargar_localidades_pobladas() -> pd.DataFrame:
    """Carga las localidades de México con población conocida (>0).

    clase == 'P' es el código GeoNames para "populated place" (ciudad,
    pueblo, colonia, etc.) — excluye ríos, montañas, y otras features sin
    relación con población.
    """
    df = pd.read_csv(
        GEONAMES_MX_PATH,
        sep="\t",
        names=_COLUMNAS,
        usecols=["nombre", "latitud", "longitud", "clase", "poblacion"],
        low_memory=False,
    )
    return df[(df["clase"] == "P") & (df["poblacion"] > 0)].reset_index(drop=True)
