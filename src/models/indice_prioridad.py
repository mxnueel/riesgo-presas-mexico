"""Índice de prioridad de revisión: combina los factores de exposición
disponibles en un solo ranking.

IMPORTANTE — limitación de alcance, explícita a propósito: este índice usa
solo factores de EXPOSICIÓN por ubicación (peligro sísmico, lluvia extrema).
No incluye margen estructural real (altura de cortina, geometría, capacidad
de vertedor, estado físico, antigüedad) porque esos datos no están en el
catálogo público disponible — están pendientes de la solicitud de
transparencia (ver plan del proyecto). Por lo tanto, este ranking prioriza
"qué presas están en las ubicaciones más exigentes", no "qué presas están
estructuralmente más débiles". Es un punto de partida honesto, no un
diagnóstico de seguridad estructural.

Método: percentil de cada factor (0-100), promedio simple. Usar percentil
en vez de z-score porque las distribuciones de PGA y lluvia extrema son muy
sesgadas (pocas presas con valores muy altos) — el percentil es más robusto
e interpretable ("está en el top X% del país en este factor").
"""

import pandas as pd


def calcular_indice_prioridad(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas de percentil por factor y un índice compuesto.

    Requiere que el DataFrame ya tenga las columnas 'pga_g' y
    'lluvia_diseno_100a_mm' (ver peligro_sismico.agregar_pga y
    exposicion_hidrologica.agregar_exposicion_hidrologica).
    """
    df = df.copy()
    df["percentil_sismico"] = df["pga_g"].rank(pct=True) * 100
    df["percentil_hidrologico"] = df["lluvia_diseno_100a_mm"].rank(pct=True) * 100

    df["indice_prioridad"] = df[["percentil_sismico", "percentil_hidrologico"]].mean(axis=1)

    return df.sort_values("indice_prioridad", ascending=False).reset_index(drop=True)
