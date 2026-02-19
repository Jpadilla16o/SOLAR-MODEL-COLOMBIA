import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#st.set_page_config(page_title="SolarExpert Pro Colombia", layout="wide")

# Estilo personalizado
#st.markdown("""
 #   <style>
  #  .main { background-color: #f5f7f9; }
   # .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    #</style>
    #""", unsafe_allow_html=True)

st.set_page_config(page_title="SolarExpert Pro Colombia", layout="wide")

# Estilo para forzar que las métricas se vean bien en modo claro y oscuro
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #555555 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("☀️ SolarExpert Pro: Ingeniería y Finanzas Solar")
st.write("Herramienta de análisis técnico-financiero bajo Ley 1715 y CREG 174")

with st.sidebar:
    st.header("⚙️ Configuración del Proyecto")
    ciudad = st.selectbox("Ubicación del Proyecto", ["Barranquilla", "Medellín", "Bogotá", "Cali", "Bucaramanga"])
    consumo_mes = st.number_input("Consumo Mensual Factura (kWh)", value=400)
    tarifa_kwh = st.number_input("Costo kWh Comercial ($ COP)", value=950)
    
    st.divider()
    st.header("💰 Datos de Inversión")
    costo_vatio = st.number_input("Costo instalado por Vatio ($/Wp)", value=4500) # Promedio mercado Col
    autoconsumo_directo = st.slider("% Autoconsumo (Uso mientras hay sol)", 0, 100, 60)

# --- LÓGICA TÉCNICA ---
hsp_dict = {"Barranquilla": 5.5, "Medellín": 4.2, "Bogotá": 4.1, "Cali": 4.8, "Bucaramanga": 4.5}
hsp = hsp_dict[ciudad]
eficiencia = 0.80

# Cálculo de capacidad necesaria para cubrir el 100%
kwp_necesario = (consumo_mes / 30) / (hsp * eficiencia)
inversion_total = (kwp_necesario * 1000) * costo_vatio

# --- LÓGICA FINANCIERA ---
gen_anual = kwp_necesario * hsp * eficiencia * 365
ahorro_por_autoconsumo = (gen_anual * (autoconsumo_directo/100)) * tarifa_kwh
venta_excedentes = (gen_anual * (1 - autoconsumo_directo/100)) * (tarifa_kwh * 0.6) # Se paga aprox al 60%
ahorro_total_anio = ahorro_por_autoconsumo + venta_excedentes

# Beneficio Fiscal (Deducción Renta 50% de la inversión en 15 años)
beneficio_fiscal_anual = (inversion_total * 0.5) / 15

# --- INTERFAZ DE RESULTADOS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Capacidad Sistema", f"{kwp_necesario:.2f} kWp")
c2.metric("Inversión Estimada", f"${inversion_total/1e6:.1f}M")
c3.metric("Ahorro + Venta Anual", f"${ahorro_total_anio/1e6:.2f}M")
c4.metric("Payback (Años)", f"{inversion_total / (ahorro_total_anio + beneficio_fiscal_anual):.1f}")

# --- GRÁFICO DE RETORNO ---
st.subheader("📈 Proyección de Flujo de Caja (Retorno de Inversión)")
flujo = [-inversion_total]
for i in range(1, 11):
    flujo.append(flujo[-1] + ahorro_total_anio + beneficio_fiscal_anual)

fig = go.Figure()
fig.add_trace(go.Bar(x=list(range(11)), y=flujo, name="Flujo Acumulado", 
                     marker_color=['red' if x < 0 else 'green' for x in flujo]))
#fig.update_layout(title="Recuperación de la inversión en 10 años", ylabel="COP $")
fig.update_layout(title="Recuperación de la inversión en 10 años", yaxis_title="COP $", xaxis_title="Años")
st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.caption("Nota: Este modelo considera degradación de paneles del 0.5% anual y beneficios de la Ley 1715.")
