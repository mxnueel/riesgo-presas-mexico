"""Índice de prioridad de revisión: combina los factores disponibles en un
solo ranking.

Ahora con tres factores:
- Peligro sísmico (PGA) — qué tan probable es un sismo fuerte en el sitio
- Lluvia extrema (Gumbel, 100 años) — qué tan probable es una tormenta severa
- Población cercana (30 km) — qué tan grave sería una falla (proxy de
  consecuencia, no un mapa de inundación real)

Los dos primeros son "peligro" (probabilidad de un evento detonante); el
tercero es "exposición/consecuencia" (qué hay en riesgo si el evento ocurre
y la presa falla). Un índice de riesgo real combina ambas dimensiones — este
todavía no incluye la tercera pieza clásica del riesgo, "vulnerabilidad"
(qué tan débil está la presa misma: altura, antigüedad, estado físico),
porque ese dato sigue pendiente de la solicitud de transparencia.

Método: percentil de cada factor (0-100). El peligro (sísmico + hidrológico)
se promedia primero entre sí, y ese promedio se combina con el percentil de
población cercana (también promedio simple) — así ningún factor de peligro
domina solo por tener dos entradas en vez de una.
"""

import pandas as pd


def calcular_indice_prioridad(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas de percentil por factor y un índice compuesto.

    Requiere que el DataFrame ya tenga 'pga_g', 'lluvia_diseno_100a_mm' y
    'poblacion_30km' (ver los módulos de src/data_sources y src/models
    correspondientes).
    """
    df = df.copy()
    df["percentil_sismico"] = df["pga_g"].rank(pct=True) * 100
    df["percentil_hidrologico"] = df["lluvia_diseno_100a_mm"].rank(pct=True) * 100
    df["percentil_poblacional"] = df["poblacion_30km"].rank(pct=True) * 100

    percentil_peligro = df[["percentil_sismico", "percentil_hidrologico"]].mean(axis=1)
    df["indice_prioridad"] = (percentil_peligro + df["percentil_poblacional"]) / 2

    return df.sort_values("indice_prioridad", ascending=False).reset_index(drop=True)
