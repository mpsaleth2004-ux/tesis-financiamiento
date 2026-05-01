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
# Funciones financieras y de formato
# -----------------------------

def calcular_van(tasa_mensual, flujos):
    van = 0
    for i, flujo in enumerate(flujos):
        van += flujo / ((1 + tasa_mensual) ** i)
    return van


def calcular_tir(flujos):
    tasas = np.linspace(-0.99, 2.0, 30000)
    valores = [calcular_van(tasa, flujos) for tasa in tasas]

    for i in range(len(valores) - 1):
        if valores[i] == 0:
            return tasas[i]
        if valores[i] * valores[i + 1] < 0:
            return tasas[i]
    return None


def obtener_texto_likert(valor):
    v = round(valor)
    if v == 5:
        return "5 (Completamente satisfecho)"
    elif v == 4:
        return "4 (Satisfecho)"
    elif v == 3:
        return "3 (Neutral)"
    elif v == 2:
        return "2 (Insatisfecho)"
    else:
        return "1 (Completamente insatisfecho)"


def formato_van(van):
    if van >= 1000000:
        return f"+ S/{van/1000000:.1f} millones"
    elif van <= -1000000:
        return f"- S/{abs(van)/1000000:.1f} millones"
    else:
        return f"S/ {van:,.2f}"


def evaluar_general(rentabilidad, tir_anual, van, satisfaccion):
    if van > 0 and tir_anual is not None and tir_anual >= 0.14 and rentabilidad >= 17.5 and satisfaccion >= 4:
        return "Viable", "Viable y cumple con los indicadores de aceptación."
    else:
        return "No viable", "No viable. La alternativa no cumple con todas las metas de aceptación."


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
    ubicacion = st.text_input("Ubicación", "Lima Top - Jesús María")
    horizonte_meses = st.number_input("Horizonte de evaluación (meses)", min_value=1, max_value=120, value=20)

