"""Genera un mapa de dispersión (lon/lat) de las presas, coloreado por su
índice de prioridad de revisión. No usa un basemap geográfico (para no
depender de geopandas/cartopy) — la forma de México es reconocible solo con
los puntos.
"""

import matplotlib.pyplot as plt
import pandas as pd

from src.config import DATA_PROCESSED_DIR


def main() -> None:
    ruta = DATA_PROCESSED_DIR / "ranking_prioridad_presas.csv"
    df = pd.read_csv(ruta)

    fig, ax = plt.subplots(figsize=(10, 7))
    disp = ax.scatter(
        df["longitud"],
        df["latitud"],
        c=df["indice_prioridad"],
        cmap="YlOrRd",
        s=40,
        edgecolors="black",
        linewidths=0.3,
    )

    top10 = df.nlargest(10, "indice_prioridad")
    for _, fila in top10.iterrows():
        ax.annotate(
            fila["clave"],
            (fila["longitud"], fila["latitud"]),
            fontsize=7,
            xytext=(3, 3),
            textcoords="offset points",
        )

    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_title(
        "Índice de prioridad de revisión\n"
        "(peligro sísmico + lluvia extrema + población cercana) — presas monitoreadas por CONAGUA"
    )
    ax.set_aspect("equal")
    fig.colorbar(disp, ax=ax, label="Índice de prioridad (percentil combinado)")
    fig.tight_layout()

    destino = DATA_PROCESSED_DIR / "mapa_prioridad_presas.png"
    fig.savefig(destino, dpi=150)
    print(f"Guardado: {destino}")


if __name__ == "__main__":
    main()
