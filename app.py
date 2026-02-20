import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
import math
#from fpdf import FPDF
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
            st.caption("Dato basado en promedios históricos IDEAM/UPME.")
        else:
            st.warning("Selecciona una ciudad para ver la radiación.")

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
    if kwp_necesario < 3: costo_kwp = 6500000
    elif 3 <= kwp_necesario < 15: costo_kwp = 5000000
    elif 15 <= kwp_necesario < 100: costo_kwp = 4000000
    else: costo_kwp = 3800000

    # Ingeniería Detallada (Actualizada con math.ceil)
    potencia_panel = 550
    num_paneles = math.ceil((kwp_necesario * 1000) / potencia_panel)
    
    area_neta_paneles = num_paneles * 2.6
    area_mantenimiento = area_neta_paneles * 0.15
    area_total_estimada = area_neta_paneles + area_mantenimiento
    
    # Peso con Factor de Seguridad del 20%
    peso_nominal = num_paneles * 28
    peso_diseno_seguridad = peso_nominal * 1.2
    carga_distribuida = peso_diseno_seguridad / area_neta_paneles
    
    # Finanzas Detalladas
    inversion_total = kwp_necesario * costo_kwp
    gen_anual = kwp_necesario * hsp * eficiencia * 365
    ahorro_energia_anual = (gen_anual * (autoconsumo_directo/100) * tarifa_kwh) + \
                           (gen_anual * (1 - autoconsumo_directo/100) * tarifa_kwh * 0.6)
    beneficio_anual_renta = (inversion_total * 0.5 * 0.35) / 5 if aplica_ley_1715 else 0
    ahorro_total_anual = ahorro_energia_anual + beneficio_anual_renta
    payback = inversion_total / ahorro_total_anual

    # Impacto Ambiental (Nuevos Cálculos)
    co2_evitado_anual = gen_anual * 0.126 
    arboles_equivalentes = co2_evitado_anual / 20

    with tab2:
        st.header(f"🛠️ Propuesta Técnica para {nombre_cliente}")
        t1, t2, t3 = st.columns(3)
        t1.metric("Capacidad Total", f"{kwp_necesario:.2f} kWp")
        t2.metric("Paneles Necesarios", f"{num_paneles} Und", f"{potencia_panel}Wp")
        t3.metric("Espacio Requerido", f"{area_total_estimada:.1f} m²", help="Incluye 15% de área de mantenimiento.")
        
        st.divider()

        # --- GRÁFICO DINÁMICO DE DISTRIBUCIÓN ---
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
            st.subheader("🏗️ Detalles de Carga y Seguridad")
            st.markdown(f"""
            - **Peso Total (con FS 20%):** ~{peso_diseno_seguridad:.0f} kg.
            - **Carga Distribuida:** {carga_distribuida:.2f} kg/m².
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
        nueva_factura = factura_actual - (ahorro_energia_anual / 12)
        
        fig_f = go.Figure(data=[
            go.Bar(name='Factura Actual', x=['Escenario'], y=[factura_actual], marker_color='#E74C3C'),
            go.Bar(name='Con Energía Solar', x=['Escenario'], y=[nueva_factura], marker_color='#2ECC71')
        ])
        fig_f.update_layout(barmode='group', yaxis_title="Costo Mensual (COP $)")
        st.plotly_chart(fig_f, use_container_width=True)

        # --- SECCIÓN DE IMPACTO AMBIENTAL ---
        st.divider()
        st.subheader("🌿 Impacto Ambiental Estimado")
        ia1, ia2, ia3 = st.columns(3)
        ia1.metric("CO2 Evitado", f"{co2_evitado_anual:,.1f} kg/año", "♻️")
        ia2.metric("Árboles equiv.", f"{arboles_equivalentes:.0f} Und", "🌳")
        ia3.metric("Gen. Limpia", f"{gen_anual:,.0f} kWh/año", "☀️")

        # --- EXPORTACIÓN A PDF ---
        st.divider()
        datos_pdf = {
            "Cliente": nombre_cliente,
            "Ciudad": ciudad,
            "Capacidad Sistema": f"{kwp_necesario:.2f} kWp",
            "Número de Paneles": num_paneles,
            "Inversión Estimada": f"${inversion_total:,.0f} COP",
            "Payback": f"{payback:.1f} años",
            "CO2 evitado": f"{co2_evitado_anual:.1f} kg/año"
        }
        
        pdf_bytes = generar_pdf(datos_pdf)
        st.download_button(
            label="📄 Descargar Propuesta en PDF",
            data=pdf_bytes,
            file_name=f"Propuesta_Solar_{nombre_cliente.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

else:
    with tab2: st.warning("🔒 Registra los datos del proyecto en la Capa 1 para ver el diseño técnico.")
    with tab3: st.warning("🔒 Registra los datos del proyecto en la Capa 1 para ver el análisis financiero.")
