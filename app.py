import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

# Configuración de página
st.set_page_config(page_title="SolarExpert Pro Colombia", layout="wide", page_icon="☀️")

# --- BASE DE DATOS HSP ---
hsp_data = {
    "Seleccionar": 0, "Leticia": 4.2, "Medellín": 4.2, "Arauca": 5.0, "Barranquilla": 5.5,
    "Bogotá": 4.1, "Bucaramanga": 4.5, "Cali": 4.8, "Cartagena": 5.4, "Florencia": 3.8,
    "Inírida": 4.5, "Mocoa": 3.5, "Neiva": 4.9, "Montería": 5.1, "Pasto": 4.2,
    "Pereira": 4.0, "Popayán": 4.1, "Puerto Carreño": 5.8, "Quibdó": 3.2, "Riohacha": 6.1,
    "San Andrés": 5.7, "San José del Guaviare": 4.2, "Santa Marta": 5.6, "Sincelejo": 5.0,
    "Mitú": 4.0, "Ibagué": 4.6, "Tunja": 4.3, "Villavicencio": 4.1, "Yopal": 4.8,
    "Valledupar": 5.6, "Manizales": 3.9, "Cúcuta": 5.2, "Puerto Inírida": 4.5
}

# --- VALIDACIONES ---
def es_correo_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email)

if 'registro_exitoso' not in st.session_state:
    st.session_state.registro_exitoso = False

st.title("☀️ SolarExpert Pro: Colombia")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 Datos del Proyecto", "🛠️ Diseño Técnico", "📊 Análisis Financiero"])

with tab1:
    st.header("👤 Información de Contacto")
    c_nom, c_mail, c_tel = st.columns([2, 2, 1.5])
    with c_nom:
        nombre_cliente = st.text_input("Nombre del Cotizante", placeholder="Ej: Juan Pérez")
    with c_mail:
        correo_cliente = st.text_input("Correo Electrónico", placeholder="ejemplo@correo.com")
        if correo_cliente and not es_correo_valido(correo_cliente):
            st.caption("⚠️ Formato de correo inválido")
    with c_tel:
        col_prefijo, col_num = st.columns([1, 2.5])
        with col_prefijo: st.text_input("País", value="+57", disabled=True)
        with col_num:
            telefono_cliente = st.text_input("Celular (10 dígitos)", placeholder="3001234567", max_chars=10)

    st.divider()
    st.header("📍 Ubicación y Consumo")
    col1, col2 = st.columns(2)
    with col1:
        ciudad = st.selectbox("Ubicación del Proyecto (Capital)", options=list(hsp_data.keys()))
        hsp = hsp_data[ciudad]
    with col2:
        consumo_mes = st.number_input("Consumo Mensual Promedio (kWh)", value=300)
        tarifa_kwh = st.number_input("Costo del kWh factura ($ COP)", value=950)

    st.divider()
    st.header("⚖️ Configuración Adicional")
    c_a, c_b = st.columns(2)
    with c_a:
        aplica_ley_1715 = st.checkbox("¿Es declarante de Renta? (Ley 1715)", value=True)
    with c_b:
        autoconsumo_directo = st.slider("% Autoconsumo", 0, 100, 60)

    st.divider()
    if st.button("💾 Guardar y Registrar Proyecto"):
        if not nombre_cliente or not es_correo_valido(correo_cliente) or len(telefono_cliente) < 10 or ciudad == "Seleccionar":
            st.error("❌ Por favor completa todos los campos correctamente.")
            st.session_state.registro_exitoso = False
        else:
            st.session_state.registro_exitoso = True
            st.balloons()
            st.success("✅ Registro exitoso. Resultados desbloqueados.")

# --- LÓGICA DE CÁLCULO Y RESULTADOS ---
if st.session_state.registro_exitoso:
    # MOTOR DE CÁLCULO
    eficiencia = 0.80
    kwp_necesario = (consumo_mes / 30) / (hsp * eficiencia)
    
    # Precios escalonados
    if kwp_necesario < 3: costo_kwp = 6000000
    elif 3 <= kwp_necesario < 15: costo_kwp = 4600000
    elif 15 <= kwp_necesario < 100: costo_kwp = 3750000
    else: costo_kwp = 3200000

    # Ingeniería Detallada
    potencia_panel = 550
    num_paneles = round((kwp_necesario * 1000) / potencia_panel + 0.5)
    area_estimada = num_paneles * 2.6
    peso_estimado = num_paneles * 28
    
    # Finanzas Detalladas
    inversion_total = kwp_necesario * costo_kwp
    gen_anual = kwp_necesario * hsp * eficiencia * 365
    ahorro_energia_anual = (gen_anual * (autoconsumo_directo/100) * tarifa_kwh) + \
                           (gen_anual * (1 - autoconsumo_directo/100) * tarifa_kwh * 0.6)
    beneficio_anual_renta = (inversion_total * 0.5 * 0.35) / 5 if aplica_ley_1715 else 0
    ahorro_total_anual = ahorro_energia_anual + beneficio_anual_renta
    payback = inversion_total / ahorro_total_anual

    with tab2:
        st.header(f"🛠️ Propuesta Técnica para {nombre_cliente}")
        t1, t2, t3 = st.columns(3)
        t1.metric("Capacidad Total", f"{kwp_necesario:.2f} kWp")
        t2.metric("Paneles Necesarios", f"{num_paneles} Und", f"{potencia_panel}Wp")
        t3.metric("Espacio en Techo", f"{area_estimada:.1f} m²")
        
        
        
        st.divider()
        col_ta, col_tb = st.columns(2)
        with col_ta:
            st.subheader("⚡ Componentes")
            st.markdown(f"""
            - **Inversor Sugerido:** {"Monofásico" if kwp_necesario < 8 else "Trifásico"} de {kwp_necesario:.1f} kW.
            - **Tecnología:** Módulos Tier 1 Monocristalinos N-Type.
            - **Estructura:** Aluminio anodizado 6005-T5.
            """)
        with col_tb:
            st.subheader("🏗️ Detalles de Carga")
            st.markdown(f"""
            - **Peso en Cubierta:** ~{peso_estimado:.0f} kg.
            - **Certificaciones:** RETIE / IEC 61215.
            - **Garantía Inversor:** 10-12 años.
            """)

    with tab3:
        st.header(f"💰 Rentabilidad Económica: {nombre_cliente}")
        f1, f2, f3 = st.columns(3)
        f1.metric("Inversión Total", f"${inversion_total:,.0f} COP")
        f2.metric("Ahorro Anual (Energía+Renta)", f"${ahorro_total_anual:,.0f} COP")
        f3.metric("Tiempo de Retorno", f"{payback:.1f} Años")
        
        st.divider()
        st.subheader("📈 Proyección de Flujo de Caja (10 años)")
        años = list(range(0, 11))
        flujo = [-inversion_total]
        for a in años[1:]: flujo.append(flujo[-1] + ahorro_total_anual)
        
        fig_p = go.Figure(data=[go.Bar(x=años, y=flujo, marker_color=['#E74C3C' if v < 0 else '#2ECC71' for v in flujo])])
        fig_p.update_layout(yaxis_title="Flujo Acumulado (COP $)", xaxis_title="Años")
        st.plotly_chart(fig_p, use_container_width=True)
        
        

        st.subheader("📉 Comparativa de Factura Mensual")
        factura_actual = consumo_mes * tarifa_kwh
        nueva_factura =
