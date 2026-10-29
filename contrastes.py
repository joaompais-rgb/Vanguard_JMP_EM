"""Contrastes de hipótesis del test A/B (días 4 y 5).

Siguen el esquema de la lección de contrastes de hipótesis: se plantean H0 y H1,
se fija el nivel de significación (config.ALFA), se calcula el estadístico y el
p-valor con scipy.stats y se decide con un if: si el p-valor es menor que alfa,
se rechaza H0.

Las variables de resultado son columnas de 0 y 100 (por ejemplo, completo_pct):
su media es directamente el % de clientes y la diferencia de medias son puntos.
"""

import pandas as pd
import scipy.stats as st
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association


def decision(p_valor, alfa):
    """Devuelve el texto de la decisión: se rechaza o no la hipótesis nula."""
    if p_valor < alfa:
        return "Se rechaza H0"
    return "No se puede rechazar H0"


def formato_p(p_valor):
    """Escribe el p-valor con 4 decimales, o '< 0.0001' si es más pequeño."""
    if p_valor < 0.0001:
        return "< 0.0001"
    return f"{round(p_valor, 4)}"


def contraste_medias(test, referencia, alfa, una_cola=False):
    """t de Welch entre el grupo Test y una referencia (st.ttest_ind con equal_var=False).

    - referencia suele ser el grupo Control. Para el umbral del 5 % se pasa el
      Control desplazado (Control + 5) o escalado (Control x 1.05).
    - una_cola=False: H1 dice que Test y referencia son distintos (dos colas).
    - una_cola=True: H1 dice que el Test es mayor. Como en la lección, el p-valor de
      dos colas cuenta las dos colas (por eso allí se multiplica por 2); el de una cola
      es la mitad si el Test va en la dirección de H1 (t positivo) y 1 menos esa mitad si no.
    Devuelve un diccionario con las medias, la diferencia, el estadístico t,
    el p-valor (en texto) y la decisión.
    """
    estadistico, p_dos_colas = st.ttest_ind(test, referencia, equal_var=False)
    if not una_cola:
        p_valor = p_dos_colas
    elif estadistico > 0:
        p_valor = p_dos_colas / 2
    else:
        p_valor = 1 - p_dos_colas / 2
    return {
        "clientes_test": len(test),
        "clientes_referencia": len(referencia),
        "media_test": round(test.mean(), 2),
        "media_referencia": round(referencia.mean(), 2),
        "diferencia": round(test.mean() - referencia.mean(), 2),
        "t": round(estadistico, 2),
        "p_valor": formato_p(p_valor),
        "decision": decision(p_valor, alfa),
    }


def contraste_por_categoria(df, categoria, variable, alfa, orden, sumar=0, multiplicar=1, una_cola=False):
    """Repite contraste_medias dentro de cada categoría (tramo de edad, mes, periodo...).

    Para cada valor de la lista orden se queda con las filas de esa categoría y
    compara la variable del Test con la del Control. La referencia es
    Control x multiplicar + sumar (por defecto, el Control tal cual).
    Devuelve una tabla con una fila por categoría.
    """
    resultados = []
    for valor in orden:
        parte = df[df[categoria] == valor]
        test = parte.loc[parte["grupo"] == "Test", variable]
        control = parte.loc[parte["grupo"] == "Control", variable]
        resultados.append(contraste_medias(test, control * multiplicar + sumar, alfa, una_cola))
    return pd.DataFrame(resultados, index=orden)


def contraste_variables(df, variables, alfa):
    """Compara la media de varias variables del perfil (edad, saldo...) entre Test y Control.

    Sirve para comprobar si el reparto entre grupos fue aleatorio: si lo fue,
    los dos grupos deberían tener perfiles parecidos. Devuelve una fila por variable.
    """
    resultados = []
    for variable in variables:
        test = df.loc[df["grupo"] == "Test", variable].dropna()
        control = df.loc[df["grupo"] == "Control", variable].dropna()
        resultados.append(contraste_medias(test, control, alfa))
    return pd.DataFrame(resultados, index=variables)


def contraste_chi2(df, filas, columnas, alfa):
    """Chi-cuadrado de independencia entre dos variables categóricas (lección de EDA bivariante).

    H0: las dos variables son independientes (por ejemplo, el grupo no cambia el
    reparto por género). Devuelve la tabla cruzada (pd.crosstab) y un diccionario
    con el estadístico, el p-valor, la decisión y la V de Cramér (fuerza de la
    relación: 0 = ninguna, 1 = total).
    """
    tabla = pd.crosstab(df[filas], df[columnas])
    estadistico, p_valor, _, _ = chi2_contingency(tabla)
    resultado = {
        "chi2": round(estadistico, 2),
        "p_valor": formato_p(p_valor),
        "decision": decision(p_valor, alfa),
        "v_cramer": round(association(tabla, method="cramer"), 3),
    }
    return tabla, resultado
