# Preguntas del proyecto

Esta es la guía de trabajo: cada análisis responde a una de estas preguntas. Se actualiza con lo que van diciendo los datos.

**Estado:** ✅ respondida · 🟡 respuesta parcial o solo descriptiva · ⬜ pendiente
**Dónde:** todo está en `vanguard_analisis.ipynb`: NB01 = Parte 1 (exploración y limpieza), NB02 = Parte 2 (comportamiento), NB03 = Parte 3 (KPI), NB04 = Parte 4 (prueba de hipótesis). Tableau: `05_datos_tableau.ipynb`.

## 0. La pregunta principal

> **¿El nuevo diseño hace que más clientes completen el proceso online, y lo suficiente como para que compense su coste?**

**Primera respuesta (descriptiva):** completa el 69,3 % del Test y el 65,6 % del Control, +3,7 puntos. Que sea suficiente depende de cómo se lea el umbral del 5 % (D5) y de que la diferencia no se deba al reparto desigual en el tiempo (E7).

**Respuesta con contrastes (NB04, días 4 y 5):** sí, el nuevo diseño hace que más clientes completen el proceso, y la diferencia es significativa (H1, p < 0,0001). La mejora es de 3,7 puntos: no llega a 5 puntos (H2a, p = 0,999) y, si el umbral es un 5 % relativo, queda en el límite sin poder afirmarse (H2b, p = 0,16). Además, el nuevo diseño tiene más clientes con errores (H5), sobre todo a partir de los 45 años (H7).

## Lo que ha cambiado con los datos

Al explorar los datos aparecieron cosas que cambian las preguntas iniciales:

1. **El umbral del 5 % decide el resultado (D5).** Con 5 puntos, el Test (69,3 %) no llega al 70,6 % necesario; con un 5 % relativo, sí supera el 68,9 %. Hay que preguntarlo al profesor.
2. **La ventaja del Test baja con el tiempo (E4).** +5,2 puntos en marzo, +2,7 en abril, +2,8 en mayo, +0,5 en junio. Puede ser efecto novedad o que los clientes de junio tuvieron menos días para terminar.
3. **El reparto cambió a mitad del test (E2) y eso puede inflar la ventaja (E7, nueva).** El Test tiene más clientes en marzo y abril, cuando todos completan más. Dentro de cada periodo, la ventaja es de +3,3 (hasta el 7 de mayo) y +1,7 (desde el 8 de mayo).
4. **La hipótesis propia se amplía (H3).** El nuevo diseño no ayuda solo a los mayores: también, y más, a los menores de 30.
5. **Nuevas preguntas de calidad:** los accesos parecen tener un tope en 9 (C11) y el Test hace más clics por cliente (K8).
6. **El nuevo diseño tiene más errores (K4, día 3).** Más clientes terminan y más rápido, pero el Test vuelve atrás más veces: 9,2 % de los pasos frente a 6,7 %. El error que más crece es volver de `step_1` a `start`, desde el mismo paso en el que el Test tarda más (K3). Además, en el Test los errores suben con la edad (K9). La recomendación ya no es solo «lanzar o no»: hay que revisar `step_1`.
7. **Los contrastes confirman la ventaja, pero no el umbral (días 4 y 5).** La diferencia en la tasa de finalización es significativa (H1), pero no se puede afirmar que llegue al 5 % con ninguna de las dos lecturas (H2). Desde el 8 de mayo la ventaja (+1,7) deja de ser significativa, y en junio también (H6). El experimento comparó grupos con el mismo perfil (H4), pero el reparto no fue 50/50 (E1) ni igual en el tiempo (E2).

## 1. Definiciones

