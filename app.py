import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
import math
from fpdf import FPDF
import base64

# Configuración de página
st.set_page_config(page_title="SolarCol Pro", layout="wide", page_icon="☀️")

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

# --- FUNCIONES DE APOYO ---
def es_correo_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email)

def generar_pdf(datos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Propuesta Técnica-Económica SolarCol Pro", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for clave, valor in datos.items():
        pdf.cell(200, 10, txt=f"{clave}: {valor}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

if 'registro_exitoso' not in st.session_state:
    st.session_state.registro_exitoso = False

st.title("☀️ SolarCol Pro by Josejaime Padilla")
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
        if ciudad != "Seleccionar":
            st.info(f"☀️ Horas Solares Pico (HSP) para **{ciudad}**: **{hsp} h/día**")
        else:
            st.warning("Selecciona una ciudad para ver la radiación.")

    with col2:
        consumo_mes = st.number_input("Consumo Mensual Promedio (kWh)", value=300)
        tarifa_kwh = st.number_input("Costo del kWh factura ($ COP)", value=950)

    st.divider()
    st.header("⚖️ Configuración Adicional")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write("**¿Declara Renta? (Ley 1715)**")
        seleccion_renta = st.radio(
            "Seleccione:",
            ["Sí, soy declarante", "No declaro renta"],
            index=1,
            horizontal=True,
            label_visibility="collapsed"
        )
        aplica_ley_1715 = True if seleccion_renta == "Sí, soy declarante" else False
        if aplica_ley_1715:
            st.caption("✨ *Incluye incentivos fiscales en el ahorro.*")
        else:
            st.caption("ℹ️ *Análisis basado únicamente en ahorro energético.*")

    with c_b:
        # Dejado en 95% como estándar inicial solicitado
        autoconsumo_directo = st.slider("% Autoconsumo (Ahorro 1 a 1)", 0, 100, 95)

    st.divider()
    if st.button("💾 Guardar y Registrar Proyecto", use_container_width=True, type="primary"):
        if not nombre_cliente or not es_correo_valido(correo_cliente) or len(telefono_cliente) < 10 or ciudad == "Seleccionar":
            st.error("❌ Por favor completa todos los campos correctamente.")
            st.session_state.registro_exitoso = False
        else:
            st.session_state.registro_exitoso = True
            st.balloons()
            st.success("✅ Registro exitoso. Resultados desbloqueados.")

# --- LÓGICA DE CÁLCULO ---
if st.session_state.registro_exitoso:
    eficiencia = 0.80
    kwp_teorico = (consumo_mes / 30) / (hsp * eficiencia)
    
    potencia_panel = 550
    num_paneles = math.ceil((kwp_teorico * 1000) / potencia_panel)
    kwp_instalado = (num_paneles * potencia_panel) / 1000
    
    # Estructura de costos protegida
    if kwp_instalado <= 3.5:
        inversion_total = 12000000 + (kwp_instalado * 3200000)
    elif 3.5 < kwp_instalado <= 10:
        inversion_total = kwp_instalado * 6400000
    elif 10 < kwp_instalado <= 50:
        inversion_total = kwp_instalado * 4900000
    else:
        inversion_total = kwp_instalado * 3900000

    area_neta_paneles = num_paneles * 2.6
    area_mantenimiento = area_neta_paneles * 0.15
    area_total_estimada = area_neta_paneles + area_mantenimiento
    
    peso_nominal = num_paneles * 28
    peso_diseno_seguridad = peso_nominal * 1.2
    carga_distribuida = peso_diseno_seguridad / area_neta_paneles
    
    # Finanzas (Considerando esquema de medición neta casi 1 a 1)
    gen_anual = kwp_instalado * hsp * eficiencia * 365
    
    # El slider ahora actúa como un factor de ajuste de eficiencia económica
    # 95-100% es ahorro pleno. Valores menores castigan el excedente.
    factor_remuneracion_excedente = 0.75 # Ajustado un poco más alto para Colombia
    ahorro_energia_anual = (gen_anual * (autoconsumo_directo/100) * tarifa_kwh) + \
                           (gen_anual * (1 - autoconsumo_directo/100) * tarifa_kwh * factor_remuneracion_excedente)
    
    beneficio_anual_renta = (inversion_total * 0.5 * 0.35) / 5 if aplica_ley_1715 else 0
    ahorro_total_anual = ahorro_energia_anual + beneficio_anual_renta
    payback = inversion_total / ahorro_total_anual

    co2_evitado_anual = gen_anual * 0.126 
    arboles_equivalentes = co2_evitado_anual / 20

    with tab2:
        st.header(f"🛠️ Propuesta Técnica para {nombre_cliente}")
        t1, t2, t3 = st.columns(3)
        t1.metric("Capacidad Instalada", f"{kwp_instalado:.2f} kWp")
        t2.metric("Paneles Necesarios", f"{num_paneles} Und", f"{potencia_panel}Wp")
        t3.metric("Espacio Requerido", f"{area_total_estimada:.1f} m²")
        
        st.divider()
        st.subheader("📐 Distribución de Espacio Sugerida")
        df_espacio = pd.DataFrame({
            "Categoría": ["Paneles (Generación)", "Pasillos (Mantenimiento)"],
            "Padre": ["Área Total", "Área Total"],
            "Metros": [area_neta_paneles, area_mantenimiento]
        })
        fig_area = px.treemap(
            df_espacio, path=["Padre", "Categoría"], values="Metros",
            color="Categoría", color_discrete_map={"Paneles (Generación)": "#1f77b4", "Pasillos (Mantenimiento)": "#a6cee3"}
        )
        fig_area.update_traces(textinfo="label+value", texttemplate="%{label}<br>%{value:.1f} m²")
        fig_area.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=300)
        st.plotly_chart(fig_area, use_container_width=True)

    with tab3:
        st.header(f"💰 Rentabilidad Económica: {nombre_cliente}")
        f1, f2, f3 = st.columns(3)
        f1.metric("Inversión Total", f"${inversion_total:,.0f} COP")
        f2.metric("Ahorro Anual Estimado", f"${ahorro_total_anual:,.0f} COP")
        f3.metric("Payback (Retorno)", f"{payback:.1f} Años")
        
        st.divider()
        st.subheader("📈 Flujo de Caja Acumulado (10 años)")
        años = list(range(0, 11))
        flujo = [-inversion_total]
        for a in años[1:]: flujo.append(flujo[-1] + ahorro_total_anual)
        fig_p = go.Figure(data=[go.Bar(x=años, y=flujo, marker_color=['#E74C3C' if v < 0 else '#2ECC71' for v in flujo])])
        st.plotly_chart(fig_p, use_container_width=True)
        
        st.divider()
        st.subheader("🌿 Impacto Ambiental")
        ia1, ia2, ia3 = st.columns(3)
        ia1.metric("CO2 Evitado", f"{co2_evitado_anual:,.1f} kg/año")
        ia2.metric("Árboles equiv.", f"{arboles_equivalentes:.0f} Und")
        ia3.metric("Generación Anual", f"{gen_anual:,.0f} kWh")

        st.divider()
        pdf_bytes = generar_pdf({
            "Cliente": nombre_cliente,
            "Ciudad": ciudad,
            "Capacidad": f"{kwp_instalado:.2f} kWp",
            "Inversión": f"${inversion_total:,.0f} COP",
            "Payback": f"{payback:.1f} años"
        })
        st.download_button(label="📄 Descargar Propuesta en PDF", data=pdf_bytes, file_name=f"Propuesta_{nombre_cliente}.pdf", mime="application/pdf", use_container_width=True)

else:
    with tab2: st.warning("🔒 Registra los datos del proyecto para ver el diseño técnico.")
    with tab3: st.warning("🔒 Registra los datos del proyecto para ver el análisis financiero.")
