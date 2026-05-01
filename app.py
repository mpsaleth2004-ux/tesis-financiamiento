import streamlit as st
import numpy as np
import pandas as pd

# ============================================================
# PROTOTIPO WEB PARA EVALUACIÓN DE FINANCIAMIENTO INMOBILIARIO
# Basado en Lean Construction - Choosing by Advantages (CBA)
# Desarrollado en Python con Streamlit
# ============================================================

st.set_page_config(
    page_title="Prototipo CBA - Financiamiento Inmobiliario",
    page_icon="🏗️",
    layout="wide"
)

# -----------------------------
# Funciones financieras
# -----------------------------

def calcular_van(tasa_mensual, flujos):
    van = 0
    for i, flujo in enumerate(flujos):
        van += flujo / ((1 + tasa_mensual) ** i)
    return van


def calcular_tir(flujos):
    tasas = np.linspace(-0.99, 1.5, 20000)
    valores = [calcular_van(tasa, flujos) for tasa in tasas]

    for i in range(len(valores) - 1):
        if valores[i] == 0:
            return tasas[i]
        if valores[i] * valores[i + 1] < 0:
            return tasas[i]
    return None


def interpretar_resultado(van, tir_mensual, rentabilidad, satisfaccion, puntaje_cba):
    tir_anual = ((1 + tir_mensual) ** 12 - 1) if tir_mensual is not None else None

    if van > 0 and tir_anual is not None and tir_anual > 0.14 and rentabilidad >= 17 and satisfaccion >= 4 and puntaje_cba >= 70:
        return "Viable y recomendable", "La alternativa evaluada cumple con los criterios financieros y de satisfacción establecidos."
    elif van > 0 and rentabilidad >= 10:
        return "Viable con observaciones", "La alternativa puede aceptarse, pero requiere revisar riesgos, satisfacción o ventajas CBA."
    else:
        return "No recomendable", "La alternativa no cumple con los criterios mínimos de viabilidad establecidos."


# -----------------------------
# Encabezado
# -----------------------------

st.title("🏗️ Prototipo web para selección del financiamiento inmobiliario")
st.markdown(
    """
    Este prototipo evalúa métodos de financiamiento inmobiliario mediante **VAN, TIR, rentabilidad**, 
    **satisfacción del cliente** y criterios basados en **Choosing by Advantages (CBA)**.
    """
)

st.divider()

# -----------------------------
# Datos generales
# -----------------------------

st.header("1. Datos generales del proyecto")

col1, col2 = st.columns(2)

with col1:
    nombre_proyecto = st.text_input("Nombre del proyecto", "Green Tower")
    costo_total = st.number_input("Costo total del proyecto (S/.)", min_value=0.0, value=10000000.0, step=100000.0)
    horizonte_meses = st.number_input("Horizonte de evaluación (meses)", min_value=1, max_value=60, value=8)

with col2:
    ubicacion = st.text_input("Ubicación", "Lima Top")
    tasa_descuento_anual = st.number_input("Tasa de descuento anual (%)", min_value=0.0, value=12.0, step=0.5) / 100
    inversion_inicial = st.number_input("Inversión inicial / desembolso inicial (S/.)", min_value=0.0, value=3000000.0, step=100000.0)

st.subheader(f"Proyecto evaluado: {nombre_proyecto}")

tasa_descuento_mensual = (1 + tasa_descuento_anual) ** (1 / 12) - 1

st.divider()

# -----------------------------
# Método de financiamiento
# -----------------------------

st.header("2. Datos del método de financiamiento")

metodo = st.selectbox(
    "Seleccione el método de financiamiento",
    [
        "Método 1: Tradicional",
        "Método 2: Aporte mixto",
        "Método 3: Financiamiento con inversionistas"
    ],
    index=1
)

st.subheader("Distribución del financiamiento")

if metodo == "Método 1: Tradicional":
    col3, col4 = st.columns(2)

    with col3:
        porcentaje_banco = st.number_input("Financiamiento bancario (%)", min_value=0.0, max_value=100.0, value=80.0, step=5.0)

    with col4:
        porcentaje_aporte_inmobiliario = st.number_input("Aporte inmobiliario (%)", min_value=0.0, max_value=100.0, value=20.0, step=5.0)

    porcentaje_inversionistas = 0
    porcentaje_asociacion = 0