| # | Pregunta | Decisión | Estado |
|---|---|---|---|
| D1 | ¿Qué es «completar»? | Llegar a `confirm` al menos una vez; tasa sobre todos los clientes del grupo | ✅ |
| D2 | ¿Unidad de análisis? | El cliente para las tasas; la visita de cada cliente para tiempos y errores | ✅ |
| D3 | ¿Qué cuenta como error? | Cada paso hacia atrás dentro de una visita (enunciado). Sin contar volver a empezar tras `confirm`, la conclusión no cambia (9,2 % frente a 6,4 %) | ✅ NB03 |
| D4 | ¿Cómo se mide el tiempo de un paso? | Diferencia entre un clic y el siguiente en la misma visita; se quitan los tiempos de más de 30 minutos (0,11 % de los clics, límite en `config.py`); se usa la mediana | ✅ NB03 |
| D5 | El umbral del 5 %: ¿5 puntos o un 5 % relativo? | Control 65,6 % → 70,6 % (5 puntos) o 68,9 % (5 % relativo). El Test (69,3 %) solo supera el segundo, y no de forma significativa. Calculadas las dos lecturas (H2): ninguna se puede afirmar. Falta confirmar con el profesor cuál vale | 🟡 NB04 |
| D6 | ¿Qué hacer con los clientes sin `start` (424) o con `confirm` sin `step_3` (347)? | Se mantienen y se marcan. Sin ellos: 69,0 % frente a 65,4 %, la conclusión no cambia | ✅ NB01 |

## 2. Calidad de los datos

| # | Pregunta | Respuesta | Estado |
|---|---|---|---|
| C1 | ¿Todos los clientes tienen grupo? | No: 20.109 sin grupo, fuera del análisis | ✅ NB01 |
| C2 | ¿Hay filas repetidas? | 10.764 clics repetidos, eliminados | ✅ NB01 |
| C3 | ¿Hay nulos? | 14 perfiles vacíos, eliminados | ✅ NB01 |
| C4 | ¿Las fechas están dentro del test? | Sí: del 15/3 al 20/6/2017 | ✅ NB01 |
| C5 | ¿Antigüedad en años y en meses cuadra? | Sí: los meses sobran y se eliminan | ✅ NB01 |
| C6 | ¿Llamadas y accesos son distintas? | No: en el 97 % de los clientes, accesos = llamadas + 3. Se eliminan las llamadas | ✅ NB01 |
| C7 | ¿Dispositivos o visitas compartidos? | 360 y 242. Se analiza siempre por cliente | ✅ NB01 |
| C8 | ¿Pasos con la misma hora? | 528. Se ordenan por número de paso | ✅ NB01 |
| C9 | ¿Valores extraños? | 62 menores de 18, saldos de hasta 16 millones, 2 «Otro»: se mantienen | ✅ NB01 |
| C10 | ¿Cuánto falta en género? | 34 % desconocido: límite para cualquier análisis por género | ✅ NB01 |
| C11 | **Nueva:** ¿los accesos tienen un tope? | El 24,5 % de los clientes tiene exactamente 9 accesos, el máximo: probablemente 9 significa «9 o más» | 🟡 NB02, citar como limitación |
| C12 | ¿Hay espacios sobrantes en los textos? | No (0 celdas) | ✅ NB01 |

## 3. Quiénes son los clientes

| # | Pregunta | Respuesta | Estado |
|---|---|---|---|
| P1 | ¿Qué edad tienen? | Mediana de 48 años; el 56 % tiene 45 o más | ✅ NB01 |
| P2 | ¿Nuevos o antiguos? | Antiguos: mediana de 11 años; el 92 % lleva 5 o más | ✅ NB01 |
| P3 | ¿Saldo y cuentas? | Saldo mediano de 66.000 USD (muy desigual); el 79 % tiene 2 cuentas | ✅ NB01 |
| P4 | ¿Género? | Hombre 34 %, Mujer 32 %, Desconocido 34 % | ✅ NB01 |
| P5 | ¿Usan el canal digital? | Mediana de 6 accesos en seis meses | ✅ NB01 |

## 4. Cómo se comportan

