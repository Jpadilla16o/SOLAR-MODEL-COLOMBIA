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
tab1, tab2, tab3 = st.tabs(["📋 Datos del Proyecto", "📊 Análisis Financiero", "🛠️ Diseño Técnico"])

with tab1:
    st.header("👤 Información de Contacto")
    # Nueva fila para datos personales
    c_nom, c_mail, c_tel = st.columns([2, 2, 1])
    
    with c_nom:
        nombre_cliente = st.text_input("Nombre del Cotizante", placeholder="Ej: Juan Pérez")
    with c_mail:
        correo_cliente = st.text_input("Correo Electrónico", placeholder="juan@ejemplo.com")
    with c_tel:
        telefono_cliente = st.text_input("WhatsApp / Celular", placeholder="300 123 4567")

    st.divider()
    st.header("📍 Ubicación y Consumo")
    col1, col2 = st.columns(2)
    
    with col1:
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
    st.header("⚙️ Configuración Económica")
    c_a, c_b = st.columns(2)
    
    with c_a:
        tarifa_kwh = st.number_input("Costo del kWh según factura ($ COP)", value=950)
        costo_vatio = 4500 # Valor interno para cálculos financieros
    
    with c_b:
        autoconsumo_directo = st.slider("% Autoconsumo (Uso directo del sol)", 0, 100, 60)
        st.caption("Predeterminado: 60%. Energía que consumes mientras hay sol.")

    st.divider()
    st.subheader("💾 Gestión del Proyecto")
    
    if st.button("Guardar y Registrar Proyecto"):
        # Validación de campos obligatorios
        if ciudad == "Seleccionar" or nombre_cliente == "" or correo_cliente == "":
            st.error("❌ Por favor completa Nombre, Correo y Ciudad antes de guardar.")
        else:
            st.balloons()
            st.success(f"✅ ¡Proyecto de {nombre_cliente} guardado exitosamente!")
            # Aquí quedan listos los datos para tu futura base de datos
            st.write(f"Registro: {correo_cliente} | {telefono_cliente} | {ciudad}")

# --- CÁLCULOS MOTOR ---
if ciudad != "Seleccionar" and hsp > 0:
    # Ingeniería básica
    eficiencia = 0.80
    kwp_necesario = (consumo_mes / 30) / (hsp * eficiencia)
    inversion_total = (kwp_necesario * 1000) * costo_vatio
    
    with tab2:
        st.header(f"📊 Análisis Financiero: {nombre_cliente}")
        # Aquí puedes añadir el gráfico de barras que hicimos antes
        st.write("Cálculos procesados. Listo para mostrar ROI y flujo de caja.")
        
    with tab3:
        st.header("🛠️ Especificaciones Técnicas")
        # Aquí irá el número de paneles, área y configuración de strings
        st.write(f"Sistema sugerido: **{kwp_necesario:.2f} kWp**")
else:
    with tab2:
        st.info("👈 Por favor, completa la **Capa 1** para ver el análisis financiero.")
    with tab3:
        st.info("👈 Por favor, completa la **Capa 1** para ver el diseño técnico.")
