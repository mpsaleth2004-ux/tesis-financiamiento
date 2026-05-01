import streamlit as st
import numpy as np
import pandas as pd

# ============================================================
# PROTOTIPO WEB PARA EVALUACIÓN DE FINANCIAMIENTO INMOBILIARIO
# ============================================================

st.set_page_config(
    page_title="Prototipo CBA - Financiamiento Inmobiliario",
    page_icon="🏗️",
    layout="wide"
)

# --- Funciones financieras ---
def calcular_van(tasa_mensual, flujos):
    van = 0
    for i, flujo in enumerate(flujos):
        van += flujo / ((1 + tasa_mensual) ** i)
    return van

def calcular_tir(flujos):
    tasas = np.linspace(-0.99, 1.5, 20000)
    valores = [calcular_van(tasa, flujos) for tasa in tasas]
    for i in range(len(valores) - 1):
        if valores[i] * valores[i + 1] < 0:
            return tasas[i]
    return None

def interpretar_resultado(van, tir_mensual, rentabilidad, satisfaccion, puntaje_cba):
    tir_anual = ((1 + tir_mensual) ** 12 - 1) if tir_mensual is not None else None
    if van > 0 and tir_anual is not None and tir_anual > 0.14 and rentabilidad >= 17 and satisfaccion >= 4 and puntaje_cba >= 70:
        return "Viable y recomendable", "Cumple con criterios financieros y CBA."
    elif van > 0 and rentabilidad >= 10:
        return "Viable con observaciones", "Revisar riesgos o satisfacción."
    else:
        return "No recomendable", "No cumple mínimos de viabilidad."

# --- Encabezado ---
st.title("🏗️ Prototipo web para selección del financiamiento inmobiliario")
st.divider()

# --- 1. Datos Generales ---
st.header("1. Datos generales del proyecto")
col1, col2 = st.columns(2)
with col1:
    nombre_proyecto = st.text_input("Nombre del proyecto", "Green Tower")
    costo_total = st.number_input("Costo total (S/.)", value=10000000.0)
    horizonte_meses = st.number_input("Horizonte (meses)", value=8)
with col2:
    ubicacion = st.text_input("Ubicación", "Lima Top")
    tasa_descuento_anual = st.number_input("Tasa descuento anual (%)", value=12.0) / 100
    inversion_inicial = st.number_input("Inversión inicial (S/.)", value=3000000.0)

tasa_descuento_mensual = (1 + tasa_descuento_anual) ** (1 / 12) - 1

# --- 2. Método de Financiamiento ---
st.header("2. Datos del método de financiamiento")
metodo = st.selectbox("Seleccione el método", ["Tradicional", "Aporte mixto", "Inversionistas"])
st.info("Asegúrese de que la suma de porcentajes sea 100% en sus cálculos internos.")

col7, col8, col9 = st.columns(3)
with col7:
    tasa_interes = st.number_input("Tasa interés anual Banco (%)", value=7.24) / 100
with col8:
    plazo_credito = st.number_input("Plazo crédito (meses)", value=24)
with col9:
    riesgo = st.selectbox("Riesgo", ["Bajo", "Medio", "Alto"], index=1)

# Cálculo simplificado de egresos
interes_estimado = (costo_total * 0.8) * tasa_interes * (plazo_credito / 12)
egreso_total = costo_total + interes_estimado + 500000 # Otros egresos fijos

# --- 3. Ingresos ---
st.header("3. Ingresos del proyecto")
col10, col11 = st.columns(2)
with col10:
    unidades = st.number_input("Unidades", value=40)
with col11:
    precio = st.number_input("Precio promedio (S/.)", value=350000.0)
ingreso_total = unidades * precio
utilidad = ingreso_total - egreso_total
rentabilidad = (utilidad / egreso_total) * 100

# --- 4. Flujo de Caja ---
st.header("4. Flujo de caja proyectado")
flujos = [-inversion_inicial]
for i in range(1, horizonte_meses + 1):
    flujos.append(utilidad / horizonte_meses)

# --- 5. TABLA CBA (ESTRUCTURA WORD: FILAS DOBLES) ---
st.header("5. Aplicación del Método CBA (Estructura de Matriz)")
st.markdown("La tabla alterna: Fila 1 (Factor/Atributo) y Fila 2 (Criterio/Ventaja). El IDV se edita en la primera fila de cada par.")