| # | Pregunta | Respuesta | Estado |
|---|---|---|---|
| B1 | ¿Cuántas visitas hacen? | El 74 % hace una sola | ✅ NB01 |
| B2 | ¿Dónde se pierden más? | En `start`: el 14 % del Control no pasa de ahí, frente al 9 % del Test. En los demás pasos los grupos se parecen | ✅ NB01 |
| B3 | ¿Los mayores se comportan distinto? | Hacen más visitas y completan menos (63 % los de 60+ frente a 71 % los menores de 30) | ✅ NB01 |
| B4 | ¿Quien usa más la web completa más? | Un poco (de 63-66 % a 67-72 %). El Test gana en todos los niveles | ✅ NB02 |
| B5 | ¿Influyen el saldo o la antigüedad? | Apenas. El Test gana en todos los cuartiles de saldo (+3,6 a +3,8) | ✅ NB02 |
| B6 | ¿Cuándo se usa el proceso? | Abril (57 % de los clics), los miércoles y a las 11; los 4 días con más clics son miércoles seguidos | ✅ NB02 |
| B6b | **Nueva:** ¿los que llegan un miércoles se comportan distinto? | Completan más (71-75 % frente a 63-66 %), pero la ventaja del Test es la misma (+3,9 frente a +3,6): la campaña, si existió, no favorece a un grupo | ✅ |
| B7 | ¿Volver es abandonar? | No: quien vuelve otro día completa más (73 %) | ✅ NB02 |
| B8 | ¿Los dos grupos siguen el mismo recorrido? | El recorrido perfecto pesa igual (29 % y 28 % de las visitas). El Test se queda menos en `start` (8 % frente a 16 %) pero añade idas y vueltas entre `start` y `step_1` | ✅ NB03, bonus |
| B9 | ¿Hay comportamientos extremos? | 571 clientes con más de 20 clics; el 76 % completa. Más en el Test (349 frente a 222), coherente con sus más errores (K4) | ✅ NB02, NB03 |
| B10 | ¿Influye el género? | Las mujeres completan unos 3 puntos menos en los dos grupos; el nuevo diseño no cambia esa diferencia | ✅ NB02 |

## 5. Resultado del test: KPI (día 3)

| # | Pregunta | Lo que sabemos | Estado |
|---|---|---|---|
| K1 | ¿Qué grupo completa más? | Test 69,3 %, Control 65,6 %; diferencia significativa (H1) | ✅ NB03, NB04 |
| K2 | ¿En qué paso gana el nuevo diseño? | Embudo: el Test va por delante desde `step_1` (+4,4 puntos) y la ventaja se mantiene hasta `confirm` (+3,7) | ✅ NB03 |
| K3 | ¿Cuánto se tarda en cada paso? | Medianas Control / Test: `start` 20 / 14 s, `step_1` 20 / **27 s**, `step_2` 64 / 61 s, `step_3` 72 / 57 s. El Test es más rápido salvo en `step_1` | ✅ NB03 (descriptivo) |
| K4 | ¿Qué grupo vuelve más atrás (errores)? | **El Test:** 9,2 % de los pasos frente a 6,7 %; 33 % de los clientes con algún error frente a 26 %. El que más crece: de `step_1` a `start` (6.372 frente a 2.483) | ✅ NB03, NB04 (H5) |
| K5 | ¿Cuánto se tarda en completar el proceso entero? | Mediana 4,7 min en el Test y 5,4 en el Control; terminan en menos de 30 min el 83,7 % y el 82,4 % | ✅ NB03 |
| K6 | ¿Cuántas visitas hacen falta para completar? | Parcial: quien vuelve otro día completa el 73 % (B7) | ⬜ opcional |
| K7 | ¿El resultado es igual para todas las edades? | No: +6,8 en menores de 30, +4,8 en 60+, +2,8 en 30-44, +1,8 en 45-59 | ✅ NB02, NB04 (H3) |
| K8 | **Nueva:** ¿el nuevo diseño provoca más clics o más vueltas? | Más vueltas: los clics de más del Test son sobre todo pasos hacia atrás (K4), no pasos nuevos | ✅ NB03 |
| K9 | **Nueva:** ¿los errores cambian con la edad? | En el Control, 23-28 % de clientes con error en todas las edades; en el Test sube de 29 % (<30) a 39 % (60+). Diferencia de 10-11 puntos desde los 45 años | ✅ NB03, NB04 (H7) |

