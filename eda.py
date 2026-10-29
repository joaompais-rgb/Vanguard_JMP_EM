"""Funciones del análisis exploratorio: tramos, gráficos univariantes y comportamiento.

Los gráficos se muestran en el notebook con plt.show(); no se guardan en archivos.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

COLOR = "#1f77b4"
COLORES_GRUPO = {"Control": "#999999", "Test": COLOR}


def tramo(valor, limites, nombres):
    """Devuelve el tramo de un valor con condiciones simples (if).

    limites y nombres vienen de config.py. Por ejemplo, con limites [0, 30, 45, 60, 120]
    y nombres ["<30", "30-44", "45-59", "60+"], una edad de 50 devuelve "45-59".
    Si el valor falta, devuelve None.
    """
    if pd.isna(valor):
        return None
    for i in range(len(nombres)):
        if valor < limites[i + 1]:
            return nombres[i]
    return nombres[-1]


def histograma_y_caja(serie, titulo, etiqueta):
    """Histograma y diagrama de caja de una variable numérica, uno encima del otro.

    El histograma muestra la forma; la caja, la mediana, los cuartiles y los valores atípicos.
    La mediana se escribe en el título.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    sns.histplot(serie.dropna(), bins=30, ax=ax1, color=COLOR)
    ax1.set_title(f"{titulo} (mediana = {round(serie.median())})")
    ax1.set_ylabel("Clientes")
    sns.boxplot(x=serie.dropna(), ax=ax2, color=COLOR)
    ax2.set_xlabel(etiqueta)
    plt.tight_layout()
    plt.show()


def barras_categoria(serie, titulo, etiqueta):
    """Barras con el porcentaje de cada categoría (en el orden de la propia variable)."""
    porcentaje = serie.value_counts(normalize=True).sort_index() * 100
    plt.figure(figsize=(7, 4))
    sns.barplot(x=porcentaje.index.astype(str), y=porcentaje.values, color=COLOR)
    plt.title(titulo)
    plt.xlabel(etiqueta)
    plt.ylabel("% de clientes")
    plt.tight_layout()
    plt.show()


def comportamiento_por_cliente(web):
    """Una fila por cliente: visitas, clics, dispositivos y qué pasos llegó a hacer.

    completo = llegó a 'confirm' al menos una vez (definición D1 de preguntas.md).
    Las visitas se cuentan por cliente, así que una visita compartida por dos
    clientes cuenta para cada uno por separado.
    """
    agrupado = web.groupby("client_id")
    por_cliente = pd.DataFrame({
        "visitas": agrupado["visit_id"].nunique(),
        "clics": agrupado["process_step"].count(),
        "dispositivos": agrupado["visitor_id"].nunique(),
        "paso_max": agrupado["paso_num"].max(),
    })
    pasos_hechos = agrupado["process_step"].unique()
    por_cliente["empezo"] = pasos_hechos.apply(lambda pasos: "start" in pasos)
    por_cliente["completo"] = pasos_hechos.apply(lambda pasos: "confirm" in pasos)
    por_cliente["confirm_sin_step_3"] = pasos_hechos.apply(lambda pasos: "confirm" in pasos and "step_3" not in pasos)
    return por_cliente.reset_index()


def ids_compartidos(web, columna):
    """Cuántos valores de una columna (visitor_id o visit_id) aparecen con más de un cliente."""
    clientes_por_id = web.groupby(columna)["client_id"].nunique()
    return int((clientes_por_id > 1).sum())


def tasa_por_categoria(por_cliente, columna, orden=None):
    """Porcentaje de clientes que completan, por categoría y grupo, con el número de clientes.

    Devuelve una tabla con una fila por categoría y las columnas Control, Test,
    diferencia (Test - Control, en puntos) y clientes. Si se da una lista en orden,
    las filas salen en ese orden (con .loc).
    """
    tabla = por_cliente.groupby([columna, "grupo"])["completo"].mean().unstack() * 100
    tabla["diferencia"] = tabla["Test"] - tabla["Control"]
    tabla["clientes"] = por_cliente.groupby(columna)["client_id"].count()
    if orden is not None:
        tabla = tabla.loc[orden]
    return tabla.round(1)


def barras_por_grupo(tabla, titulo, etiqueta, etiqueta_y="% que completa el proceso"):
    """Barras agrupadas Control / Test para cada categoría (filas de la tabla).

    melt pasa la tabla de ancha (Control y Test en columnas) a larga (una fila por
    categoría y grupo), que es lo que necesita sns.barplot para usar hue.
    """
    datos = tabla[["Control", "Test"]].reset_index().melt(id_vars=tabla.index.name, var_name="grupo", value_name="valor")
    plt.figure(figsize=(8, 4))
    sns.barplot(data=datos, x=tabla.index.name, y="valor", hue="grupo", palette=COLORES_GRUPO)
    plt.title(titulo)
    plt.xlabel(etiqueta)
    plt.ylabel(etiqueta_y)
    plt.tight_layout()
    plt.show()


def barras_simples(serie, titulo, etiqueta, etiqueta_y):
    """Barras de una Serie ya calculada (por ejemplo, clics por día de la semana), en su orden."""
    plt.figure(figsize=(8, 4))
    sns.barplot(x=serie.index.astype(str), y=serie.values, color=COLOR)
    plt.title(titulo)
    plt.xlabel(etiqueta)
    plt.ylabel(etiqueta_y)
    plt.tight_layout()
    plt.show()
