"""KPI del test A/B: embudo, tiempo en cada paso, errores y tiempo total.

Todas las funciones parten de la tabla web limpia (data/clean/web.csv) y de la
tabla de clientes, y devuelven tablas con una columna por grupo (Control, Test).
"""

import pandas as pd

ORDEN_GRUPOS = ["Control", "Test"]


def preparar_pasos(web, clientes):
    """Añade a cada clic su grupo y lo que hace falta para los KPI.

    La tabla se ordena por cliente, visita, hora y número de paso. Después se
    recorre fila a fila con un bucle for, mirando el clic siguiente (i + 1) y el
    anterior (i - 1). Solo cuentan si son de la misma visita (mismo cliente y
    misma visita):
    - tiempo_seg: segundos hasta el clic siguiente, es decir, el tiempo que el
      cliente pasó en este paso. El último clic de la visita queda vacío (None).
    - paso_anterior: número del paso del clic anterior. El primero queda vacío.
    - es_error: el cliente ha vuelto a un paso anterior (paso_num menor que el anterior).
    - es_repeticion: el mismo paso dos veces seguidas (por ejemplo, recargar la página).
    """
    pasos = web.merge(clientes[["client_id", "grupo"]], on="client_id")
    pasos = pasos.sort_values(["client_id", "visit_id", "date_time", "paso_num"]).reset_index(drop=True)

    # Las columnas se pasan a listas: recorrer una lista es mucho más rápido que usar .iloc en cada fila
    ids_cliente = list(pasos["client_id"])
    ids_visita = list(pasos["visit_id"])
    horas = list(pasos["date_time"])
    numeros = list(pasos["paso_num"])
    total = len(pasos)

    tiempo_seg = []
    paso_anterior = []
    for i in range(total):
        # ¿El clic siguiente es de la misma visita?
        if i + 1 < total and ids_cliente[i + 1] == ids_cliente[i] and ids_visita[i + 1] == ids_visita[i]:
            tiempo_seg.append((horas[i + 1] - horas[i]).total_seconds())
        else:
            tiempo_seg.append(None)
        # ¿El clic anterior es de la misma visita?
        if i > 0 and ids_cliente[i - 1] == ids_cliente[i] and ids_visita[i - 1] == ids_visita[i]:
            paso_anterior.append(numeros[i - 1])
        else:
            paso_anterior.append(None)

    pasos["tiempo_seg"] = tiempo_seg        # None se convierte en NaN (valor vacío)
    pasos["paso_anterior"] = paso_anterior
    pasos["es_error"] = pasos["paso_num"] < pasos["paso_anterior"]
    pasos["es_repeticion"] = pasos["paso_num"] == pasos["paso_anterior"]
    return pasos


def embudo(pasos, clientes, orden_pasos):
    """% de clientes de cada grupo que llega al menos una vez a cada paso.

    llegan tiene una fila por paso y una columna por grupo. Al dividir esa tabla
    entre total (una Serie con un valor por grupo), pandas divide cada columna
    por el total de su grupo, porque empareja los nombres de las columnas con
    los de la Serie.
    """
    llegan = pasos.groupby(["process_step", "grupo"])["client_id"].nunique().unstack()
    total = clientes["grupo"].value_counts()
    tabla = llegan / total * 100
    return tabla.loc[orden_pasos, ORDEN_GRUPOS].round(1)


def tiempo_por_paso(pasos, limite_seg, medida="median"):
    """Segundos en cada paso (sin confirm), por grupo, con la medida que se pida.

    medida es el nombre de la función de agregación: "median" (la principal,
    porque no la mueven los tiempos muy largos) o "mean".
    Se quitan los tiempos de más de limite_seg: son pausas (el cliente se fue y
    volvió), no tiempo dedicado al paso.
    """
    validos = pasos[(pasos["process_step"] != "confirm") & (pasos["tiempo_seg"] <= limite_seg)]
    tabla = validos.groupby(["process_step", "grupo"])["tiempo_seg"].agg(medida).unstack()
    return tabla[ORDEN_GRUPOS].round(1)


def tasa_errores(pasos):
    """Tasa de errores por grupo: pasos hacia atrás / total de pasos (fórmula del enunciado).

    Añade el % de clientes con al menos un error y la tasa de repeticiones del mismo paso.
    """
    agrupado = pasos.groupby("grupo")
    tabla = pd.DataFrame({
        "pasos": agrupado["es_error"].size(),
        "errores": agrupado["es_error"].sum(),
        "repeticiones": agrupado["es_repeticion"].sum(),
    })
    tabla["tasa_errores_pct"] = tabla["errores"] / tabla["pasos"] * 100
    tabla["tasa_repeticiones_pct"] = tabla["repeticiones"] / tabla["pasos"] * 100
    # Una fila por cliente: True si tuvo al menos un error
    error_cliente = pasos.groupby(["grupo", "client_id"])["es_error"].any().reset_index()
    tabla["clientes_con_error_pct"] = error_cliente.groupby("grupo")["es_error"].mean() * 100
    return tabla.loc[ORDEN_GRUPOS].round(1)


def errores_por_destino(pasos, orden_pasos):
    """A qué paso vuelven los clientes cuando van hacia atrás, por grupo.

    Solo salen los pasos a los que vuelve alguien, en el orden del proceso.
    """
    errores = pasos[pasos["es_error"]]
    tabla = pd.crosstab(errores["process_step"], errores["grupo"])
    pasos_con_errores = [paso for paso in orden_pasos if paso in tabla.index]
    return tabla.loc[pasos_con_errores, ORDEN_GRUPOS]


def tiempo_total(pasos):
    """Minutos desde el primer start hasta el primer confirm de cada cliente que completa.

    Se quitan los casos en que el primer confirm es anterior al primer start
    (registros incompletos). Devuelve una fila por cliente con su grupo y los minutos.
    """
    inicio = pasos[pasos["process_step"] == "start"].groupby("client_id")["date_time"].min()
    fin = pasos[pasos["process_step"] == "confirm"].groupby("client_id")["date_time"].min()
    tabla = pd.DataFrame({"inicio": inicio, "fin": fin}).dropna()
    tabla["minutos"] = (tabla["fin"] - tabla["inicio"]).dt.total_seconds() / 60
    tabla = tabla[tabla["minutos"] >= 0]
    grupos = pasos.drop_duplicates("client_id").set_index("client_id")["grupo"]
    tabla["grupo"] = grupos
    return tabla.reset_index()
