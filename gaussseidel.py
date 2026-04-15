"""
Método de Gauss-Seidel
Castillo Cruz Sofia
"""

import streamlit as st
import numpy as np
import pandas as pd
from math import isclose

# -------------------------------------------------
# COLORES Y ESTILOS DE LA PAGINA
# -------------------------------------------------
COLOR_FONDO = "#344e41"
COLOR_TARJETA = "#a3b18a"
COLOR_BOTON = "#588157"
COLOR_TEXTO = "#a3b18a"
COLOR_ALERTA_ERROR = "#8B1E1E"   
RADIO_BORDES = "10px"

# Configuración de la página
st.set_page_config(page_title="Método de Gauss-Seidel", layout="centered")

# ----------------
# CSS
# ----------------
st.markdown(f"""
<style>
body {{
  background-color: {COLOR_FONDO};
  color: {COLOR_TEXTO};
  font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}
.stApp {{ background-color: {COLOR_FONDO}; }}
h1, h2, h3 {{
  color: {COLOR_TEXTO};
  text-align:center;
}}
.tarjeta {{
  background-color: {COLOR_TARJETA};
  padding: 16px;
  border-radius: {RADIO_BORDES};
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  margin-bottom: 16px;
}}
div[data-testid="stNumberInput"] input {{
  text-align:center;
  color: white !important;
  background-color: {COLOR_TARJETA};
  border-radius: 6px;
  font-size: 16px !important;
  font-weight: 600;
}}
.stButton>button {{
  background-color: {COLOR_BOTON};
  border-radius: 8px;
  height:40px;
  border: 1px solid;
  color: white;
  font-weight: 600;
}}
.contenedor-tabla {{
  display: flex;
  justify-content: center;
  background-color: {COLOR_TARJETA};
  padding:8px;
  border-radius:8px;
}}
.texto-comprobacion {{
  color: white;
  font-size: 17px;
  font-weight: 600;
}}
.texto-iteraciones {{
  text-align:center;
  font-weight:700;
  color:{COLOR_TEXTO};
  font-size:22px;
  margin-top:10px;
}}
.tarjeta-error {{
  background-color: {COLOR_ALERTA_ERROR};
  padding: 12px;
  border-radius: 8px;
  color: white;
  font-weight: 700;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------
def formato_numero(valor, decimales_max=6):
    try:
        numero = float(valor)
    except Exception:
        return str(valor)
    if isclose(numero, round(numero), rel_tol=0, abs_tol=1e-12):
        return str(int(round(numero)))
    else:
        texto = f"{numero:.{decimales_max}f}".rstrip("0").rstrip(".")
        return texto

def convertir_tabla_html(tabla):
    copia = tabla.copy()
    for columna in copia.columns:
        copia[columna] = copia[columna].apply(formato_numero)
    return copia.to_html(index=False)

# -------------------------------------------------
# ENCABEZADO
# -------------------------------------------------
st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
st.title("Método de Gauss-Seidel")
st.markdown("<div style='text-align:center;'>Castillo Cruz Sofia — 24212705 — SC4A</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# INGRESO DE LOS COEFICIENTES
# -------------------------------------------------
st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
st.subheader("Ingrese los coeficientes del sistema (3×3)")

valores_iniciales_coeficientes = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
valores_iniciales_resultados = [6, 25, 11]
lista_ecuaciones = []

for i in range(3):
    columnas = st.columns([0.9, 1, 1, 1, 0.25, 1])
    with columnas[0]:
        st.markdown(f"<div style='font-weight:700;'>Ecuación {i+1}</div>", unsafe_allow_html=True)
    with columnas[1]:
        c1 = st.number_input("", value=float(valores_iniciales_coeficientes[i][0]), format="%f", key=f"c_{i}_1")
    with columnas[2]:
        c2 = st.number_input("", value=float(valores_iniciales_coeficientes[i][1]), format="%f", key=f"c_{i}_2")
    with columnas[3]:
        c3 = st.number_input("", value=float(valores_iniciales_coeficientes[i][2]), format="%f", key=f"c_{i}_3")
    with columnas[4]:
        st.markdown("<div style='text-align:center;'> = </div>", unsafe_allow_html=True)
    with columnas[5]:
        b = st.number_input("", value=float(valores_iniciales_resultados[i]), format="%f", key=f"b_{i}")
    lista_ecuaciones.append((c1, c2, c3, b))

st.markdown("</div>", unsafe_allow_html=True)

matriz_coeficientes = np.array([[e[0], e[1], e[2]] for e in lista_ecuaciones], dtype=float)
vector_resultados = np.array([e[3] for e in lista_ecuaciones], dtype=float)

# -------------------------------------------------
# MATRIZ AMPLIADA
# -------------------------------------------------
st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Matriz ampliada [A | b]</h3>", unsafe_allow_html=True)
tabla_ampliada = pd.DataFrame(np.hstack([matriz_coeficientes, vector_resultados.reshape(3,1)]),
                              columns=["a1", "a2", "a3", "b"])
st.markdown(f"<div class='contenedor-tabla'>{convertir_tabla_html(tabla_ampliada)}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# ECUACIONES DESPEJADAS
# -------------------------------------------------
st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
st.subheader("Ecuaciones despejadas")
st.markdown(f"""
<div style='font-weight:700;'>x1 = ({formato_numero(vector_resultados[0])} - ({formato_numero(matriz_coeficientes[0,1])}·x2) - ({formato_numero(matriz_coeficientes[0,2])}·x3)) / {formato_numero(matriz_coeficientes[0,0])}</div>
<div style='font-weight:700;'>x2 = ({formato_numero(vector_resultados[1])} - ({formato_numero(matriz_coeficientes[1,0])}·x1) - ({formato_numero(matriz_coeficientes[1,2])}·x3)) / {formato_numero(matriz_coeficientes[1,1])}</div>
<div style='font-weight:700;'>x3 = ({formato_numero(vector_resultados[2])} - ({formato_numero(matriz_coeficientes[2,0])}·x1) - ({formato_numero(matriz_coeficientes[2,1])}·x2)) / {formato_numero(matriz_coeficientes[2,2])}</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# VERIFICACIÓN DE DIAGONAL DOMINANTE
# -------------------------------------------------
st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
st.subheader("Verificación de Diagonal Dominante")

cumple_diagonal = True
mensajes = []
for i in range(3):
    suma = sum(abs(matriz_coeficientes[i, j]) for j in range(3) if j != i)
    if abs(matriz_coeficientes[i, i]) <= suma:
        cumple_diagonal = False
        mensajes.append(f"La ecuación {i+1} NO cumple diagonal dominante")
    else:
        mensajes.append(f"La ecuación {i+1} cumple diagonal dominante")

if cumple_diagonal:
    st.markdown(f"<div class='tarjeta' style='text-align:center;'><strong> El sistema cumple la condición de diagonal dominante.</strong></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='tarjeta-error' style='text-align:center;'> El sistema NO cumple la condición de diagonal dominante. El método puede no converger.</div>", unsafe_allow_html=True)

for linea in mensajes:
    st.write("- " + linea)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# VARIABLES DE SESIÓN
# -------------------------------------------------
if "solucion_actual" not in st.session_state:
    st.session_state.solucion_actual = np.zeros(3)
if "historial_iteraciones" not in st.session_state:
    st.session_state.historial_iteraciones = []
if "numero_iteracion" not in st.session_state:
    st.session_state.numero_iteracion = 0

# -------------------------------------------------
# BOTÓN
# -------------------------------------------------
st.markdown("<div class='tarjeta' style='text-align:center;'>", unsafe_allow_html=True)
boton_iniciar = st.button("Iniciar / Ejecutar iteración")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# FUNCIÓN DE ITERACIÓN GAUSS-SEIDEL
# -------------------------------------------------
def realizar_iteracion_gauss_seidel(matriz, vector):
    anterior = st.session_state.solucion_actual.copy().astype(float)
    nueva = anterior.copy()
    nueva[0] = (vector[0] - matriz[0,1]*nueva[1] - matriz[0,2]*nueva[2]) / matriz[0,0] if matriz[0,0] != 0 else nueva[0]
    nueva[1] = (vector[1] - matriz[1,0]*nueva[0] - matriz[1,2]*nueva[2]) / matriz[1,1] if matriz[1,1] != 0 else nueva[1]
    nueva[2] = (vector[2] - matriz[2,0]*nueva[0] - matriz[2,1]*nueva[1]) / matriz[2,2] if matriz[2,2] != 0 else nueva[2]
    return nueva

# -------------------------------------------------
# CÁLCULO AUTOMÁTICO
# -------------------------------------------------
if boton_iniciar:
    st.session_state.solucion_actual = np.zeros(3)
    st.session_state.historial_iteraciones = []
    st.session_state.numero_iteracion = 0

    max_iter = 50
    error_limite = 0.1
    continuar = True

    while continuar and st.session_state.numero_iteracion < max_iter:
        anterior = st.session_state.solucion_actual.copy()
        nueva = realizar_iteracion_gauss_seidel(matriz_coeficientes, vector_resultados)
        errores = np.abs(nueva - anterior)

        st.session_state.numero_iteracion += 1
        st.session_state.historial_iteraciones.append({
            "Iteración": st.session_state.numero_iteracion,
            "x1": nueva[0], "x2": nueva[1], "x3": nueva[2],
            "Error x1": errores[0], "Error x2": errores[1], "Error x3": errores[2]
        })

        st.session_state.solucion_actual = nueva.copy()
        if all(e <= error_limite for e in errores):
            continuar = False

    # HISTORIAL DE ITERACIONES
    if st.session_state.historial_iteraciones:
        st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
        st.subheader("Historial de iteraciones")
        tabla = pd.DataFrame(st.session_state.historial_iteraciones)
        st.markdown(f"<div class='contenedor-tabla'>{convertir_tabla_html(tabla)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='texto-iteraciones'>Iteraciones realizadas: {st.session_state.numero_iteracion}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # COMPROBACIÓN FINAL
    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.subheader("Comprobación final (sustitución)")
    solucion_final = st.session_state.solucion_actual.copy()
    sustitucion = matriz_coeficientes.dot(solucion_final)
    for i in range(3):
        terminos = [f"({formato_numero(matriz_coeficientes[i,j])}·{formato_numero(solucion_final[j])})" for j in range(3)]
        suma_terminos = " + ".join(terminos)
        obtenido = formato_numero(sustitucion[i])
        esperado = formato_numero(vector_resultados[i])
        error_ec = formato_numero(vector_resultados[i] - sustitucion[i])
        st.markdown(
            f"<div style='background-color:{COLOR_TARJETA}; padding:12px; border-radius:8px; margin-bottom:10px; border:1px solid {COLOR_BOTON};'>"
            f"<div style='font-weight:700; color:white; font-size:18px;'>Ecuación {i+1}:</div>"
            f"<div class='texto-comprobacion'>{suma_terminos} = {obtenido} ≈ {esperado}</div>"
            f"<div class='texto-comprobacion' style='font-size:15px;'>Error ecuación {i+1} = {error_ec}</div>"
            f"</div>", unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f"<div style='text-align:center; color:{COLOR_TEXTO};'>Aún no se han realizado iteraciones. Presione “Iniciar / Ejecutar iteración”.</div>", unsafe_allow_html=True)
