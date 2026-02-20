import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="SolarExpert Pro Colombia", layout="wide", page_icon="☀️")

# --- BASE DE DATOS DE CAPITALES Y RADIACIÓN (HSP) ---
hsp_data = {
    "Seleccionar": 0, "Leticia": 4.2, "Medellín": 4.2, "Arauca": 5.0, "Barranquilla": 5.5,
    "Bogotá": 4.1, "Bucaramanga": 4.5, "Cali": 4.8, "Cartagena": 5.4, "Florencia": 3.8,
    "Inírida": 4.5, "Mocoa": 3.5, "Neiva": 4.9, "Montería": 5.1, "Pasto": 4.2,
    "Pereira": 4.0, "Popayán": 4.1, "Puerto Carreño": 5.8, "Quibdó": 3.2, "Riohacha": 6.1,
    "San Andrés": 5.7, "San José del Guaviare": 4.2, "Santa Marta": 5.6, "Sincelejo": 5.0,
    "Mitú": 4.0, "Ibagué": 4.6, "Tunja": 4.3, "Villavicencio": 4.1, "Yopal": 4.8,
    "Valledupar": 5.6, "Manizales": 3.9, "Cúcuta": 5.2, "Puerto Inírida": 4.5
}

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #f39c12; font-size: 1.8rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("☀️ SolarExpert Pro: Colombia")
st.markdown("---")

# --- DEFINICIÓN DE CAPAS (TABS) ---
tab1, tab2, tab3 = st.tabs(["📋 Datos del Proyecto", "🛠️ Diseño Técnico", "📊 Análisis Financiero"])

# --- CAPA 1: ENTRADA DE DATOS ---
with tab1:
    st.header("👤 Información de Contacto")
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
        hsp = hsp_data[ciudad]
        if ciudad != "Seleccionar":
            st.success(f"📍 Radiación detectada: **{hsp} Horas Sol Pico (HSP) / día**")

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
    st.header("⚖️ Perfil Tributario y Tarifas")
    c_a, c_b = st.columns(2)
    with c_a:
        tarifa_kwh = st.number_input("Costo del kWh factura ($ COP)", value=950)
        # BOTÓN CLAVE: Lógica Ley 1715
        aplica_ley_1715 = st.checkbox("¿Es declarante de Renta? (Activar beneficio Ley 1715)", value=True)
    with c_b:
        autoconsumo_directo = st.slider("% Autoconsumo (Uso durante el día)", 0, 100, 60)
        st.caption("Nota: Las empresas suelen tener >70% de autoconsumo.")

    st.divider()
    if st.button("💾 Guardar y Registrar Proyecto"):
        if ciudad == "Seleccionar" or nombre_cliente == "" or correo_cliente == "":
            st.error("⚠️ Completa Nombre, Correo y Ciudad.")
        else:
            st.balloons()
            st.success(f"✅ Proyecto de {nombre_cliente} guardado exitosamente.")