elif metodo == "Método 2: Aporte mixto":
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        porcentaje_banco = st.number_input("Financiamiento bancario (%)", min_value=0.0, max_value=100.0, value=80.0, step=5.0)

    with col4:
        porcentaje_inversionistas = st.number_input("Inversionistas (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

    with col5:
        porcentaje_asociacion = st.number_input("Asociación con propietarios (%)", min_value=0.0, max_value=100.0, value=7.0, step=1.0)

    with col6:
        porcentaje_aporte_inmobiliario = st.number_input("Aporte inmobiliario (%)", min_value=0.0, max_value=100.0, value=3.0, step=1.0)

else:
    col3, col4, col5 = st.columns(3)

    with col3:
        porcentaje_banco = st.number_input("Financiamiento bancario (%)", min_value=0.0, max_value=100.0, value=80.0, step=5.0)

    with col4:
        porcentaje_inversionistas = st.number_input("Inversionistas (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)

    with col5:
        porcentaje_aporte_inmobiliario = st.number_input("Aporte inmobiliario (%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0)

    porcentaje_asociacion = 0

suma_financiamiento = porcentaje_banco + porcentaje_aporte_inmobiliario + porcentaje_inversionistas + porcentaje_asociacion

if suma_financiamiento != 100:
    st.error(f"La suma del financiamiento debe ser 100%. Actualmente suma {suma_financiamiento:.2f}%")
else:
    st.success("La distribución del financiamiento suma 100%.")

col7, col8, col9 = st.columns(3)

with col7:
    tasa_interes = st.number_input("Tasa de interés anual del crédito bancario (%)", min_value=0.0, value=7.24, step=0.1) / 100

with col8:
    plazo_credito = st.number_input("Plazo del crédito (meses)", min_value=1, max_value=120, value=24)

with col9:
    riesgo = st.selectbox("Nivel de riesgo financiero", ["Bajo", "Medio", "Alto"], index=1)

monto_banco = costo_total * (porcentaje_banco / 100)
monto_aporte_inmobiliario = costo_total * (porcentaje_aporte_inmobiliario / 100)
monto_inversionistas = costo_total * (porcentaje_inversionistas / 100)
monto_asociacion = costo_total * (porcentaje_asociacion / 100)
interes_estimado = monto_banco * tasa_interes * (plazo_credito / 12)

st.info(
    f"Banco: S/. {monto_banco:,.2f} | "
    f"Aporte inmobiliario: S/. {monto_aporte_inmobiliario:,.2f} | "
    f"Inversionistas: S/. {monto_inversionistas:,.2f} | "
    f"Asociación con propietarios: S/. {monto_asociacion:,.2f} | "
    f"Interés estimado: S/. {interes_estimado:,.2f}"
)

st.divider()

# -----------------------------
# Ingresos y egresos
# -----------------------------

st.header("3. Ingresos y egresos del proyecto")

col10, col11 = st.columns(2)

with col10:
    numero_unidades = st.number_input("Número de unidades inmobiliarias", min_value=1, value=40)
    precio_promedio = st.number_input("Precio promedio de venta por unidad (S/.)", min_value=0.0, value=350000.0, step=10000.0)

with col11:
    costos_indirectos = st.number_input("Costos indirectos (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0) / 100
    otros_egresos = st.number_input("Otros egresos estimados (S/.)", min_value=0.0, value=500000.0, step=50000.0)

ingreso_total = numero_unidades * precio_promedio
egreso_total = costo_total + (costo_total * costos_indirectos) + interes_estimado + otros_egresos
utilidad = ingreso_total - egreso_total
rentabilidad = (utilidad / egreso_total) * 100 if egreso_total > 0 else 0

st.success(f"Ingreso total estimado: S/. {ingreso_total:,.2f}")
st.warning(f"Egreso total estimado: S/. {egreso_total:,.2f}")

st.divider()

# -----------------------------
# Flujo de caja mensual
# -----------------------------

st.header("4. Flujo de caja proyectado mensual")
st.markdown("Ingrese el flujo neto esperado por mes. El mes 0 se considera como inversión inicial negativa.")

flujos = [-inversion_inicial]
flujo_base = utilidad / horizonte_meses if horizonte_meses > 0 else 0

for i in range(1, horizonte_meses + 1):
    flujo = st.number_input(f"Flujo mes {i} (S/.)", value=float(flujo_base), step=50000.0)
    flujos.append(flujo)

st.divider()

# -----------------------------
# Matriz CBA
# -----------------------------

st.header(f"5. Aplicación del método CBA - {nombre_proyecto}")
st.markdown("Complete los puntajes IdV en la tabla. Cada valor representa la importancia de la ventaja de cada alternativa.")

factores = [
    "FACTOR 01: Tasa de interés / costo financiero",
    "FACTOR 02: Plazo de retorno / plazo del crédito",
    "FACTOR 03: Riesgo financiero",
    "FACTOR 04: Liquidez / entrada inicial",
    "FACTOR 05: Flexibilidad de condiciones",
    "FACTOR 06: Rentabilidad esperada / retención de utilidades",
    "FACTOR 07: Impacto en la satisfacción del cliente"
]

alternativas = [
    "Crédito bancario tradicional",
    "Asociación con propietarios",
    "Aporte inmobiliario",
    "Fondos de inversión"
]

# Valores iniciales similares al formato de tesis
valores_iniciales = pd.DataFrame({
    "Información general": factores,
    "Crédito bancario tradicional": [80, 70, 60, 90, 70, 80, 80],
    "Asociación con propietarios": [90, 80, 80, 80, 80, 80, 80],
    "Aporte inmobiliario": [95, 85, 85, 85, 80, 90, 70],
    "Fondos de inversión": [60, 60, 50, 60, 70, 50, 50]
})

st.subheader("Tabla CBA editable")

df_cba_editado = st.data_editor(
    valores_iniciales,
    use_container_width=True,
    hide_index=True,
    disabled=["Información general"],
    column_config={
        "Información general": st.column_config.TextColumn("Información general", width="large"),
        "Crédito bancario tradicional": st.column_config.NumberColumn("Crédito bancario tradicional - IdV", min_value=0, max_value=1000, step=10),
        "Asociación con propietarios": st.column_config.NumberColumn("Asociación con propietarios - IdV", min_value=0, max_value=1000, step=10),
        "Aporte inmobiliario": st.column_config.NumberColumn("Aporte inmobiliario - IdV", min_value=0, max_value=1000, step=10),
        "Fondos de inversión": st.column_config.NumberColumn("Fondos de inversión - IdV", min_value=0, max_value=1000, step=10),
    }
)

# Cálculo de IdV total
idv_totales = {}
for alt in alternativas:
    idv_totales[alt] = df_cba_editado[alt].sum()

fila_total = pd.DataFrame({
    "Alternativa": list(idv_totales.keys()),
    "IdV TOTAL": list(idv_totales.values())
})

st.subheader("IdV total por alternativa")
st.dataframe(fila_total, use_container_width=True, hide_index=True)

st.subheader("Gráfico de puntajes IdV")
st.bar_chart(fila_total.set_index("Alternativa"))

alternativa_ganadora = max(idv_totales, key=idv_totales.get)
puntaje_cba = idv_totales[alternativa_ganadora]

st.success(f"Alternativa ganadora según CBA: {alternativa_ganadora} con {puntaje_cba:.0f} puntos IdV.")

st.divider()

# -----------------------------
# Satisfacción
# -----------------------------

st.header("6. Satisfacción del cliente")
satisfaccion = st.slider("Nivel de satisfacción del cliente esperado", 1.0, 5.0, 4.0, step=0.1)

st.divider()

# -----------------------------
# Resultados
# -----------------------------

st.header("7. Resultados del análisis")

if st.button("Calcular resultados"):
    if suma_financiamiento != 100:
        st.error("Corrige la distribución del financiamiento antes de calcular.")
    else:
        van = calcular_van(tasa_descuento_mensual, flujos)
        tir_mensual = calcular_tir(flujos)
        tir_anual = ((1 + tir_mensual) ** 12 - 1) if tir_mensual is not None else None

        estado, recomendacion = interpretar_resultado(van, tir_mensual, rentabilidad, satisfaccion, puntaje_cba)

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.metric("VAN", f"S/. {van:,.2f}")
        with r2:
            if tir_anual is not None:
                st.metric("TIR anual", f"{tir_anual * 100:.2f}%")
            else:
                st.metric("TIR anual", "No calculable")
        with r3:
            st.metric("Rentabilidad", f"{rentabilidad:.2f}%")
        with r4:
            st.metric("Satisfacción", f"{satisfaccion:.1f}/5")

        st.subheader("Resultado CBA")
        st.write(f"Alternativa ganadora: **{alternativa_ganadora}**")
        st.write(f"Puntaje CBA obtenido: **{puntaje_cba:.0f} puntos IdV**")

        st.subheader("Recomendación final")
        if estado == "Viable y recomendable":
            st.success(f"✅ {estado}")
        elif estado == "Viable con observaciones":
            st.warning(f"⚠️ {estado}")
        else:
            st.error(f"❌ {estado}")

        st.write(recomendacion)

        if tir_anual is not None:
            tir_texto = f"{tir_anual * 100:.2f}%"
        else:
            tir_texto = "no calculable"

        st.markdown(
            f"""
            **Interpretación:**  
            Para el proyecto **{nombre_proyecto}**, ubicado en **{ubicacion}**, la aplicación del método CBA identifica como alternativa más conveniente a **{alternativa_ganadora}**, 
            con un puntaje de **{puntaje_cba:.0f} puntos IdV**. Asimismo, el análisis financiero del **{metodo}** obtiene un VAN de **S/. {van:,.2f}**, 
            una TIR anual de **{tir_texto}**, una rentabilidad de **{rentabilidad:.2f}%** y una satisfacción esperada de **{satisfaccion:.1f}/5**.
            """
        )

st.divider()
st.caption(
    "Nota: Este prototipo es una herramienta de apoyo a la toma de decisiones. "
    "Los resultados dependen de los datos ingresados por el usuario y deben interpretarse junto con el análisis técnico-financiero del proyecto."
)
