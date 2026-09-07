"""Catálogo de presas monitoreadas por CONAGUA (Sistema de Información Hidrológica).

Fuente: https://sih.conagua.gob.mx/basedatos/Presas/0_Catalogo_de_presas.xls
Descargado manualmente el 2026-09-06 (el sitio está protegido por un firewall
anti-bots que bloquea la descarga por script).

Cobertura conocida: ~210 presas con estación de monitoreo activa de CONAGUA
(las presas mayores). NO es el inventario nacional completo (836 grandes +
4,330 chicas + ~8,000 bordos no registrados) ni incluye altura de cortina,
capacidad de almacenamiento, año de construcción o estado físico/operativo —
esos campos se solicitaron por separado vía la Plataforma Nacional de
Transparencia (ver plan del proyecto).
"""

import pandas as pd

from src.config import CATALOGO_PRESAS_XLS

_RENOMBRAR_COLUMNAS = {
    "Número": "numero",
    "Clave ": "clave",
    "Nombre de la presa": "nombre",
    "Latitud": "latitud",
    "Longitud": "longitud",
    "Altitud": "altitud_msnm",
    "Estado": "estado",
    "Municipio": "municipio",
    "Identificador de la \ncuenca de disponibilidad": "id_cuenca",
    "Cuenca de disponibilidad": "cuenca",
    "Número de la \nregión hidrológica": "id_region_hidrologica",
    "Región hidrológica": "region_hidrologica",
}


def cargar_catalogo() -> pd.DataFrame:
    """Carga el catálogo de presas monitoreadas y normaliza los nombres de columna."""
    df = pd.read_excel(CATALOGO_PRESAS_XLS)
    df = df.rename(columns=_RENOMBRAR_COLUMNAS)
    df["clave"] = df["clave"].str.strip()
    df["nombre"] = df["nombre"].str.strip()
    return df
