import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="SolarExpert Pro", layout="wide")

# --- BASE DE DATOS DE CAPITALES Y HSP (IDEAM/UPME) ---
hsp_data = {
    "Seleccionar": 0, "Leticia": 4.2, "Medellín": 4.2, "Arauca": 5.0, "Barranquilla": 5.5,
    "Bogotá": 4.1, "Bucaramanga": 4.5, "Cali": 4.8, "Cartagena": 5.4, "Florencia": 3.8,
    "Inírida": 4.5, "Mocoa": 3.5, "Neiva": 4.9, "Montería": 5.1, "Pasto": 4.2,
    "Pereira": 4.0, "Popayán": 4.1, "Puerto Carreño": 5.8, "Quibdó": 3.2, "Riohacha": 6.1,
    "San Andrés": 5.7, "San José del Guaviare": 4.2, "Santa Marta": 5.6, "Sincelejo": 5.0,
    "Mitú": 4.0, "Ibagué": 4.6, "Tunja": 4.3, "Villavicencio": 4.1, "Yopal": 4.8,
    "Valledupar": 5.6, "Manizales": 3.9, "Cúcuta": 5.2, "Puerto Inírida": 4.5
}

# --- ESTILO ---
st.markdown("<style>div[data-testid='stMetricValue'] { color: #f39c12; }</style>", unsafe_allow_html=True)

st.title("☀️ SolarExpert Pro: Colombia")

# --- CREACIÓN DE CAPAS (TABS) ---
tab1, tab2, tab3 = st.tabs(["📋 Capa 1: Datos del Proyecto", "📊 Capa 2: Análisis Financiero", "🛠️ Capa 3: Diseño Técnico"])

with tab1:
    st.header("Información Básica")
    col1, col2 = st.columns(2)
    
    with col1:
        nombre_cliente = st.text_input("Nombre del Cotizante", placeholder="Ej: Juan Pérez")
        ciudad = st.selectbox("Ubicación del Proyecto (Capital)", options=list(hsp_data.keys()))
        
        if ciudad != "Seleccionar":
            st.info(f"📍 Horas Solares Pico (HSP) detectadas: **{hsp_data[ciudad]} h/día**")
            hsp = hsp_data[ciudad]
        else:
            hsp = 0

    with col2:
        metodo_consumo = st.radio("¿Cómo ingresarás el consumo?", ["Promedio Directo", "Detalle mes a mes"])
        
        if metodo_consumo == "Promedio Directo":
            consumo_mes = st.number_input("Consumo Mensual Promedio (kWh)", value=300)
        else:
            with st.expander("Ingresar consumos de los últimos 12 meses"):
                meses = [st.number_input(f"Mes {i+1}", value=300) for i in range(12)]
                consumo_mes = sum(meses) / 12
                st.write(f"**Promedio calculado: {consumo_mes:.1f} kWh/mes**")

    st.divider()
    st.header("Configuración de Tarifas y Uso")
    c_a, c_b = st.columns(2)
    
    with c_a:
        tarifa_kwh = st.number_input("Costo del kWh según factura ($ COP)", value=950)
        # Costo por vatio oculto al usuario final pero usado en cálculos
        costo_vatio = 4500 
    
    with c_b:
        autoconsumo_directo = st.slider("% Autoconsumo (Uso directo del sol)", 0, 100, 60)
        st.caption("Predeterminado: 60%. Ajuste según el uso de electrodomésticos en el día.")

# --- CÁLCULOS MOTOR (Background) ---
if ciudad != "Seleccionar" and hsp > 0:
    eficiencia = 0.80
    energia_dia_necesaria = consumo_mes / 30
    kwp_necesario = energia_dia_necesaria / (hsp * eficiencia)
    
    # Datos para las siguientes capas... (Solo se activan si hay ciudad seleccionada)
    with tab2:
        st.warning("Selecciona una ciudad en la Capa 1 para ver el análisis.") if ciudad == "Seleccionar" else st.write(f"Análisis Financiero para {nombre_cliente}...")
        # Aquí iría tu código de barras de retorno y métricas financieras
        
    with tab3:
        st.warning("Selecciona una ciudad en la Capa 1 para ver el diseño.") if ciudad == "Seleccionar" else st.write("Especificaciones Técnicas...")
        # Aquí iría tu código de paneles, área y strings
else:
    st.info("👈 Por favor, completa la **Capa 1** para generar el diseño.")
