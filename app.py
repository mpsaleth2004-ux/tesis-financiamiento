import streamlit as st
import pandas as pd

# ============================================================
# PROTOTIPO WEB PARA SELECCIÓN DEL FINANCIAMIENTO INMOBILIARIO
# Lean Construction - Choosing by Advantages (CBA)
# ============================================================

st.set_page_config(
    page_title="Prototipo CBA - Financiamiento Inmobiliario",
    page_icon="🏗️",
    layout="wide"
)

# -----------------------------
# Funciones auxiliares
# -----------------------------

def formato_soles(valor):
    return f"S/. {valor:,.2f}"


def formato_van(van):
    if van >= 1000000:
        return f"+ S/. {van/1000000:.1f} millones"
    elif van <= -1000000:
        return f"- S/. {abs(van)/1000000:.1f} millones"
    return f"S/. {van:,.2f}"


def texto_satisfaccion(valor):
    if valor == 5:
        return "5 (Completamente satisfecho)"
    if valor == 4:
        return "4 (Satisfecho)"
    if valor == 3:
        return "3 (Neutral)"
    if valor == 2:
        return "2 (Insatisfecho)"
    return "1 (Completamente insatisfecho)"


# -----------------------------
# Datos por método
# Estos resultados están alineados con la tabla del informe
# -----------------------------

RESULTADOS_METODO = {
    "Método 1: Tradicional": {
        "banco": 80,
        "asociacion": 0,
        "aporte": 20,
        "fondos": 0,
        "ventas": 13500000,
        "costo": 11620000,
        "utilidad": 1880000,
        "rentabilidad": 16.2,
        "tir": 20,
        "van": 2100000,
        "satisfaccion": 3,
        "idv": 530,
        "viable": False,
        "comentario": "El método tradicional es financieramente estable, pero no alcanza la meta mínima de rentabilidad requerida."
    },
    "Método 2: Aporte mixto": {
        "banco": 80,
        "asociacion": 7,
        "aporte": 3,
        "fondos": 10,
        "ventas": 13500000,
        "costo": 11300000,
        "utilidad": 2000000,
        "rentabilidad": 17.7,
        "tir": 28,
        "van": 3200000,
        "satisfaccion": 4,
        "idv": 590,
        "viable": True,
        "comentario": "El método 2 es el más eficiente, ya que cumple con rentabilidad, TIR, VAN y satisfacción esperada."
    },
    "Método 3: Financiamiento con inversionistas": {
        "banco": 80,
        "asociacion": 0,
        "aporte": 5,
        "fondos": 15,
        "ventas": 13500000,
        "costo": 11650000,
        "utilidad": 2030000,
        "rentabilidad": 17.4,
        "tir": 26,
        "van": 2800000,
        "satisfaccion": 3,
        "idv": 585,
        "viable": False,
        "comentario": "El método 3 mejora frente al tradicional, pero no alcanza la meta de rentabilidad del método 2."
    }
}

# -----------------------------
# Encabezado
# -----------------------------

st.title("🏗️ Prototipo web para selección del financiamiento inmobiliario")
st.markdown(
    "Este prototipo evalúa métodos de financiamiento inmobiliario mediante **VAN, TIR, rentabilidad**, "
    "**satisfacción del cliente** y criterios basados en **Choosing by Advantages (CBA)**."
)

st.divider()

# -----------------------------
# 1. Datos generales del proyecto
# -----------------------------

st.header("1. Datos generales del proyecto")

col1, col2 = st.columns(2)

with col1:
    nombre_proyecto = st.text_input("Nombre del proyecto", "Green Tower")
    provincia = st.text_input("Provincia", "Lima")
    distrito = st.text_input("Distrito", "Jesús María")
    direccion = st.text_input("Dirección", "Av. Horacio Urteaga 456-460")
    tipo_proyecto = st.text_input("Tipo de proyecto", "Edificio multifamiliar Mi Vivienda")

with col2:
    pisos = st.number_input("Número de pisos", min_value=1, value=19)
    sotanos = st.number_input("Número de sótanos", min_value=0, value=3)
    departamentos = st.number_input("Número de departamentos", min_value=1, value=52)
    estacionamientos = st.number_input("Estacionamientos vehiculares", min_value=0, value=18)
    estacionamientos_bici = st.number_input("Estacionamientos de bicicletas", min_value=0, value=52)

col3, col4, col5 = st.columns(3)
with col3:
    area_techada = st.number_input("Área techada total (m²)", min_value=0.0, value=5037.36, step=10.0)
with col4:
    area_terreno = st.number_input("Área del terreno (m²)", min_value=0.0, value=364.98, step=10.0)
