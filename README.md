# Priorización de Riesgo Estructural en Presas de México

Código fuente del proyecto de Manuel Bautista Mejía sobre priorización del
riesgo en presas mexicanas usando datos abiertos.

CONAGUA reconoce públicamente que desconoce el estado físico de cerca de
1,000 de sus presas registradas por falta de presupuesto para inspeccionarlas
(de un inventario de 836 presas grandes, 4,330 chicas, y un estimado de 8,000
bordos ni siquiera registrados). 95 presas ya están clasificadas como de alto
riesgo. Este proyecto construye una herramienta de **triage/screening**: usa
datos abiertos de peligro sísmico y lluvia extrema para priorizar qué presas
sin inspección reciente necesitan revisión más urgente — no reemplaza la
inspección física, hace más eficiente el presupuesto de inspección que la
propia CONAGUA admite no tener.

## Alcance actual y limitación honesta

Este repositorio construye y valida la metodología sobre las **~210 presas
que CONAGUA ya monitorea activamente** (las que tienen estación en su
Sistema de Información Hidrológica) — es un dataset público y descargable,
pero es precisamente el subconjunto de presas **mejor** vigilado, no las
~1,000 sin supervisar que motivan el proyecto.

El ranking actual combina tres factores:

- **Peligro sísmico** (PGA, probabilidad de excedencia 10% en 50 años) — qué
  tan probable es un sismo fuerte en el sitio
- **Lluvia extrema histórica** (ajuste Gumbel a máximos anuales, 33 años de
  datos) — qué tan probable es una tormenta severa
- **Población cercana** (suma de población en 30 km, GeoNames) — qué tan
  grave sería una falla; es un proxy de consecuencia, no un mapa de
  inundación real (eso requeriría un modelo de elevación digital y análisis
  hidrológico de flujo, fuera del alcance actual)

Los dos primeros son *peligro* (probabilidad del evento detonante); el
tercero es *exposición/consecuencia*. Todavía **falta la tercera pieza
clásica del riesgo — vulnerabilidad** (qué tan débil está la presa misma:
altura de cortina, geometría, capacidad del vertedor, antigüedad, estado
físico/operativo) — porque esos campos no están en el catálogo público
disponible; se solicitaron por separado a través de la Plataforma Nacional
de Transparencia. En cuanto esos datos lleguen, `src/models/` es el lugar
para convertir el ranking de peligro+exposición en un screening estructural
completo (peligro × exposición × vulnerabilidad).

## Estructura del repositorio

```
.
├── src/
│   ├── config.py                       # Rutas y parámetros del proyecto
│   ├── data_sources/
│   │   ├── conagua_presas.py           # Catálogo de presas (nombre, ubicación, cuenca)
│   │   ├── peligro_sismico.py          # PGA por coordenada (GEM Foundation / OpenQuake)
│   │   ├── precipitacion.py            # Precipitación diaria histórica (NASA POWER)
│   │   └── poblacion.py                # Localidades pobladas de México (GeoNames)
│   └── models/
│       ├── exposicion_hidrologica.py   # Lluvia de diseño por ubicación (Gumbel)
│       ├── exposicion_poblacional.py   # Población dentro de un radio de cada presa
│       └── indice_prioridad.py         # Índice compuesto (sísmico + hidrológico + poblacional)
├── scripts/
│   ├── descargar_peligro_sismico.sh    # Descarga el raster de peligro sísmico (no incluido por tamaño)
│   └── descargar_geonames.sh           # Descarga las localidades de GeoNames (no incluido por tamaño)
├── data/
│   ├── raw/                            # Catálogo de presas + datos descargados (ver .gitignore)
│   └── processed/                      # Ranking final y mapa generado
├── run_pipeline.py                     # Ejecuta el pipeline de extremo a extremo
├── plot_mapa_riesgo.py                 # Genera el mapa de prioridad
└── requirements.txt
```

## Reproducir los resultados

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 1. Descargar el raster de peligro sísmico (165 MB, no incluido en el repo)
bash scripts/descargar_peligro_sismico.sh

# 2. Descargar las localidades pobladas de GeoNames (70 MB, no incluido)
bash scripts/descargar_geonames.sh

# 3. Descargar y cachear la precipitación histórica de las 210 presas
#    (tarda unos minutos, usa la API pública de NASA POWER, sin llave)
python3 -c "
from src.data_sources.conagua_presas import cargar_catalogo
from src.data_sources.precipitacion import fetch_precip_catalogo
fetch_precip_catalogo(cargar_catalogo())
"

# 4. Correr el pipeline y generar el mapa
python3 run_pipeline.py
python3 plot_mapa_riesgo.py
```

El catálogo de presas (`data/raw/0_Catalogo_de_presas.xls`) sí está incluido
en el repositorio: el sitio de origen (CONAGUA) está protegido por un
firewall anti-bots que bloquea la descarga automática, así que se descargó
manualmente y se conserva como archivo estático.

## Fuentes de datos

- **Catálogo de presas**: [Sistema de Información Hidrológica, CONAGUA](https://sih.conagua.gob.mx/basedatos/Presas/0_Catalogo_de_presas.xls) (descarga manual, sitio protegido contra scripts)
- **Peligro sísmico**: [GEM Foundation, Global Seismic Hazard Map v2023.1](https://doi.org/10.5281/zenodo.8409647) (CC BY-NC-SA 4.0)
- **Precipitación histórica**: [NASA POWER](https://power.larc.nasa.gov/docs/services/api/) (API pública, sin llave)
- **Localidades pobladas**: [GeoNames](https://download.geonames.org/export/dump/) (CC-BY 4.0)

## Licencia y contacto

Código bajo autoría de Manuel Bautista Mejía. Contacto: 18102328bmm@gmail.com
