"""Carga y limpieza de los datos del test A/B de Vanguard.

Cada función hace un solo paso y devuelve un DataFrame nuevo, para poder
comprobar el resultado en el notebook antes de seguir. Los nombres de archivos,
columnas y categorías vienen de config.py.
"""

import pandas as pd


def cargar_datos(carpeta_raw, archivos):
    """Lee los archivos originales y une las dos partes de los datos web con pd.concat.

    Devuelve tres tablas: demo (perfil de cada cliente), experimento
    (grupo de cada cliente) y web (cada clic en el proceso).
    """
    demo = pd.read_csv(f"{carpeta_raw}/{archivos['demo']}")
    experimento = pd.read_csv(f"{carpeta_raw}/{archivos['experimento']}")
    partes_web = [pd.read_csv(f"{carpeta_raw}/{nombre}") for nombre in archivos["web"]]
    web = pd.concat(partes_web, ignore_index=True)
    return demo, experimento, web


def resumen_calidad(df):
    """Tabla de calidad: tipo, nulos y valores distintos de cada columna."""
    return pd.DataFrame({"tipo": df.dtypes.astype(str),
                         "nulos": df.isna().sum(),
                         "distintos": df.nunique()})


def limpiar_texto(df):
    """Quita los espacios del principio y del final en todas las columnas de texto.

    Un espacio de más hace que «Test» y «Test » cuenten como valores distintos y que
    los merge no encuentren coincidencias. include=["object", "string"] selecciona las
    columnas de texto tanto en pandas 2 como en pandas 3.
    Devuelve una copia limpia y el número de celdas que han cambiado.
    """
    df = df.copy()
    cambiadas = 0
    for columna in df.select_dtypes(include=["object", "string"]).columns:
        limpia = df[columna].str.strip()
        distintas = (limpia != df[columna]) & df[columna].notna()
        cambiadas += int(distintas.sum())
        df[columna] = limpia
    return df, cambiadas


def limpiar_experimento(experimento, renombrar):
    """Deja solo a los clientes con grupo (Test o Control).

    Los clientes sin grupo no participaron en el test: no vieron ninguno
    de los dos diseños, así que no sirven para compararlos.
    """
    df = experimento.rename(columns=renombrar).dropna(subset=["grupo"])
    assert df["grupo"].isin(["Test", "Control"]).all()
    assert df["client_id"].is_unique
    return df.reset_index(drop=True)


def limpiar_demo(demo, renombrar, descartar, genero):
    """Limpia el perfil: quita filas vacías y columnas repetidas, renombra y traduce el género.

    - Filas vacías: solo tienen client_id; no hay nada que analizar y no se rellenan
      (rellenar con la media inventaría clientes).
    - Columnas descartadas: ver config.py (repiten información de otras).
    - Género: las letras pasan a texto claro; U = Desconocido.
    """
    df = demo.drop(columns=list(descartar))
    df = df.dropna(subset=[c for c in df.columns if c != "client_id"], how="all")
    df = df.rename(columns=renombrar)
    df["genero"] = df["genero"].str.strip().map(genero)
    for columna in ["antiguedad_anos", "num_cuentas", "accesos_6m"]:
        df[columna] = df[columna].astype(int)  # son cuentas enteras: 2.0 pasa a 2
    assert df["client_id"].is_unique
    assert df["genero"].notna().all()
    return df.reset_index(drop=True)


def unir_clientes(demo, experimento):
    """Une el perfil de cada cliente con su grupo (solo clientes que están en las dos tablas)."""
    df = experimento.merge(demo, on="client_id", how="inner")
    assert len(df) == df["client_id"].nunique()
    return df


def limpiar_web(web, clientes, pasos):
    """Limpia los clics: sin duplicados, con fecha y solo de clientes del test.

    - drop_duplicates: un clic repetido en el mismo segundo contaría un paso dos veces.
    - pd.to_datetime: hace falta para medir el tiempo entre pasos.
    - paso_num: número del paso (start = 0 ... confirm = 4) para ordenar y, más
      adelante, detectar cuándo un cliente vuelve atrás.
    - Se ordena por cliente, visita, hora y número de paso: si dos pasos tienen
      la misma hora, va primero el paso anterior del proceso.
    """
    df = web.drop_duplicates()
    df = df[df["client_id"].isin(clientes)].copy()
    df["date_time"] = pd.to_datetime(df["date_time"])
    df["paso_num"] = df["process_step"].map(pasos)
    assert df["paso_num"].notna().all()
    df = df.sort_values(["client_id", "visit_id", "date_time", "paso_num"])
    return df.reset_index(drop=True)
