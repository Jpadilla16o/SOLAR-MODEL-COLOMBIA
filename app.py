import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re # Librería para validar el formato de correo

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

# --- FUNCIÓN PARA VALIDAR CORREO ---
def es_correo_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email)

# --- INICIALIZACIÓN DEL ESTADO ---
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
            st.caption("⚠️ Formato de correo inválido (ejemplo@dominio.com)")
    
    with c_tel:
        # Teléfono con prefijo Colombia predeterminado
        col_prefijo, col_num = st.columns([1, 2.5])
        with col_prefijo:
            prefijo = st.text_input("País", value="+57", disabled=True)
        with col_num:
            telefono_cliente = st.text_input("Celular (10 dígitos)", placeholder="300 123 4567", max_chars=10)
            if telefono_cliente and (not telefono_cliente.isdigit() or len(telefono_cliente) < 10):
                st.caption("⚠️ Ingresa 10 números")

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
    # LÓGICA DE VALIDACIÓN ANTES DE GUARDAR
    if st.button("💾 Guardar y Registrar Proyecto"):
        errores = []
        if not nombre_cliente: errores.append("Nombre")
        if not es_correo_valido(correo_cliente): errores.append("Correo válido")
        if not (telefono_cliente.isdigit() and len(telefono_cliente) == 10): errores.append("Celular (10 dígitos)")
        if ciudad == "Seleccionar": errores.append("Ciudad")

        if errores:
            st.error(f"❌ Revisa los siguientes campos: {', '.join(errores)}")
            st.session_state.registro_exitoso = False
        else:
            st.session_state.registro_exitoso = True
            st.balloons()
            st.success(f"✅ ¡Registro completo! Resultados técnicos y financieros desbloqueados.")

# --- MOSTRAR RESULTADOS SI ESTÁ REGISTRADO ---
if st.session_state.registro_exitoso:
    # (El resto del código de cálculos, tab2 y tab3 se mantiene igual)
    # Copia aquí la lógica de cálculos y contenido de tab2/tab3 de la v3.5
    eficiencia = 0.80
    kwp_necesario = (consumo_mes / 30) / (hsp * eficiencia)
    
    # Precios escalonados
    if kwp_necesario < 3: costo_kwp = 6000000
    elif 3 <= kwp_necesario < 15: costo_kwp = 4600000
    elif 15 <= kwp_necesario < 100: costo_kwp = 3750000
    else: costo_kwp = 3200000

    inversion_total = kwp_necesario * costo_kwp
    gen_anual = kwp_necesario * hsp * eficiencia * 365
    ahorro_energia_anual = (gen_anual * (autoconsumo_directo/100) * tarifa_kwh) + \
                           (gen_anual * (1 - autoconsumo_directo/100) * tarifa_kwh * 0.6)
    beneficio_anual_renta = (inversion_total * 0.5 * 0.35) / 5 if aplica_ley_1715 else 0
    ahorro_total_anual = ahorro_energia_anual + beneficio_anual_renta
    payback = inversion_total / ahorro_total_anual

    with tab2:
        st.header(f"🛠️ Diseño Técnico: {nombre_cliente}")
        t1, t2, t3 = st.columns(3)
        t1.metric("Capacidad Total", f"{kwp_necesario:.2f} kWp")
        t2.metric("Paneles (550Wp)", f"{round((kwp_necesario*1000)/550 + 0.5)} Und")
        t3.metric("Área Estimada", f"{((kwp_necesario*1000)/550)*2.6:.1f} m²")
        

    with tab3:
        st.header(f"💰 Análisis Financiero: {nombre_cliente}")
        f1, f2, f3 = st.columns(3)
        f1.metric("Inversión Total", f"${inversion_total:,.0f}")
        f2.metric("Ahorro Anual", f"${ahorro_total_anual:,.0f}")
        f3.metric("Payback", f"{payback:.1f} Años")
        
        años = list(range(0, 11))
        flujo = [-inversion_total]
        for a in años[1:]: flujo.append(flujo[-1] + ahorro_total_anual)
        fig = go.Figure(data=[go.Bar(x=años, y=flujo, marker_color=['#E74C3C' if v < 0 else '#2ECC71' for v in flujo])])
        st.plotly_chart(fig, use_container_width=True)
        

else:
    with tab2: st.warning("🔒 Registra tus datos para ver el diseño técnico.")
    with tab3: st.warning("🔒 Registra tus datos para ver el análisis financiero.")
