"""Cliente NASA POWER para precipitación diaria histórica (adaptado del
mismo patrón usado en Gemelos Digitales/pipeline/src/data_sources/nasa_power.py
para el proyecto del aguacate).

Se usa para estimar la tormenta de diseño (precipitación máxima esperada)
en la ubicación de cada presa, y compararla contra la capacidad de su
vertedor (ver src/models/exposicion_hidrologica.py).

No requiere llave de acceso: https://power.larc.nasa.gov/docs/services/api/
"""

from __future__ import annotations

import time

import pandas as pd
import requests

from src.config import DATA_RAW_DIR

POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PRECIP_CACHE_DIR = DATA_RAW_DIR / "precipitacion"


def fetch_daily_precip(lat: float, lon: float, start: str, end: str, timeout: int = 60) -> pd.Series:
    """Descarga la serie diaria de precipitación (mm) para una coordenada.

    start, end: fechas 'YYYYMMDD'. Devuelve una Serie indexada por fecha.
    """
    params = {
        "parameters": "PRECTOTCORR",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    response = requests.get(POWER_BASE_URL, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    props = payload["properties"]["parameter"]["PRECTOTCORR"]
    dates = sorted(props.keys())
    serie = pd.Series(
        [props[d] for d in dates],
        index=pd.to_datetime(dates, format="%Y%m%d"),
        name="precip_mm",
    )
    return serie.replace(-999, pd.NA).astype(float)


def fetch_precip_catalogo(
    df_presas: pd.DataFrame,
    start: str = "19910101",
    end: str = "20231231",
    pausa_seg: float = 0.5,
) -> None:
    """Descarga y guarda en caché (un CSV por presa) la serie histórica de
    precipitación de cada presa del catálogo. Omite las que ya están en caché
    (para poder interrumpir y reanudar sin perder progreso ni re-descargar).
    """
    PRECIP_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    total = len(df_presas)
    for i, fila in df_presas.iterrows():
        destino = PRECIP_CACHE_DIR / f"{fila['clave']}.csv"
        if destino.exists():
            continue
        try:
            serie = fetch_daily_precip(fila["latitud"], fila["longitud"], start, end)
            serie.to_csv(destino, header=True)
            print(f"[{i + 1}/{total}] {fila['clave']} ({fila['nombre']}): {len(serie)} dias OK")
        except Exception as exc:  # noqa: BLE001 - queremos continuar aunque falle una presa
            print(f"[{i + 1}/{total}] {fila['clave']} ({fila['nombre']}): ERROR {exc}")
        time.sleep(pausa_seg)


def cargar_precip_cache(clave: str) -> pd.Series:
    """Carga del caché local la serie de precipitación de una presa."""
    ruta = PRECIP_CACHE_DIR / f"{clave}.csv"
    serie = pd.read_csv(ruta, index_col=0, parse_dates=True)["precip_mm"]
    return serie


if __name__ == "__main__":
    # Prueba rapida en una sola presa (Infiernillo, Mich., una de mayor
    # exposicion sismica encontrada en el catalogo).
    serie = fetch_daily_precip(18.25, -101.9, "20230101", "20231231")
    print(f"Dias descargados: {len(serie)}")
    print(serie.describe())