## 6. Contrastes de hipótesis (días 4 y 5)

Todos con α = 0,05 (`config.ALFA`) y con las herramientas de la lección: t de Welch (`st.ttest_ind` con `equal_var=False`), chi-cuadrado (`st.chi2_contingency`) y binomial (`st.binom`). Las tasas se comparan como medias de una columna de 0 y 100 por cliente.

| # | Hipótesis | Contraste | Resultado | Estado |
|---|---|---|---|---|
| H1 | La tasa de finalización del Test es distinta de la del Control | t de Welch (a mano y con `scipy`) y chi-cuadrado | +3,7 puntos, t = 8,88, p < 0,0001; V de Cramér 0,04 (efecto pequeño). Por periodo: +3,3 hasta el 7 de mayo (significativa), +1,7 desde el 8 de mayo (p = 0,11) | ✅ NB04 |
| H2 | La mejora supera el umbral del 5 % | t de Welch de una cola, con el Control + 5 puntos (a) o × 1,05 (b) | a) p = 0,999; b) p = 0,16. Mejora observada: 3,7 puntos (5,7 % relativo) | ✅ NB04: no se puede afirmar con ninguna lectura |
| H3 | La ventaja del nuevo diseño cambia según la edad | t de Welch por tramo | +6,8 (<30), +2,8 (30-44), +1,8 (45-59, p = 0,016), +4,8 (60+): significativa en todos | ✅ NB04 |
| H4 | Los dos grupos tienen el mismo perfil | t de Welch por variable y chi-cuadrado para el género | Antigüedad, saldo y género iguales; edad, cuentas y accesos con diferencias significativas pero diminutas (0,3 años, 0,01 cuentas, 0,06 accesos) | ✅ NB04 (4.6 y, para la edad, también 4A.4, la hipótesis de Emanuel): grupos equivalentes |
| H5 | El % de clientes con algún error es distinto entre grupos | t de Welch y chi-cuadrado | 33,4 % frente a 25,8 %, t = 18,7, p < 0,0001 | ✅ NB04 |
| H6 | La ventaja del Test se mantiene en el tiempo | t de Welch por mes de inicio | +5,2 (marzo), +2,7 (abril), +2,8 (mayo) significativas; +0,5 en junio (p = 0,77) | ✅ NB04: la ventaja baja |
| H7 | El nuevo diseño provoca más errores en los clientes mayores | t de Welch por tramo | +2,9 (<30), +4,7 (30-44), +10,1 (45-59), +11,0 (60+): significativa en todos y creciente con la edad | ✅ NB04 |
| H8 | **Nueva:** el tiempo en cada paso es distinto entre grupos | t de Welch sobre el logaritmo del tiempo (`np.log1p`), por paso | Test más rápido en `start`, `step_2` y `step_3`; más lento en `step_1`. Orientativo: la unidad es el clic | ✅ NB04 |
| H9 | **Bonus:** el número de clics por cliente es distinto | t de Welch | 6,55 frente a 5,97 de media, p < 0,0001; misma mediana (5): son vueltas atrás | ✅ NB04 |
| Bonus | Tamaño del efecto y potencia | No visto en clase (análisis de potencia, intervalos de confianza) | Solo la V de Cramér como medida de tamaño | ⬜ |

## 7. ¿Estaba bien hecho el experimento?