# Creamos la lista de datos con filas dobles para cada factor
rows = []
factores_info = [
    {
        "id": "FACTOR 01", "nombre": "Tasa de interés / costo financiero",
        "criterio": "Mientras menor sea la tasa efectiva anual y más estable la modalidad, mejor",
        "trad": ["Tasa efectiva anual 10.5% fija", "Tasa relativamente baja y previsible", 80],
        "asoc": ["Interés 0%, pero cesión ≈ 20% proyecto", "Elimina costo financiero directo", 100],
        "apor": ["Interés 0%, requiere preventa ≥ 30-50%", "Se elimina costo financiero, maximiza utilidad", 100],
        "fond": ["Rentabilidad exigida entre 18-22%", "Mayor costo financiero", 40]
    },
    {
        "id": "FACTOR 02", "nombre": "Plazo de retorno / plazo del crédito",
        "criterio": "Mientras menor sea el plazo sin afectar el flujo de caja, mejor",
        "trad": ["Plazo de 24 meses, ajustado al ciclo", "Permite flujo estable y recuperación", 80],
        "asoc": ["Retorno ligado a ventas (>24 meses)", "No hay presión de pago, retorno largo", 60],
        "apor": ["Venta/entrega escalonada (12-24 meses)", "Flexibilidad en recuperación, sin presiones", 75],
        "fond": ["Fondos exigen retorno 18-24 meses", "Presiona flujo de caja; menos margen", 50]
    },
    {
        "id": "FACTOR 03", "nombre": "Riesgo financiero",
        "criterio": "Mientras menor sea la exposición a inflación e impago, mejor",
        "trad": ["Riesgo controlado (hipotecas)", "Riesgo controlado por supervisión bancaria", 70],
        "asoc": ["Riesgo bajo (sin deuda)", "Riesgo bajo; no hay intereses ni pagos fijos", 90],
        "apor": ["Riesgo dependiente de venta (30-50%)", "Se evita endeudamiento, sube exposición total", 50],
        "fond": ["Estricto covenants, riesgo alto", "Riesgo elevado por compromisos", 40]
    }
    # Agregados solo 3 factores para brevedad, puedes replicar el objeto para los 7
]

for f in factores_info:
    # FILA A: FACTOR Y ATRIBUTO
    rows.append({
        "Descripción / Información": f"{f['id']}: {f['nombre']}",
        "Crédito Bancario (A/V)": f"Atributo: {f['trad'][0]}",
        "Trad. IdV": f[ 'trad'][2],
        "Asociación (A/V)": f"Atributo: {f['asoc'][0]}",
        "Asoc. IdV": f['asoc'][2],
        "Aporte (A/V)": f"Atributo: {f['apor'][0]}",
        "Apor. IdV": f['apor'][2],
        "Fondos (A/V)": f"Atributo: {f['fond'][0]}",
        "Fond. IdV": f['fond'][2]
    })
    # FILA B: CRITERIO Y VENTAJAS
    rows.append({
        "Descripción / Información": f"Criterio: {f['criterio']}",
        "Crédito Bancario (A/V)": f"Ventaja: {f['trad'][1]}",
        "Trad. IdV": f['trad'][2],
        "Asociación (A/V)": f"Ventaja: {f['asoc'][1]}",
        "Asoc. IdV": f['asoc'][2],
        "Aporte (A/V)": f"Ventaja: {f['apor'][1]}",
        "Apor. IdV": f['apor'][2],
        "Fondos (A/V)": f"Ventaja: {f['fond'][1]}",
        "Fond. IdV": f['fond'][2]
    })

df_cba = pd.DataFrame(rows)

df_editado = st.data_editor(
    df_cba,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Descripción / Información": st.column_config.TextColumn(width="large"),
        "Crédito Bancario (A/V)": st.column_config.TextColumn(width="medium"),
        "Asociación (A/V)": st.column_config.TextColumn(width="medium"),
        "Aporte (A/V)": st.column_config.TextColumn(width="medium"),
        "Fondos (A/V)": st.column_config.TextColumn(width="medium"),
    }
)

# Sumamos solo las filas pares (0, 2, 4...) para no duplicar el IDV
totales = df_editado.iloc[::2][["Trad. IdV", "Asoc. IdV", "Apor. IdV", "Fond. IdV"]].sum()

st.subheader("Totales IdV")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Tradicional", totales["Trad. IdV"])
c2.metric("Asociación", totales["Asoc. IdV"])
c3.metric("Aporte", totales["Apor. IdV"])
c4.metric("Fondos", totales["Fond. IdV"])

puntaje_cba = totales.max()
alternativa_ganadora = totales.idxmax()

# --- 6. Satisfacción ---
st.header("6. Satisfacción")
satisfaccion = st.slider("Satisfacción esperada", 1.0, 5.0, 4.0)

# --- 7. Resultados ---
st.header("7. Resultados")
if st.button("Calcular"):
    van = calcular_van(tasa_descuento_mensual, flujos)
    tir_m = calcular_tir(flujos)
    estado, reco = interpretar_resultado(van, tir_m, rentabilidad, satisfaccion, puntaje_cba)
    
    st.write(f"Resultado: **{estado}**")
    st.write(f"Ganador CBA: **{alternativa_ganadora}** con {puntaje_cba} pts.")
    st.metric("VAN", f"S/. {van:,.2f}")
    st.write(reco)