# --- LÓGICA DE CÁLCULO MOTOR ---
if ciudad != "Seleccionar" and hsp > 0:
    # 1. Ingeniería básica
    eficiencia = 0.80
    kwp_necesario = (consumo_mes / 30) / (hsp * eficiencia)
    
    # 2. Selección de costo por kWp según escala
    if kwp_necesario < 3:
        costo_kwp = 6000000
    elif 3 <= kwp_necesario < 15:
        costo_kwp = 4600000
    elif 15 <= kwp_necesario < 100:
        costo_kwp = 3750000
    else:
        costo_kwp = 3200000

    # 3. Diseño Técnico
    potencia_panel = 550
    num_paneles = round((kwp_necesario * 1000) / potencia_panel + 0.5)
    area_estimada = num_paneles * 2.6
    peso_estimado = num_paneles * 28
    
    # 4. Cálculos Financieros y Tributarios
    inversion_total = kwp_necesario * costo_kwp
    gen_anual = kwp_necesario * hsp * eficiencia * 365
    
    # Ahorro por energía (Autoconsumo + Excedentes valorados al 60%)
    ahorro_energia_anual = (gen_anual * (autoconsumo_directo/100) * tarifa_kwh) + \
                           (gen_anual * (1 - autoconsumo_directo/100) * tarifa_kwh * 0.6)
    
    # Lógica de Beneficio Tributario (Ley 1715)
    if aplica_ley_1715:
        # Se puede deducir el 50% de la inversión de la renta, máximo en 15 años.
        # Impacto real en caja anual = (Inversión * 0.5 * 0.35) / años_amortización
        beneficio_anual_renta = (inversion_total * 0.5 * 0.35) / 5 # Estimado a 5 años para payback agresivo
    else:
        beneficio_anual_renta = 0

    ahorro_total_anual = ahorro_energia_anual + beneficio_anual_renta
    payback = inversion_total / ahorro_total_anual

    # --- CAPA 2: DISEÑO TÉCNICO ---
    with tab2:
        st.header(f"🛠️ Propuesta Técnica para {nombre_cliente}")
        t1, t2, t3 = st.columns(3)
        t1.metric("Capacidad Total", f"{kwp_necesario:.2f} kWp")
        t2.metric("Paneles", f"{num_paneles} Und", f"{potencia_panel}Wp")
        t3.metric("Espacio", f"{area_estimada:.1f} m²")
        st.divider()
        st.subheader("📋 Resumen de Instalación")
        st.markdown(f"""
        - **Generador:** {num_paneles} módulos de alta eficiencia con certificación RETIE.
        - **Inversor:** Tecnología de cadena (String) optimizada para {ciudad}.
        - **Estructura:** Soportería de aluminio resistente a vientos de hasta 120km/h.
        """)

    # --- CAPA 3: ANÁLISIS FINANCIERO ---
    with tab3:
        st.header(f"💰 Rentabilidad Económica")
        
        f1, f2, f3 = st.columns(3)
        f1.metric("Inversión Total", f"${inversion_total:,.0f} COP")
        f2.metric("Ahorro Anual Proyectado", f"${ahorro_total_anual:,.0f} COP")
        f3.metric("Retorno de Inversión", f"{payback:.1f} Años")

        if aplica_ley_1715:
            st.info(f"💡 El tiempo de retorno incluye un beneficio tributario anual de **${beneficio_anual_renta:,.0f}** por deducción de renta.")

        st.divider()
        
        # Gráfico Cash Flow
        st.subheader("📈 Flujo de Caja Acumulado (10 años)")
        años = list(range(0, 11))
        flujo = [-inversion_total]
        for a in años[1:]:
            flujo.append(flujo[-1] + ahorro_total_anual)
        
        fig_p = go.Figure()
        fig_p.add_trace(go.Bar(x=años, y=flujo, marker_color=['#E74C3C' if v < 0 else '#2ECC71' for v in flujo]))
        fig_p.update_layout(yaxis_title="COP $", xaxis_title="Años")
        st.plotly_chart(fig_p, use_container_width=True)

        # Comparativa Factura
        st.subheader("📉 Ahorro en Factura Mensual")
        factura_actual = consumo_mes * tarifa_kwh
        nueva_factura = factura_actual - (ahorro_energia_anual / 12)
        
        fig_f = go.Figure(data=[
            go.Bar(name='Factura Actual', x=['Escenario'], y=[factura_actual], marker_color='#E74C3C'),
            go.Bar(name='Con Energía Solar', x=['Escenario'], y=[nueva_factura], marker_color='#2ECC71')
        ])
        fig_f.update_layout(barmode='group', yaxis_title="COP $")
        st.plotly_chart(fig_f, use_container_width=True)

else:
    with tab2: st.info("👈 Completa la **Capa 1** para generar el diseño.")
    with tab3: st.info("👈 Completa la **Capa 1** para generar las finanzas.")
