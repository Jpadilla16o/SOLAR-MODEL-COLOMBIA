import streamlit as st

# Título y configuración
st.set_page_config(page_title="SolarExpert Colombia", layout="wide")
st.title("☀️ SolarExpert: Analizador de Inversión Fotovoltaica")
st.markdown("---")

# --- COLUMNAS DE ENTRADA ---
col_inputs, col_results = st.columns([1, 2])

with col_inputs:
    st.header("Datos del Proyecto")
    ciudad = st.selectbox("Ubicación", ["Medellín", "Bogotá", "Barranquilla", "Cali"])
    consumo = st.number_input("Consumo mensual (kWh)", value=300)
    tarifa = st.number_input("Costo del kWh ($ COP)", value=950)
    inversion_estimada = st.number_input("Costo del sistema ($ Millones)", value=15.0) * 1_000_000

# --- LÓGICA TÉCNICA Y FINANCIERA ---
hsp_dict = {"Barranquilla": 5.5, "Medellín": 4.2, "Bogotá": 4.1, "Cali": 4.8}
hsp = hsp_dict[ciudad]
generacion_mes = (consumo / 30 / hsp / 0.8) * hsp * 30 * 0.8 # Simplificado para el MVP
ahorro_mes = generacion_mes * tarifa
ahorro_anio = ahorro_mes * 12

# Beneficio Ley 1715 (Deducción 50% Renta en 15 años)
beneficio_anual_renta = (inversion_estimada * 0.5) / 15
retorno_anios = inversion_estimada / (ahorro_anio + beneficio_anual_renta)

# --- COLUMNA DE RESULTADOS ---
with col_results:
    st.header(f"Resultados para {ciudad}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Ahorro Anual Estimado", f"$ {ahorro_anio:,.0f}")
    m2.metric("Beneficio Ley 1715 (Año)", f"$ {beneficio_anual_renta:,.0f}")
    m3.metric("Retorno de Inversión", f"{retorno_anios:.1f} años")
    
    st.info("💡 Este es un cálculo básico. Para un diseño detallado (Helioscope style), consulta a un ingeniero.")
