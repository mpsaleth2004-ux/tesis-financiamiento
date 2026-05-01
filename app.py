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
    # Nota: Para mayor precisión en producción se recomienda usar numpy_financial.irr()
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
# 5. Tabla de CBA (Editable y Dinámica - Estructura Word)
# -----------------------------

st.header("5. Aplicación del Método CBA (Tabular)")
st.info("💡 **Nota técnica:** Streamlit no soporta visualmente la combinación de celdas (merge) en tablas editables. Para mantener los cálculos exactos y no duplicar valores, el IdV solo se ingresa en la primera fila de cada factor.")

# Construcción de la matriz con los 7 factores completos. 
filas_cba = [
    # --- FACTOR 01 ---
    {
        "Descripción / Información": "F01: Tasa de interés / costo financiero",
        "Crédito Bancario": "Atributo: Tasa efectiva anual 10.5% fija", "Trad. IdV": 80,
        "Asociación": "Atributo: Interés 0%, pero cesión ≈ 20% del proyecto", "Asoc. IdV": 100,
        "Aporte Inmob.": "Atributo: Interés 0%, requiere preventa ≥ 30-50% para liquidez", "Apor. IdV": 100,
        "Fondos Invers.": "Atributo: Rentabilidad exigida entre 18-22%", "Fond. IdV": 40
    },
    {
        "Descripción / Información": "Criterio: Mientras menor sea la tasa efectiva anual y más estable la modalidad, mejor",
        "Crédito Bancario": "Ventaja: Tasa relativamente baja y previsible", "Trad. IdV": None,
        "Asociación": "Ventaja: Elimina costo financiero directo", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Se elimina completamente el costo financiero, lo que maximiza la utilidad neta", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Mayor costo financiero", "Fond. IdV": None
    },
    
    # --- FACTOR 02 ---
    {
        "Descripción / Información": "F02: Plazo de retorno / plazo del crédito",
        "Crédito Bancario": "Atributo: Plazo de 24 meses, ajustado al ciclo constructivo", "Trad. IdV": 80,
        "Asociación": "Atributo: Retorno ligado a ventas (plazo indefinido / >24 meses)", "Asoc. IdV": 60,
        "Aporte Inmob.": "Atributo: Venta/entrega escalonada -> parte del ingreso en 12-24 meses", "Apor. IdV": 75,
        "Fondos Invers.": "Atributo: Fondos exigen retorno 18-24 meses (fuerte presión)", "Fond. IdV": 50
    },
    {
        "Descripción / Información": "Criterio: Mientras menor sea el plazo sin afectar el flujo de caja, mejor",
        "Crédito Bancario": "Ventaja: Permite flujo estable y recuperación sincronizada con ventas", "Trad. IdV": None,
        "Asociación": "Ventaja: No hay presión de pago, pero retorno más largo", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Flexibilidad en la recuperación del capital, sin presiones externas", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Presiona flujo de caja; menos margen de maniobra", "Fond. IdV": None
    },

    # --- FACTOR 03 ---
    {
        "Descripción / Información": "F03: Riesgo financiero",
        "Crédito Bancario": "Atributo: Riesgo controlado (garantías hipotecarias, ratio DSCR = 1.2-1.3)", "Trad. IdV": 70,
        "Asociación": "Atributo: Riesgo financiero bajo (sin deuda, reparto de utilidades)", "Asoc. IdV": 90,
        "Aporte Inmob.": "Atributo: Riesgo dependiente de venta (porcentaje vendido p.ej. 30-50%)", "Apor. IdV": 50,
        "Fondos Invers.": "Atributo: Estricto covenants, riesgo si no se cumple objetivo de venta", "Fond. IdV": 40
    },
    {
        "Descripción / Información": "Criterio: Mientras menor sea la exposición a inflación, impago y variabilidad de tasas, mejor",
        "Crédito Bancario": "Ventaja: Riesgo controlado gracias a supervisión bancaria", "Trad. IdV": None,
        "Asociación": "Ventaja: Riesgo bajo; no hay intereses ni pagos fijos", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Se evita el endeudamiento, pero se incrementa la exposición financiera total", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Riesgo elevado por compromisos contractuales", "Fond. IdV": None
    },

    # --- FACTOR 04 ---
    {
        "Descripción / Información": "F04: Liquidez / entrada inicial",
        "Crédito Bancario": "Atributo: Aporte inicial del 30%", "Trad. IdV": 70,
        "Asociación": "Atributo: Aporte propio ~0-10% (terreno aportado como capital)", "Asoc. IdV": 90,
        "Aporte Inmob.": "Atributo: Entradas de clientes: 30% del precio como reserva/anticipo", "Apor. IdV": 85,
        "Fondos Invers.": "Atributo: Inyección inmediata 70-100% del capital requerido", "Fond. IdV": 80
    },
    {
        "Descripción / Información": "Criterio: Mientras menor sea el porcentaje de entrada y mayor la flexibilidad de acceso, mejor",
        "Crédito Bancario": "Ventaja: Acceso rápido al financiamiento tras preventas", "Trad. IdV": None,
        "Asociación": "Ventaja: No requiere gran desembolso inicial", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Se dispone de liquidez inmediata para iniciar la obra, sin trámites bancarios", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Liquidez inmediata para la obra", "Fond. IdV": None
    },

    # --- FACTOR 05 ---
    {
        "Descripción / Información": "F05: Flexibilidad de condiciones",
        "Crédito Bancario": "Atributo: Condiciones contractuales bajas renegociables; comisiones por modificación", "Trad. IdV": 50,
        "Asociación": "Atributo: Contrato privado, cláusulas negociables (alta flexibilidad)", "Asoc. IdV": 90,
        "Aporte Inmob.": "Atributo: Flexibilidad media (acuerdos con compradores)", "Apor. IdV": 100,
        "Fondos Invers.": "Atributo: Condiciones negociables caso a caso", "Fond. IdV": 80
    },
    {
        "Descripción / Información": "Criterio: Mientras mayor sea la capacidad de renegociar plazos, pagos y garantías, mejor",
        "Crédito Bancario": "Ventaja: Menor flexibilidad ante imprevistos", "Trad. IdV": None,
        "Asociación": "Ventaja: Alta capacidad de renegociación", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Se pueden reprogramar desembolsos y cronogramas sin depender de terceros", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Condiciones negociables caso a caso", "Fond. IdV": None
    },

    # --- FACTOR 06 ---
    {
        "Descripción / Información": "F06: Rentabilidad esperada / retención de utilidades",
        "Crédito Bancario": "Atributo: Bajo costo financiero (10.5%)", "Trad. IdV": 90,
        "Asociación": "Atributo: Cesión del 20% del proyecto", "Asoc. IdV": 70,
        "Aporte Inmob.": "Atributo: No hay participación externa en las ganancias", "Apor. IdV": 95,
        "Fondos Invers.": "Atributo: Alta rentabilidad exigida por el inversor", "Fond. IdV": 50
    },
    {
        "Descripción / Información": "Criterio: Mientras mayor sea el margen neto proyectado y la capacidad de reinversión, mejor",
        "Crédito Bancario": "Ventaja: Mayor margen de utilidad neta", "Trad. IdV": None,
        "Asociación": "Ventaja: Rentabilidad media, pero sin deuda", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Se retiene el 100% de la utilidad neta", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Menor utilidad neta para el promotor", "Fond. IdV": None
    },

    # --- FACTOR 07 ---
    {
        "Descripción / Información": "F07: Impacto en la satisfacción del cliente",
        "Crédito Bancario": "Atributo: Respaldado por institución reconocida", "Trad. IdV": 90,
        "Asociación": "Atributo: Dependiente de la gestión del promotor", "Asoc. IdV": 70,
        "Aporte Inmob.": "Atributo: Financiamiento interno, sin intermediarios", "Apor. IdV": 85,
        "Fondos Invers.": "Atributo: Cliente no percibe participación directa", "Fond. IdV": 60
    },
    {
        "Descripción / Información": "Criterio: Mientras mayor sea la claridad de condiciones y percepción de seguridad, mejor",
        "Crédito Bancario": "Ventaja: Alta confianza del cliente", "Trad. IdV": None,
        "Asociación": "Ventaja: Percepción media de seguridad", "Asoc. IdV": None,
        "Aporte Inmob.": "Ventaja: Mayor control del proceso y confianza en el cumplimiento", "Apor. IdV": None,
        "Fondos Invers.": "Ventaja: Menor confianza percibida", "Fond. IdV": None
    }
]

