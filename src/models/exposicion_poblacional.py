"""Exposición poblacional cerca de cada presa.

Limitación de alcance, explícita a propósito: esto suma la población de
localidades dentro de un radio fijo alrededor de cada presa (línea recta),
NO una zona de inundación real aguas abajo (que requeriría un modelo de
elevación digital y análisis hidrológico de flujo, fuera del alcance actual).
Es un proxy razonable para un screening -- "cuánta gente vive cerca" -- no
un mapa de inundación por falla de presa.
"""

import numpy as np
import pandas as pd

from src.data_sources.poblacion import cargar_localidades_pobladas

RADIO_TIERRA_KM = 6371.0


def _distancia_haversine_km(lat1, lon1, lat2, lon2):
    """Distancia en km entre pares de coordenadas (vectorizado con numpy)."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * RADIO_TIERRA_KM * np.arcsin(np.sqrt(a))


def agregar_poblacion_cercana(df: pd.DataFrame, radio_km: float = 30.0) -> pd.DataFrame:
    """Agrega 'poblacion_{radio_km}km' con la suma de población de
    localidades dentro del radio dado de cada presa.
    """
    df = df.copy()
    localidades = cargar_localidades_pobladas()

    lat_presas = df["latitud"].to_numpy()[:, None]
    lon_presas = df["longitud"].to_numpy()[:, None]
    lat_loc = localidades["latitud"].to_numpy()[None, :]
    lon_loc = localidades["longitud"].to_numpy()[None, :]

    distancias = _distancia_haversine_km(lat_presas, lon_presas, lat_loc, lon_loc)
    dentro_radio = distancias <= radio_km

    poblaciones = localidades["poblacion"].to_numpy()[None, :]
    suma_poblacion = (dentro_radio * poblaciones).sum(axis=1)

    df[f"poblacion_{int(radio_km)}km"] = suma_poblacion
    return df