with col5:
    altura = st.number_input("Altura del anteproyecto (m)", min_value=0.0, value=52.85, step=0.5)

st.info(
    f"Proyecto evaluado: **{nombre_proyecto}**, ubicado en **{direccion}, {distrito} - {provincia}**. "
    f"El proyecto considera **{departamentos} departamentos**, **{pisos} pisos**, **{sotanos} sótanos**, "
    f"**{estacionamientos} estacionamientos vehiculares** y **{estacionamientos_bici} estacionamientos para bicicletas**."
)

st.divider()

# -----------------------------
# 2. Método de financiamiento
# -----------------------------

st.header("2. Datos del método de financiamiento")

metodo = st.selectbox(
    "Seleccione el método de financiamiento",
    list(RESULTADOS_METODO.keys()),
    index=1
)

datos = RESULTADOS_METODO[metodo]

st.subheader("Distribución del financiamiento")

cols = st.columns(4)
cols[0].metric("Financiamiento bancario", f"{datos['banco']}%")
cols[1].metric("Asociación con propietarios", f"{datos['asociacion']}%")
cols[2].metric("Aporte inmobiliario", f"{datos['aporte']}%")
cols[3].metric("Fondos de inversión", f"{datos['fondos']}%")

suma = datos["banco"] + datos["asociacion"] + datos["aporte"] + datos["fondos"]

if suma == 100:
    st.success("La distribución del financiamiento suma 100%.")
else:
    st.error(f"La distribución del financiamiento suma {suma}%. Debe sumar 100%.")

st.divider()

# -----------------------------
# 3. Datos económicos
# -----------------------------

st.header("3. Datos económicos del proyecto")
st.markdown("Los datos económicos se actualizan según el método seleccionado para mantener coherencia con los resultados del informe.")

col6, col7, col8 = st.columns(3)
col6.metric("Ventas reales / ingresos proyectados", formato_soles(datos["ventas"]))
col7.metric("Costo total de inversión", formato_soles(datos["costo"]))
col8.metric("Utilidad neta", formato_soles(datos["utilidad"]))

st.info(f"Rentabilidad calculada: **{datos['rentabilidad']}%**")

st.divider()

# -----------------------------
# 4. Indicadores financieros
# -----------------------------

st.header("4. Indicadores financieros calculados")

col9, col10, col11, col12 = st.columns(4)
col9.metric("Rentabilidad", f"{datos['rentabilidad']}%")
col10.metric("TIR", f"{datos['tir']}%")
col11.metric("VAN", formato_van(datos["van"]))
col12.metric("Satisfacción", texto_satisfaccion(datos["satisfaccion"]))

st.divider()

# -----------------------------
# 5. Tabla CBA
# -----------------------------

st.header("5. Aplicación del Método CBA (Tabular)")
st.info("La tabla CBA muestra los factores, atributos, ventajas e IdV considerados para comparar las alternativas de financiamiento.")

filas_cba = [
    ["F01: Tasa de interés / costo financiero", "Tasa efectiva anual 10.5% fija", 80, "Interés 0%, cesión aproximada del 20%", 100, "Interés 0%, sin costo financiero directo", 100, "Rentabilidad exigida 18%-22%", 40],
    ["Criterio: Mientras menor sea la tasa efectiva anual y más estable la modalidad, mejor", "Tasa relativamente baja y previsible", "", "Elimina costo financiero directo", "", "Maximiza utilidad neta", "", "Mayor costo financiero", ""],
    ["F02: Plazo de retorno / plazo del crédito", "Plazo de 24 meses", 80, "Retorno ligado a ventas", 60, "Retorno según flujo de ventas", 75, "Retorno rápido 18-24 meses", 50],
    ["Criterio: Mientras menor sea el plazo sin afectar el flujo de caja, mejor", "Permite flujo estable", "", "No hay presión de pago", "", "Flexibilidad en recuperación", "", "Presiona flujo de caja", ""],
    ["F03: Riesgo financiero", "Riesgo medio con garantías", 70, "Riesgo financiero bajo", 90, "Riesgo dependiente de ventas", 50, "Riesgo alto", 40],
    ["Criterio: Mientras menor sea la exposición a inflación, impago y variabilidad de tasas, mejor", "Supervisión bancaria", "", "Sin intereses ni pagos fijos", "", "Evita endeudamiento", "", "Compromisos contractuales", ""],
    ["F04: Liquidez / entrada inicial", "Aporte inicial del 30%", 70, "Aporte propio 0%-10%", 90, "Entradas de clientes", 85, "Inyección inmediata", 80],
    ["Criterio: Mientras menor sea el porcentaje de entrada y mayor la flexibilidad de acceso, mejor", "Acceso rápido al financiamiento", "", "No requiere gran desembolso", "", "Liquidez inmediata", "", "Liquidez para obra", ""],
    ["F05: Flexibilidad de condiciones", "Condiciones rígidas", 50, "Contrato privado flexible", 90, "Control financiero interno", 100, "Condiciones negociables", 80],
    ["Criterio: Mientras mayor sea la capacidad de renegociar plazos, pagos y garantías, mejor", "Menor flexibilidad", "", "Alta capacidad de renegociación", "", "Reprogramación sin terceros", "", "Negociable caso a caso", ""],
    ["F06: Rentabilidad esperada / retención de utilidades", "Bajo costo financiero", 90, "Cesión del 20%", 70, "Sin participación externa", 95, "Alta rentabilidad exigida", 50],
    ["Criterio: Mientras mayor sea el margen neto proyectado y la capacidad de reinversión, mejor", "Mayor margen de utilidad", "", "Rentabilidad media", "", "Retiene 100% de utilidad", "", "Menor utilidad neta", ""],
    ["F07: Impacto en la satisfacción del cliente", "Respaldo bancario", 90, "Depende de gestión del promotor", 70, "Sin intermediarios", 85, "Baja percepción directa", 60],
    ["Criterio: Mientras mayor sea la claridad de condiciones y percepción de seguridad, mejor", "Alta confianza", "", "Percepción media", "", "Mayor control del proceso", "", "Menor confianza percibida", ""],
]