| # | Pregunta | Lo que sabemos | Estado |
|---|---|---|---|
| E1 | ¿Grupos del mismo tamaño? | No: Test 53,4 %, Control 46,6 %. Contraste binomial (H0: 50/50): p < 0,0001 | ✅ NB04 |
| E2 | ¿El reparto fue igual en el tiempo? | No: Test 53-58 % hasta el 1 de mayo, 44-49 % desde el 8 de mayo. Chi-cuadrado semana de inicio × grupo: p < 0,0001 | ✅ NB02, NB04 |
| E3 | ¿Grupos parecidos en perfil? | Sí: diferencias nulas o diminutas (H4) | ✅ NB04 |
| E4 | ¿Tres meses es suficiente? ¿Efecto novedad? | La ventaja baja: +5,2 (marzo), +2,7 (abril), +2,8 (mayo), +0,5 (junio). Los clientes de junio, además, tuvieron menos días para terminar (todos completan menos: 55 %). En junio la ventaja no es significativa (H6). Tres meses bastan para el tamaño de la muestra (el error típico de la diferencia es de solo 0,42 puntos), pero no para saber si la mejora dura | ✅ NB04 |
| E5 | ¿El pico de abril puede sesgar? | Ver E7 | ✅ NB04 |
| E6 | ¿Qué sesgos puede haber? | Reparto desigual en el tiempo (E2, E7), clientes de junio con menos tiempo (E4), dispositivos compartidos (C7), registros incompletos (D6), posible campaña los miércoles (B6b) y 34 % de género desconocido (C10) | ✅ NB04, sección 4.6 |
| E7 | **Nueva:** ¿el reparto desigual infla la ventaja del Test? | Posiblemente: el Test pesa más en marzo y abril, cuando todos completan más. Dentro de cada periodo la ventaja es menor: +3,3 hasta el 7 de mayo (significativa), +1,7 después (no significativa). La conclusión de H1 se mantiene, pero la ventaja real puede ser algo menor que 3,7 | ✅ NB04 |

## 8. Qué datos faltarían

| # | Pregunta |
|---|---|
| F1 | ¿Qué trámite es exactamente el proceso? |
| F2 | ¿Qué dispositivo usaba el cliente: móvil u ordenador? |
| F3 | ¿Hay mensajes de error del sistema, o solo sabemos que vuelven atrás? |
| F4 | ¿Qué hicieron los que abandonaron: llamaron, volvieron otro día? |
| F5 | ¿Cuánto costó el nuevo diseño y cuánto vale cada proceso completado? |
| F6 | **Nueva:** ¿hubo campañas (emails, avisos) los miércoles? ¿A qué clientes llegaron? |
| F7 | **Nueva:** ¿por qué cambió el reparto entre grupos el 8 de mayo? |
| F8 | **Nueva:** ¿los accesos de 9 son «9 o más»? |

## 9. Qué recomendar a Vanguard (semana 6)

| # | Pregunta | Pista que ya tenemos |
|---|---|---|
| R1 | ¿Se lanza el nuevo diseño? | Mejora real (H1) pero por debajo del umbral de 5 puntos y en el límite del 5 % relativo (H2). Va en la buena dirección; antes de lanzarlo, revisar `step_1` y confirmar el umbral con Vanguard |
| R2 | ¿Qué paso mejorar primero? | `step_1` del nuevo diseño: es más lento que en el Control (K3) y desde ahí vuelven a `start` 2,6 veces más (K4) |
| R3 | ¿Algún grupo necesita ayuda extra? | Los de 60+: completan menos y en el nuevo diseño vuelven atrás más (39 %), aunque el diseño les ayuda a terminar |
| R4 | ¿Qué medir en un próximo test? | Reparto 50/50 constante, misma duración para todos los clientes, dispositivo y campañas |
| R5 | **Nueva:** ¿recordar el proceso a quien no termina? | Quien vuelve otro día completa más (B7). Es una propuesta, no un resultado probado |
