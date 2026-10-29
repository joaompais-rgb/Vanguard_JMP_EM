# Vanguard · test A/B del nuevo proceso online

Proyecto 2 del bootcamp de Data Analytics de Ironhack (semanas 5 y 6).

**Equipo:** João Miguel Pais y Emmanuel Chukwuemeka Amadi Agebi.

**Qué hay en el repositorio:** el análisis completo en Python (`vanguard_analisis.ipynb`), el Tableau de Emmanuel (capturas en `tableau/capturas/` y el libro en el enlace de la sección Tableau) y la presentación (`presentacion/`).

**Pregunta:** ¿el nuevo diseño del proceso online (grupo Test) hace que más clientes completen el proceso que el diseño antiguo (grupo Control)?

El test se hizo del 15/3/2017 al 20/6/2017. Los dos grupos pasan por los mismos pasos: `start`, `step_1`, `step_2`, `step_3` y `confirm`.

## Preguntas

Todo el trabajo parte de [preguntas.md](preguntas.md): definiciones, calidad de datos, perfil y comportamiento de los clientes, KPI, contrastes, evaluación del experimento y recomendaciones.

## Datos

Fuente: [data-bootcamp-v4/lessons · files_for_project](https://github.com/data-bootcamp-v4/lessons/tree/main/5_6_eda_inf_stats_tableau/project/files_for_project)

| Archivo | Contenido | Filas |
|---|---|---|
| `df_final_experiment_clients.txt` | Grupo de cada cliente (Test o Control) | 70.609 (50.500 con grupo) |
| `df_final_demo.txt` | Perfil: edad, género, antigüedad, cuentas, saldo, llamadas y accesos | 70.609 |
| `df_final_web_data_pt_1.zip` y `pt_2` | Cada clic: cliente, visita, paso y hora (el `.txt` original, comprimido en `.zip` porque pasa de 25 MB; pandas lo lee sin descomprimir) | 755.405 en total |

## Limpieza (Parte 1)

Trece problemas de calidad, cada uno con su decisión y su justificación (tabla en la Parte 1, sección 1.4). Los principales:

- Solo los clientes con grupo; sin las 14 filas vacías del perfil → **50.488 clientes** (Test 26.961, Control 23.527).
- Datos web: `pd.concat` de las dos partes, sin las 10.764 filas repetidas, `date_time` como fecha, `paso_num` para ordenar los pasos y solo clientes del test → **317.135 clics**.
- Columnas repetidas fuera: `clnt_tenure_mnth` (repite los años) y `calls_6_mnth` (en el 97 % de los clientes es accesos menos 3).
- Columnas renombradas y género en texto (Hombre, Mujer, Desconocido, Otro).
- Valores del proyecto (rutas, columnas, tramos, pasos, umbrales) en `config.py`, no dentro del código.

## Diccionario de las tablas limpias (`data/clean/`)

| Tabla | Columna | Descripción |
|---|---|---|
| `clientes.csv` | `client_id` | Identificador del cliente |
| | `grupo` | Test (nuevo diseño) o Control (diseño antiguo) |
| | `antiguedad_anos` | Años como cliente de Vanguard |
| | `edad` | Edad en años |
| | `genero` | Hombre, Mujer, Desconocido u Otro |
| | `num_cuentas` | Número de cuentas |
| | `saldo` | Saldo total en USD |
| | `accesos_6m` | Accesos a la web en los últimos 6 meses |
| `web.csv` | `client_id`, `visitor_id`, `visit_id` | Cliente, dispositivo y visita |
| | `process_step` | Paso: start, step_1, step_2, step_3, confirm |
| | `paso_num` | Número del paso (0 a 4) |
| | `date_time` | Fecha y hora del clic |

## Primeros resultados (días 1 y 2)

- Clientes de mediana edad (mediana 48 años) y antiguos (mediana 11 años en Vanguard; el 92 % lleva 5 años o más).
- Saldo muy desigual: mediana de 66.000 USD frente a una media de 149.000.
- Un 34 % de los clientes no tiene género registrado (`U` en el original, «Desconocido» en la tabla limpia).
- Descriptivo, sin contraste todavía: completa el proceso el 69,3 % del grupo Test y el 65,6 % del Control. La mayor diferencia está en el primer paso: el 14 % del Control no pasa de `start`, frente al 9 % del Test.
- Los clientes de 60 o más completan menos (62,9 %).

## Comportamiento (Parte 2)

- La ventaja del nuevo diseño aparece en todos los tipos de cliente: por saldo, uso de la web, edad y género.
- Ayuda más a los menores de 30 (+6,8 puntos) y a los de 60 o más (+4,8): base de la hipótesis propia.
- Volver otro día no es abandonar: quien vuelve completa el 73 %.
- Uso concentrado en abril y en los miércoles a las 11 (posible campaña semanal).
- El reparto entre grupos cambió a mitad del test: Test 53-58 % hasta el 1 de mayo, 44-49 % después.
- La ventaja del Test baja con el tiempo (+5,2 puntos en marzo, +0,5 en junio) y dentro de cada periodo es menor que la total (+3,3 y +1,7): parte puede venir del reparto desigual. Se tendrá en cuenta en los contrastes.
- El umbral del 5 % decide el resultado: con 5 puntos el Test no llega (70,6 % necesario); con un 5 % relativo sí (68,9 %), aunque por poco. Se contrasta en la Parte 4.

## KPI (Parte 3)

| KPI | Control | Test | Mejor |
|---|---|---|---|
| Tasa de finalización (llega a `confirm`) | 65,6 % | 69,3 % | Test (+3,7 puntos) |
| Tiempo en cada paso (mediana) | 20 / 20 / 64 / 72 s | 14 / 27 / 61 / 57 s | Test, salvo en `step_1` |
| Tasa de errores (pasos hacia atrás / pasos) | 6,7 % | 9,2 % | Control |
| Clientes con algún error | 26 % | 33 % | Control |
| Tiempo total para completar (mediana) | 5,4 min | 4,7 min | Test |

- El nuevo diseño hace que más clientes terminen y más rápido, pero con más vueltas atrás.
- El error que más crece en el Test es volver de `step_1` a `start` (2,6 veces más que en el Control). `step_1` es también el único paso más lento: es la pantalla a revisar.
- En el Test los errores suben con la edad (39 % de los mayores de 60 tiene algún error); en el Control no.
- Recorridos (bonus, sección 3.5b): el recorrido perfecto (los cinco pasos sin volver atrás) pesa lo mismo en los dos grupos (29 % y 28 % de las visitas). El nuevo diseño hace que menos visitas se queden paradas en `start` (8 % frente a 16 %), pero añade un recorrido de ida y vuelta entre `start` y `step_1`.
- Todo es descriptivo: la significación se comprueba en la Parte 4.
- Funciones en `src/kpis.py`; resultados para Tableau en `data/clean/kpis_resumen.csv` y `data/clean/pasos_kpis.csv`.

## Contrastes y evaluación del experimento (Parte 4)

La Parte 4 une dos trabajos. La **4A** es la base de Emmanuel (`Prueba-de-hipotesis.ipynb`, última versión del 20 de octubre: H1 con un z de proporciones, H2 con el umbral del 5 %, una hipótesis sobre la edad media de los dos grupos y una primera evaluación), con su texto y su código tal cual y, al lado, el mismo cálculo con lo visto en clase. En la hipótesis de la edad faltaba el contraste: lo terminamos con la t de Welch (significativo, p = 0,016, pero la diferencia es de 0,33 años: en la práctica, la misma edad). La **4B** es lo que añadimos y por qué.

Todos con α = 0,05 y con las herramientas de la lección de contrastes de hipótesis: t de Welch (`st.ttest_ind`), chi-cuadrado (`st.chi2_contingency`) y binomial (`st.binom`).

| # | Hipótesis | Resultado |
|---|---|---|
| H1 | La tasa de finalización es distinta entre grupos | ✅ Sí: +3,7 puntos, p < 0,0001. Desde el 8 de mayo la ventaja (+1,7) no es significativa |
| H2 | La mejora llega al umbral del 5 % | ❌ No se puede afirmar: la mejora es de 3,7 puntos. Con 5 puntos, p = 0,999; con un 5 % relativo, p = 0,16 |
| H5 | El nuevo diseño tiene más clientes con errores | ✅ Sí: 33,4 % frente a 25,8 % |
| H3 / H7 | La edad cambia el efecto | La ventaja existe en todas las edades (más en <30 y 60+); los errores de más del Test crecen con la edad (+10 a +11 puntos desde los 45) |
| H6 | La ventaja se mantiene en el tiempo | Baja: +5,2 en marzo, +0,5 en junio (no significativa) |
| H8 | El tiempo por paso es distinto | El Test es más rápido salvo en `step_1` |
| H9 (bonus) | El número de clics por cliente es distinto | ✅ Sí: 6,55 frente a 5,97 de media (p < 0,0001), con la misma mediana (5): son vueltas atrás, no pasos nuevos |
| E1 / E2 / E3 | ¿Experimento bien diseñado? | Grupos con el mismo perfil, pero reparto no 50/50 (53,4 % Test) y distinto en el tiempo (cambio el 8 de mayo) |

**Conclusión:** el nuevo diseño mejora la tasa de finalización de forma real, pero no alcanza el umbral de 5 puntos que justificaría su coste y queda en el límite si el umbral es un 5 % relativo. Además provoca más errores, sobre todo en los clientes mayores y en `step_1`. Funciones en `src/contrastes.py`.

## Tableau (hecho por Emmanuel)

El libro de Tableau de Emmanuel (`Tableau_Vanguard.twbx`) es un libro empaquetado: lleva los datos dentro, así que se abre con Tableau Desktop o Tableau Public sin ejecutar nada antes. Pesa 29 MB, más de lo que deja subir la web de GitHub, así que está en este enlace: **[Tableau_Vanguard.twbx](ENLACE_TABLEAU)**. En `tableau/capturas/` están las imágenes de las hojas que usamos en la presentación. Se construyó con las tablas limpias del análisis (`clientes.csv`, `web.csv` y `pasos_kpis.csv` de `data/clean/`).

| Hoja | Qué muestra | Cómo se calcula |
|---|---|---|
| Sheet 8 (embudo) | Clientes que llegan a cada paso, por grupo | Recuento de clientes por `process_step` y grupo |
| Tasa de finalización | Control 65,96 %, Test 70,04 % | `COUNTD(IF [process_step] = "confirm" THEN [client_id] END) / COUNTD(IF [process_step] = "start" THEN [client_id] END)` |
| Porcentaje de errores | Control 6,75 %, Test 9,16 % | `SUM(IF [es_error] = TRUE THEN 1 ELSE 0 END) / COUNT([es_error])`, la misma fórmula del KPI 3 |
| Tramos edad | Clientes por tramo de edad y grupo | `IF INT([edad]) < 30 THEN "Menores de 30" ELSEIF ...`, los mismos tramos del notebook; `COUNTD([client_id])` |
| Género | Clientes por género y grupo | `COUNTD([client_id])` |
| Minutos hasta confirm, Cantidad de pasos para finalizar, Accesos durante el tiempo | Sumas por grupo | Son sumas: como el Test tiene más clientes, siempre salen más altas. No las usamos en la presentación; para comparar haría falta la mediana o la media por cliente |

En la presentación (diapositiva 19) están el embudo, los tramos de edad, el género, la tasa de finalización y el porcentaje de errores.

**Una diferencia con el notebook:** la tasa de finalización de Tableau divide entre los clientes que llegan a `start`; la del KPI 1, entre todos los clientes del grupo (65,6 % y 69,3 %). La diferencia entre grupos es la misma, unos 4 puntos.

## Cómo ejecutarlo

**Requisitos:** Python 3.10 o más reciente y las librerías de `requirements.txt` (pandas, numpy, matplotlib, seaborn, scipy y jupyter). Probado de principio a fin con Python 3.13 y pandas 3.0 en una carpeta nueva, solo con los datos de `data/raw`.

1. **Datos originales.** Van incluidos en `data/raw/`: los dos `.txt` del perfil y del grupo y las dos partes web en `.zip`. No hace falta descomprimir nada: `pd.read_csv` lee el `.zip` directamente. Si faltan, se descargan de la [fuente](https://github.com/data-bootcamp-v4/lessons/tree/main/5_6_eda_inf_stats_tableau/project/files_for_project) y se guardan ahí (las partes web, comprimidas en `.zip` con el mismo nombre).
2. **Librerías.** En una terminal abierta en la carpeta del proyecto: `pip install -r requirements.txt`.
3. **Abrir la carpeta** `vanguard-ab-test` en VS Code (o lanzar `jupyter notebook` desde ella). Los notebooks se ejecutan desde la carpeta del proyecto: ahí están `config.py` y `src/`, y todas las rutas son relativas a ella (`data/raw` y `data/clean`). No hay ninguna ruta del ordenador escrita en el código.
4. **Ejecutar** con *Restart* y *Run All*:

| Orden | Notebook | Qué hace | Lee | Escribe | Tiempo aproximado |
|---|---|---|---|---|---|
| 1 | `vanguard_analisis.ipynb` | Todo el análisis: Parte 1 (exploración y limpieza), Parte 2 (comportamiento), Parte 3 (KPI) y Parte 4 (prueba de hipótesis: 4A, la base de Emmanuel; 4B, lo que añadimos) | `data/raw/` | `data/clean/` | 1-2 min |

Si la celda de preparación da `ModuleNotFoundError: config`, el notebook no se está ejecutando desde la carpeta del proyecto. Lo más habitual, si se descarga el repositorio como zip («Code › Download ZIP»): abrir el notebook con doble clic **dentro del zip**. Windows solo extrae ese archivo a una carpeta temporal, sin `config.py` ni `src/`. Hay que descomprimir el zip («Extraer todo») y abrir la carpeta `vanguard-ab-test` en VS Code. La primera vez, VS Code pregunta si confías en la carpeta (*Restricted Mode*): hay que aceptar para que se ejecute el código.

Solo se usan herramientas vistas en clase hasta la semana 5; cada bloque «Cómo funciona» dice en qué clase se vio cada herramienta y lo poco que no se vio está marcado. Los gráficos se ven dentro de los notebooks.

## Cómo está explicado el notebook

**`vanguard_analisis.ipynb`** tiene, además de los bloques «Cómo funciona» y «Qué nos llevamos» de cada celda:

- **Al principio:** el resumen con la respuesta, el índice y una guía (en español y en portugués) con nuestras funciones de `src/` y las herramientas de clase, con la lección en la que se vieron.
- **En cada «Cómo funciona»:** una línea «Dónde se vio en clase».
- **Al final de cada sección:** «Por qué lo hicimos así y preguntas posibles», con las respuestas plegadas.
- **En los puntos difíciles:** cuadros «Para entenderlo» con la idea de fondo, en español y en portugués (qué es un test A/B, subgrupos frente a causas, KPI, cómo funciona un contraste, error típico, z o t, significativo frente a importante, no rechazar H0, muchos contrastes, binomial y chi-cuadrado).
- **Al final:** las conclusiones, las recomendaciones y las limitaciones.

## Estructura

```
vanguard-ab-test/
├── data/raw/        datos originales (las dos partes web en .zip)
├── data/clean/      datos limpios (Parte 1) y CSV de los KPI (Parte 3)
├── vanguard_analisis.ipynb      todo el análisis: Partes 1 a 4 y conclusiones
├── tableau/capturas/ imágenes de las hojas del Tableau de Emmanuel (el .twbx, en el enlace)
├── presentacion/    vanguard_presentacion_final_v10.pptx (con notas del orador)
├── config.py        rutas, archivos, columnas, tramos, pasos y umbrales
├── preguntas.md     preguntas que guían el análisis
└── src/             limpieza.py, eda.py, kpis.py y contrastes.py (funciones)
```

## Plan

| Semana | Días | Tarea | Estado |
|---|---|---|---|
| 5 | 1-2 | Exploración, limpieza y perfil de los clientes | hecho |
| 5 | 3 | KPI: tasa de finalización, tiempo por paso, errores | hecho |
| 5 | 4-5 | Contrastes de hipótesis y evaluación del experimento | hecho |
| 6 | 1-2 | Tableau | hecho por Emmanuel: `Tableau_Vanguard.twbx` (enlace en la sección Tableau) |
| 6 | 3-4 | Presentación | hecha: `presentacion/vanguard_presentacion_final_v10.pptx` (João, diapositivas 1 a 11; Emmanuel, de la 12 al final) |

## Enlaces

- Diapositivas: `presentacion/vanguard_presentacion_final_v10.pptx` (enlace de Google Slides: *pendiente*)
- Tableau: [Tableau_Vanguard.twbx](ENLACE_TABLEAU) (se abre con Tableau Desktop o Tableau Public) y capturas en `tableau/capturas/`