df_cba = pd.DataFrame(filas_cba)

# Renderizar la tabla editable
df_editado = st.data_editor(
    df_cba,
    use_container_width=True,
    hide_index=True,
    height=550, 
    column_config={
        "Descripción / Información": st.column_config.TextColumn(width="large"),
        "Crédito Bancario": st.column_config.TextColumn(width="medium"),
        "Trad. IdV": st.column_config.NumberColumn(min_value=0, max_value=100),
        "Asociación": st.column_config.TextColumn(width="medium"),
        "Asoc. IdV": st.column_config.NumberColumn(min_value=0, max_value=100),
        "Aporte Inmob.": st.column_config.TextColumn(width="medium"),
        "Apor. IdV": st.column_config.NumberColumn(min_value=0, max_value=100),
        "Fondos Invers.": st.column_config.TextColumn(width="medium"),
        "Fond. IdV": st.column_config.NumberColumn(min_value=0, max_value=100),
    }
)

# Cálculo dinámico en tiempo real de los totales IdV
totales_idv = {
    "Crédito Bancario Tradicional": df_editado["Trad. IdV"].sum(),
    "Asociación con Propietarios": df_editado["Asoc. IdV"].sum(),
    "Aporte Inmobiliario": df_editado["Apor. IdV"].sum(),
    "Fondos de Inversión": df_editado["Fond. IdV"].sum()
}

alternativa_ganadora = max(totales_idv, key=totales_idv.get)
puntaje_cba = totales_idv[alternativa_ganadora]

# Mostrar métricas de puntaje total debajo de la tabla
st.markdown("### Totales IdV en tiempo real")
col_t1, col_t2, col_t3, col_t4 = st.columns(4)
col_t1.metric("Crédito Bancario", totales_idv["Crédito Bancario Tradicional"])
col_t2.metric("Asociación con Propietarios", totales_idv["Asociación con Propietarios"])
col_t3.metric("Aporte Inmobiliario", totales_idv["Aporte Inmobiliario"])
col_t4.metric("Fondos de Inversión", totales_idv["Fondos de Inversión"])

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
            **Interpretación:** Para el proyecto **{nombre_proyecto}**, ubicado en **{ubicacion}**, la aplicación del método CBA identifica como alternativa más conveniente a **{alternativa_ganadora}**, 
            con un puntaje de **{puntaje_cba:.0f} puntos IdV**. Asimismo, el análisis financiero del **{metodo}** obtiene un VAN de **S/. {van:,.2f}**, 
            una TIR anual de **{tir_texto}**, una rentabilidad de **{rentabilidad:.2f}%** y una satisfacción esperada de **{satisfaccion:.1f}/5**.
            """
        )

st.divider()
st.caption(
    "Nota: Este prototipo es una herramienta de apoyo a la toma de decisiones. "
    "Los resultados dependen de los datos ingresados por el usuario y deben interpretarse junto con el análisis técnico-financiero del proyecto."
)
