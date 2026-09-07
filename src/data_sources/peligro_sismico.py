"""Peligro sísmico (PGA) por coordenada, a partir del Global Seismic Hazard Map
del GEM Foundation (OpenQuake), versión 2023.1.

Fuente: https://doi.org/10.5281/zenodo.8409647 (CC BY-NC-SA 4.0)
Descargado el 2026-09-06 en data/raw/peligro_sismico_gem/.

El raster da la Aceleración Máxima del Terreno (PGA, en fracción de g) con
10% de probabilidad de excedencia en 50 años (periodo de retorno ~475 años),
para condiciones de roca de referencia (Vs30 760-800 m/s), a ~6 km de
resolución (3 arcmin). Cobertura global, se usa aquí solo para México.

Nota de alcance: al ser condiciones de roca de referencia, no incluye
amplificación por sitio (suelos blandos, como en la Ciudad de México) — es
un valor base conservador-razonable para un screening, no un estudio de
sitio específico.
"""

import numpy as np
import pandas as pd
import rasterio

from src.config import DATA_RAW_DIR

RASTER_PGA_PATH = DATA_RAW_DIR / "peligro_sismico_gem" / "v2023_1_pga_475_rock_3min.tif"


def obtener_pga(lat: float, lon: float) -> float:
    """Devuelve el PGA (fracción de g) para una coordenada dada."""
    with rasterio.open(RASTER_PGA_PATH) as src:
        row, col = src.index(lon, lat)
        valor = src.read(1)[row, col]
        if valor == src.nodata or not np.isfinite(valor):
            raise ValueError(f"Sin dato de PGA para ({lat}, {lon})")
        return float(valor)


def agregar_pga(df: pd.DataFrame, col_lat: str = "latitud", col_lon: str = "longitud") -> pd.DataFrame:
    """Agrega una columna 'pga_g' al DataFrame, calculada por coordenada.

    Abre el raster una sola vez para todas las filas (más eficiente que
    llamar obtener_pga en un loop, que reabriría el archivo por cada fila).
    """
    df = df.copy()
    with rasterio.open(RASTER_PGA_PATH) as src:
        banda = src.read(1)
        pgas = []
        for lat, lon in zip(df[col_lat], df[col_lon]):
            row, col = src.index(lon, lat)
            valor = banda[row, col]
            pgas.append(float(valor) if np.isfinite(valor) and valor != src.nodata else np.nan)
    df["pga_g"] = pgas
    return df
