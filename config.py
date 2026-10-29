"""Configuración del proyecto: rutas, archivos, columnas, categorías y umbrales.

Es un módulo de Python normal (como los .py de src/). Los notebooks lo importan con
`import config` y leen sus variables, por ejemplo `config.RUTA_RAW`. Si algo cambia
(otro nombre de archivo, otros tramos de edad, otro nivel de significación),
se cambia aquí y no dentro del código.

Las rutas son relativas a la carpeta del proyecto, que es donde están los
notebooks (junto a este archivo y a la carpeta src/).
"""

# Carpetas de datos
RUTA_RAW = "data/raw"      # archivos originales, sin tocar
RUTA_CLEAN = "data/clean"  # tablas limpias que generan los notebooks

# Archivos originales (son CSV aunque terminen en .txt)
# Las dos partes de los datos web van comprimidas en .zip (cada una tiene dentro su .txt
# original): sin comprimir pasan de 25 MB, el máximo que deja subir la web de GitHub.
# pd.read_csv lee el .zip directamente, sin descomprimirlo antes (no se vio en clase:
# pandas reconoce la extensión .zip y lo abre solo).
ARCHIVOS = {
    "demo": "df_final_demo.txt",
    "experimento": "df_final_experiment_clients.txt",
    "web": ["df_final_web_data_pt_1.zip", "df_final_web_data_pt_2.zip"],
}

# Pasos del proceso en orden; el número sirve para detectar cuándo un cliente vuelve atrás
PASOS = {"start": 0, "step_1": 1, "step_2": 2, "step_3": 3, "confirm": 4}

# Nombres nuevos de las columnas
RENOMBRAR_DEMO = {
    "clnt_tenure_yr": "antiguedad_anos",
    "clnt_age": "edad",
    "gendr": "genero",
    "num_accts": "num_cuentas",
    "bal": "saldo",
    "logons_6_mnth": "accesos_6m",
}
RENOMBRAR_EXPERIMENTO = {"Variation": "grupo"}

# Columnas que se quitan y por qué
COLUMNAS_DESCARTADAS = {
    "clnt_tenure_mnth": "repite la antigüedad en años, con más detalle del necesario",
    "calls_6_mnth": "en el 97 % de los clientes es exactamente accesos menos 3; aporta lo mismo",
}

# Género: de letra a texto claro
GENERO = {"M": "Hombre", "F": "Mujer", "U": "Desconocido", "X": "Otro"}

# Tramos: cada valor va al primer tramo cuyo límite superior lo supera
LIMITES_EDAD = [0, 30, 45, 60, 120]
NOMBRES_EDAD = ["<30", "30-44", "45-59", "60+"]
LIMITES_ANTIGUEDAD = [0, 5, 10, 20, 100]
NOMBRES_ANTIGUEDAD = ["<5 años", "5-9 años", "10-19 años", "20+ años"]

# KPI: un tiempo de más de 30 minutos en un paso es una pausa, no tiempo en el paso
LIMITE_TIEMPO_SEG = 1800

# Contrastes de hipótesis (notebook 04)
ALFA = 0.05            # nivel de significación
UMBRAL_MEJORA = 5      # mejora mínima de la tasa de finalización que pide Vanguard, en puntos