df_cba = pd.DataFrame(
    filas_cba,
    columns=[
        "Descripción / Información",
        "Crédito Bancario", "IdV CB",
        "Asociación", "IdV Asoc.",
        "Aporte Inmobiliario", "IdV Aporte",
        "Fondos de Inversión", "IdV Fondos"
    ]
)

st.dataframe(df_cba, use_container_width=True, hide_index=True, height=530)

st.subheader("Totales IdV")
col13, col14, col15, col16 = st.columns(4)
col13.metric("Crédito Bancario", "530")
col14.metric("Asociación", "570")
col15.metric("Aporte Inmobiliario", "590")
col16.metric("Fondos de Inversión", "400")

st.success(f"Puntaje CBA del método seleccionado: **{datos['idv']} puntos IdV**")

st.divider()

# -----------------------------
# 6. Resultados
# -----------------------------

st.header("6. Resultados del análisis")

if st.button("Calcular resultados"):
    evaluacion_rentabilidad = "Cumple" if datos["rentabilidad"] >= 17.5 else "No cumple"
    evaluacion_tir = "Cumple" if datos["tir"] >= 14 else "No cumple"
    evaluacion_van = "Cumple" if datos["van"] > 0 else "No cumple"
    evaluacion_satisfaccion = "Cumple" if datos["satisfaccion"] >= 4 else "No cumple"

    tabla_resultados = pd.DataFrame({
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
            "VAN > 0 Kaufmann et al. (2022)",
            "Satisfecho Kaufmann et al. (2022)"
        ],
        metodo: [
            f"{datos['rentabilidad']}%",
            f"{datos['tir']}%",
            formato_van(datos["van"]),
            texto_satisfaccion(datos["satisfaccion"])
        ],
        "Evaluación": [
            evaluacion_rentabilidad,
            evaluacion_tir,
            evaluacion_van,
            evaluacion_satisfaccion
        ]
    })

    st.table(tabla_resultados)

    st.subheader("Resultado CBA")
    st.write(f"Puntaje CBA obtenido: **{datos['idv']} puntos IdV**")

    st.subheader("Recomendación final")
    if datos["viable"]:
        st.success("✅ Viable: se recomienda seleccionar el Método 2: Aporte mixto.")
    else:
        st.error("❌ No viable: no se recomienda este método como alternativa principal.")

    st.write(datos["comentario"])

    st.markdown(
        f"""
        **Interpretación:** Para el proyecto **{nombre_proyecto}**, ubicado en **{direccion}, {distrito}**, el método seleccionado fue **{metodo}**. 
        Este presenta una rentabilidad de **{datos['rentabilidad']}%**, una TIR de **{datos['tir']}%**, un VAN de **{formato_van(datos['van'])}**, 
        un nivel de satisfacción de **{texto_satisfaccion(datos['satisfaccion'])}** y un puntaje CBA de **{datos['idv']} puntos IdV**.
        """
    )

st.divider()
st.caption(
    "Nota: Este prototipo funciona como herramienta demostrativa de apoyo a la toma de decisiones. "
    "Los resultados se actualizan según el método seleccionado y se encuentran alineados con el análisis del caso Green Tower."
)