with col2:
    tasa_descuento_anual = st.number_input("Tasa de descuento anual para VAN (%)", min_value=0.0, value=14.0, step=0.5) / 100
    satisfaccion = st.slider("Nivel de satisfacción esperado", 1.0, 5.0, 4.0, step=0.1)

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
        porcentaje_inversionistas = st.number_input("Fondos de inversión privados (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
    with col5:
        porcentaje_asociacion = st.number_input("Asociación con propietarios (%)", min_value=0.0, max_value=100.0, value=7.0, step=1.0)
    with col6:
        porcentaje_aporte_inmobiliario = st.number_input("Aporte inmobiliario (%)", min_value=0.0, max_value=100.0, value=3.0, step=1.0)

else:
    col3, col4, col5 = st.columns(3)
    with col3:
        porcentaje_banco = st.number_input("Financiamiento bancario (%)", min_value=0.0, max_value=100.0, value=80.0, step=5.0)
    with col4:
        porcentaje_inversionistas = st.number_input("Fondos de inversión privados (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
    with col5:
        porcentaje_aporte_inmobiliario = st.number_input("Aporte inmobiliario (%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0)
    porcentaje_asociacion = 0

suma_financiamiento = porcentaje_banco + porcentaje_aporte_inmobiliario + porcentaje_inversionistas + porcentaje_asociacion

if suma_financiamiento != 100:
    st.error(f"La suma del financiamiento debe ser 100%. Actualmente suma {suma_financiamiento:.2f}%")
else:
    st.success("La distribución del financiamiento suma 100%.")

st.divider()

# -----------------------------
# Datos económicos
# -----------------------------

st.header("3. Datos económicos del proyecto")
st.markdown("Ingrese los datos económicos consolidados del proyecto. La rentabilidad se calcula como: **Utilidad neta / Costo total de inversión × 100**.")

col10, col11, col12 = st.columns(3)

with col10:
    ingresos_ventas = st.number_input("Ventas reales / ingresos totales del proyecto (S/.)", min_value=0.0, value=13300000.0, step=100000.0)

with col11:
    costo_inversion = st.number_input("Costo total de inversión del proyecto (S/.)", min_value=0.0, value=11300000.0, step=100000.0)

with col12:
    utilidad_manual = st.number_input("Utilidad neta del proyecto (S/.)", min_value=-100000000.0, value=2000000.0, step=100000.0)

rentabilidad = (utilidad_manual / costo_inversion) * 100 if costo_inversion > 0 else 0

st.success(f"Ingresos totales: S/. {ingresos_ventas:,.2f}")
st.warning(f"Costo total de inversión: S/. {costo_inversion:,.2f}")
st.info(f"Utilidad neta: S/. {utilidad_manual:,.2f} | Rentabilidad calculada: {rentabilidad:.1f}%")

st.divider()

# -----------------------------
# VAN y TIR
# -----------------------------

st.header("4. Cálculo de VAN y TIR")

modo_indicadores = st.radio(
    "Seleccione cómo desea obtener VAN y TIR",
    [
        "Calcular desde flujo de caja mensual",
        "Ingresar VAN y TIR ya calculados"
    ],
    index=1
)

if modo_indicadores == "Calcular desde flujo de caja mensual":
    st.markdown("Ingrese el flujo neto esperado por mes. El mes 0 se considera como inversión inicial negativa.")
    inversion_inicial = st.number_input("Inversión inicial para el flujo de caja (S/.)", min_value=0.0, value=costo_inversion, step=100000.0)

    flujos = [-inversion_inicial]
    flujo_base = (inversion_inicial + utilidad_manual) / horizonte_meses if horizonte_meses > 0 else 0

    for i in range(1, horizonte_meses + 1):
        flujo = st.number_input(f"Flujo mes {i} (S/.)", value=float(flujo_base), step=50000.0)
        flujos.append(flujo)

    van = calcular_van(tasa_descuento_mensual, flujos)
    tir_mensual = calcular_tir(flujos)
    tir_anual = ((1 + tir_mensual) ** 12 - 1) if tir_mensual is not None else None

else:
    st.markdown("Use esta opción cuando ya tiene los indicadores financieros consolidados del estudio financiero del proyecto.")
    col_van, col_tir = st.columns(2)
    with col_van:
        van = st.number_input("Valor Actual Neto - VAN (S/.)", value=3200000.0, step=100000.0)
    with col_tir:
        tir_anual_porcentaje = st.number_input("Tasa Interna de Retorno - TIR (%)", value=28.0, step=0.5)
    tir_anual = tir_anual_porcentaje / 100

st.divider()

# -----------------------------
# 5. Tabla de CBA
# -----------------------------

st.header("5. Aplicación del Método CBA (Tabular)")
st.info("💡 El IdV se ingresa en la primera fila de cada factor. Los totales se actualizan automáticamente.")

filas_cba = [
    {"Descripción / Información": "F01: Tasa de interés / costo financiero", "Crédito Bancario": "Atributo: Tasa efectiva anual 10.5% fija", "Trad. IdV": 80, "Asociación": "Atributo: Interés 0%, pero cesión ≈ 20% del proyecto", "Asoc. IdV": 100, "Aporte Inmob.": "Atributo: Interés 0%, requiere preventa ≥ 30-50% para liquidez", "Apor. IdV": 100, "Fondos Invers.": "Atributo: Rentabilidad exigida entre 18-22%", "Fond. IdV": 40},
    {"Descripción / Información": "Criterio: Mientras menor sea la tasa efectiva anual y más estable la modalidad, mejor", "Crédito Bancario": "Ventaja: Tasa relativamente baja y previsible", "Trad. IdV": None, "Asociación": "Ventaja: Elimina costo financiero directo", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Se elimina completamente el costo financiero", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Mayor costo financiero", "Fond. IdV": None},
    {"Descripción / Información": "F02: Plazo de retorno / plazo del crédito", "Crédito Bancario": "Atributo: Plazo de 24 meses", "Trad. IdV": 80, "Asociación": "Atributo: Retorno ligado a ventas", "Asoc. IdV": 60, "Aporte Inmob.": "Atributo: Ingreso en 12-24 meses", "Apor. IdV": 75, "Fondos Invers.": "Atributo: Retorno 18-24 meses", "Fond. IdV": 50},
    {"Descripción / Información": "Criterio: Mientras menor sea el plazo sin afectar el flujo de caja, mejor", "Crédito Bancario": "Ventaja: Flujo estable", "Trad. IdV": None, "Asociación": "Ventaja: Sin presión de pago", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Flexibilidad en recuperación", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Presión de caja", "Fond. IdV": None},
    {"Descripción / Información": "F03: Riesgo financiero", "Crédito Bancario": "Atributo: Riesgo controlado", "Trad. IdV": 70, "Asociación": "Atributo: Riesgo financiero bajo", "Asoc. IdV": 90, "Aporte Inmob.": "Atributo: Riesgo dependiente de venta", "Apor. IdV": 50, "Fondos Invers.": "Atributo: Riesgo alto", "Fond. IdV": 40},
    {"Descripción / Información": "Criterio: Mientras menor sea la exposición a inflación, impago y variabilidad de tasas, mejor", "Crédito Bancario": "Ventaja: Supervisión bancaria", "Trad. IdV": None, "Asociación": "Ventaja: Sin intereses ni pagos fijos", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Evita endeudamiento", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Compromisos contractuales", "Fond. IdV": None},
    {"Descripción / Información": "F04: Liquidez / entrada inicial", "Crédito Bancario": "Atributo: Aporte inicial del 30%", "Trad. IdV": 70, "Asociación": "Atributo: Aporte 0-10%", "Asoc. IdV": 90, "Aporte Inmob.": "Atributo: Entradas de clientes 30%", "Apor. IdV": 85, "Fondos Invers.": "Atributo: Inyección 70-100%", "Fond. IdV": 80},
    {"Descripción / Información": "Criterio: Mientras menor sea el porcentaje de entrada y mayor la flexibilidad de acceso, mejor", "Crédito Bancario": "Ventaja: Acceso rápido", "Trad. IdV": None, "Asociación": "Ventaja: Bajo desembolso", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Liquidez inmediata", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Liquidez para obra", "Fond. IdV": None},
    {"Descripción / Información": "F05: Flexibilidad de condiciones", "Crédito Bancario": "Atributo: Baja flexibilidad", "Trad. IdV": 50, "Asociación": "Atributo: Alta flexibilidad", "Asoc. IdV": 90, "Aporte Inmob.": "Atributo: Flexibilidad media", "Apor. IdV": 100, "Fondos Invers.": "Atributo: Negociable", "Fond. IdV": 80},
    {"Descripción / Información": "Criterio: Mientras mayor sea la capacidad de renegociar plazos, pagos y garantías, mejor", "Crédito Bancario": "Ventaja: Menor flexibilidad", "Trad. IdV": None, "Asociación": "Ventaja: Alta renegociación", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Reprogramación", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Caso a caso", "Fond. IdV": None},
    {"Descripción / Información": "F06: Rentabilidad esperada / retención de utilidades", "Crédito Bancario": "Atributo: Bajo costo financiero", "Trad. IdV": 90, "Asociación": "Atributo: Cesión del 20%", "Asoc. IdV": 70, "Aporte Inmob.": "Atributo: Sin participación externa", "Apor. IdV": 95, "Fondos Invers.": "Atributo: Alta rentabilidad exigida", "Fond. IdV": 50},
    {"Descripción / Información": "Criterio: Mientras mayor sea el margen neto proyectado y la capacidad de reinversión, mejor", "Crédito Bancario": "Ventaja: Mayor utilidad neta", "Trad. IdV": None, "Asociación": "Ventaja: Media, pero sin deuda", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Retiene 100% de utilidad", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Menor utilidad", "Fond. IdV": None},
    {"Descripción / Información": "F07: Impacto en la satisfacción del cliente", "Crédito Bancario": "Atributo: Institución reconocida", "Trad. IdV": 90, "Asociación": "Atributo: Depende del promotor", "Asoc. IdV": 70, "Aporte Inmob.": "Atributo: Sin intermediarios", "Apor. IdV": 85, "Fondos Invers.": "Atributo: Cliente no percibe participación", "Fond. IdV": 60},
    {"Descripción / Información": "Criterio: Mientras mayor sea la claridad de condiciones y percepción de seguridad, mejor", "Crédito Bancario": "Ventaja: Alta confianza", "Trad. IdV": None, "Asociación": "Ventaja: Seguridad media", "Asoc. IdV": None, "Aporte Inmob.": "Ventaja: Mayor control", "Apor. IdV": None, "Fondos Invers.": "Ventaja: Menor confianza", "Fond. IdV": None},
]

df_cba = pd.DataFrame(filas_cba)
columnas_base = ["Descripción / Información"]

if metodo == "Método 1: Tradicional":
    columnas_mostrar = ["Crédito Bancario", "Trad. IdV", "Aporte Inmob.", "Apor. IdV"]
elif metodo == "Método 2: Aporte mixto":
    columnas_mostrar = ["Crédito Bancario", "Trad. IdV", "Asociación", "Asoc. IdV", "Aporte Inmob.", "Apor. IdV", "Fondos Invers.", "Fond. IdV"]
else:
    columnas_mostrar = ["Crédito Bancario", "Trad. IdV", "Aporte Inmob.", "Apor. IdV", "Fondos Invers.", "Fond. IdV"]

df_cba_visible = df_cba[columnas_base + columnas_mostrar]

df_editado = st.data_editor(
    df_cba_visible,
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

totales_idv = {}
if "Trad. IdV" in df_editado.columns:
    totales_idv["Crédito Bancario"] = df_editado["Trad. IdV"].fillna(0).sum()
if "Asoc. IdV" in df_editado.columns:
    totales_idv["Asociación"] = df_editado["Asoc. IdV"].fillna(0).sum()
if "Apor. IdV" in df_editado.columns:
    totales_idv["Aporte Inmobiliario"] = df_editado["Apor. IdV"].fillna(0).sum()
if "Fond. IdV" in df_editado.columns:
    totales_idv["Fondos de Inversión"] = df_editado["Fond. IdV"].fillna(0).sum()

alternativa_ganadora = max(totales_idv, key=totales_idv.get)
puntaje_cba = totales_idv[alternativa_ganadora]

st.markdown("### Totales IdV en tiempo real")
columnas_metricas = st.columns(len(totales_idv))
for i, (nombre_alt, valor_idv) in enumerate(totales_idv.items()):
    columnas_metricas[i].metric(nombre_alt, f"{valor_idv:.0f}")

st.divider()

# -----------------------------
# Resultados
# -----------------------------

st.header("6. Resultados del análisis")

if st.button("Calcular resultados"):
    if suma_financiamiento != 100:
        st.error("Corrige la distribución del financiamiento antes de calcular.")
    else:
        eval_rentabilidad = "Cumple" if rentabilidad >= 17.5 else "No cumple"
        eval_tir = "Cumple" if (tir_anual is not None and tir_anual >= 0.14) else "No cumple"
        eval_van = "Cumple" if van > 0 else "No cumple"
        eval_satisfaccion = "Cumple" if satisfaccion >= 4 else "No cumple"

        estado, recomendacion = evaluar_general(rentabilidad, tir_anual, van, satisfaccion)

        st.subheader("Tabla de Indicadores y Resultados")

        datos_tabla_resultados = {
            "Tipo": ["Cuantitativo", "Cuantitativo", "Cuantitativo", "Cualitativo"],
            "Indicador": [
                "Nivel de Rentabilidad del proyecto",
                "Tasa Interna de Retorno (TIR)",
                "Valor Actual Neto (VAN)",
                "Nivel de Satisfacción de la inmobiliaria - constructora"
            ],
            "Unidad de medida": ["Porcentaje (%)", "Porcentaje (%)", "Miles de soles (S/)", "Escala Likert"],
            "Rango": [
                "(Beneficio Neto)/(Inversión Total) x 100%",
                "0% - 100%",
                "VAN < 0 = No viable, VAN > 0 = Viable",
                "5: Completamente satisfecho | 4: Satisfecho | 3: Neutral | 2: Insatisfecho | 1: Completamente insatisfecho"
            ],
            "Meta de aceptación": [
                "≥ 17.5% Monteza (2024)",
                "≥ 14% Monteza (2024)",
                "VAN > 0 Kaufmann, et al. (2022)",
                "Satisfecho Kaufmann, et al. (2022)"
            ],
            metodo: [
                f"{rentabilidad:.1f}%",
                f"{tir_anual * 100:.1f}%" if tir_anual is not None else "N/A",
                formato_van(van),
                obtener_texto_likert(satisfaccion)
            ],
            "Evaluación": [eval_rentabilidad, eval_tir, eval_van, eval_satisfaccion]
        }

        df_resultados = pd.DataFrame(datos_tabla_resultados)
        st.table(df_resultados)

        st.subheader("Resultado CBA")
        st.write(f"Alternativa con mayor IdV: **{alternativa_ganadora}**")
        st.write(f"Puntaje CBA obtenido: **{puntaje_cba:.0f} puntos IdV**")

        st.subheader("Recomendación final")
        if estado == "Viable":
            st.success(f"✅ {estado}")
        else:
            st.error(f"❌ {estado}")
        st.write(recomendacion)

        tir_texto = f"{tir_anual * 100:.2f}%" if tir_anual is not None else "no calculable"
        st.markdown(
            f"""
            **Interpretación:** Para el proyecto **{nombre_proyecto}**, ubicado en **{ubicacion}**, la aplicación del método CBA identifica como alternativa con mayor valor a **{alternativa_ganadora}**, con **{puntaje_cba:.0f} puntos IdV**. Asimismo, el análisis financiero del **{metodo}** obtiene una rentabilidad de **{rentabilidad:.2f}%**, una TIR anual de **{tir_texto}**, un VAN de **{formato_van(van)}** y una satisfacción esperada de **{obtener_texto_likert(satisfaccion)}**.
            """
        )

st.divider()
st.caption(
    "Nota: Este prototipo es una herramienta de apoyo a la toma de decisiones. "
    "Los resultados dependen de los datos ingresados por el usuario y deben interpretarse junto con el análisis técnico-financiero del proyecto."
)
