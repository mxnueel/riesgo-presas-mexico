"""Ejecuta el pipeline de extremo a extremo: catálogo de presas -> exposición
sísmica + hidrológica -> índice de prioridad de revisión.

Requiere haber corrido antes la descarga de precipitación histórica
(ver src/data_sources/precipitacion.fetch_precip_catalogo), ya que ese paso
tarda varios minutos y se deja en caché local para no repetirlo.
"""

from src.config import DATA_PROCESSED_DIR
from src.data_sources.conagua_presas import cargar_catalogo
from src.data_sources.peligro_sismico import agregar_pga
from src.models.exposicion_hidrologica import agregar_exposicion_hidrologica
from src.models.indice_prioridad import calcular_indice_prioridad


def main() -> None:
    print("Cargando catálogo de presas...")
    df = cargar_catalogo()
    print(f"  {len(df)} presas")

    print("Calculando peligro sísmico (PGA) por ubicación...")
    df = agregar_pga(df)

    print("Calculando exposición a lluvia extrema (Gumbel, 100 años)...")
    df = agregar_exposicion_hidrologica(df)

    print("Calculando índice de prioridad...")
    df = calcular_indice_prioridad(df)

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    salida = DATA_PROCESSED_DIR / "ranking_prioridad_presas.csv"
    columnas = [
        "clave",
        "nombre",
        "estado",
        "municipio",
        "latitud",
        "longitud",
        "pga_g",
        "lluvia_diseno_100a_mm",
        "percentil_sismico",
        "percentil_hidrologico",
        "indice_prioridad",
    ]
    df[columnas].to_csv(salida, index=False)
    print(f"\nGuardado: {salida}")
    print("\nTop 15 presas por índice de prioridad de revisión:")
    print(df[["clave", "nombre", "estado", "indice_prioridad"]].head(15).to_string(index=False))


if __name__ == "__main__":
    main()
