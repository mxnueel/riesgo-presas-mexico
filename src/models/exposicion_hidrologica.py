"""Exposición a lluvia extrema por ubicación de presa.

Nota de alcance: el catálogo disponible (ver src/data_sources/conagua_presas.py)
NO incluye la capacidad de diseño del vertedor de cada presa (ese dato está
pendiente de la solicitud de transparencia). Por lo tanto, esto NO compara
capacidad vs. tormenta de diseño todavía — solo cuantifica qué tan severa es
la lluvia extrema histórica en la ubicación de cada presa, como factor de
EXPOSICIÓN (igual en espíritu al PGA de src/data_sources/peligro_sismico.py).
Cuando llegue el dato de capacidad del vertedor, este módulo es el punto para
convertir la exposición en un screening real de suficiencia hidráulica.

Método: máximos anuales de precipitación diaria (mm/día) ajustados a una
distribución Gumbel (método estándar en hidrología para lluvias extremas),
para estimar la lluvia de diseño a un periodo de retorno dado.
"""

import numpy as np
import pandas as pd
from scipy import stats

from src.data_sources.precipitacion import cargar_precip_cache


def maximos_anuales(clave: str) -> pd.Series:
    """Precipitación diaria máxima por año, a partir del caché histórico."""
    serie = cargar_precip_cache(clave)
    return serie.groupby(serie.index.year).max()


def lluvia_diseno_gumbel(clave: str, periodo_retorno_anios: int = 100) -> float:
    """Estima la precipitación diaria (mm) esperada para el periodo de
    retorno dado, ajustando una distribución Gumbel a los máximos anuales.

    Devuelve NaN si no hay suficientes años de datos (mínimo 10) para un
    ajuste razonable.
    """
    maximos = maximos_anuales(clave).dropna()
    if len(maximos) < 10:
        return float("nan")

    loc, escala = stats.gumbel_r.fit(maximos.values)
    prob_no_excedencia = 1 - 1 / periodo_retorno_anios
    return float(stats.gumbel_r.ppf(prob_no_excedencia, loc=loc, scale=escala))


def agregar_exposicion_hidrologica(
    df: pd.DataFrame, col_clave: str = "clave", periodo_retorno_anios: int = 100
) -> pd.DataFrame:
    """Agrega la columna 'lluvia_diseno_100a_mm' al DataFrame de presas."""
    df = df.copy()
    valores = []
    for clave in df[col_clave]:
        try:
            valores.append(lluvia_diseno_gumbel(clave, periodo_retorno_anios))
        except FileNotFoundError:
            valores.append(float("nan"))
    df[f"lluvia_diseno_{periodo_retorno_anios}a_mm"] = valores
    return df
