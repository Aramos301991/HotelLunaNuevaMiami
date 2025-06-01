import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Configuración de la página (debe ir antes de cualquier otro st.*)
st.set_page_config(
    page_title="🌿 Finca Luna Nueva Lodge - Miami",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌐 URLs de los archivos CSV en GitHub Raw
mercado_hotelero_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/mercado_hotelero.csv"
submercados_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/submercados.csv"
visitantes_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/ubicacion.csv"
financiamiento_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/financiamiento.csv"
marketing_roi_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/marketing_roi.csv"
clientes_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/clientes.csv"
ubicacion_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/ubicacion.csv"

# 📥 Carga de datos desde GitHub
@st.cache_data
def load_data():
    try:
        mercado_hotelero = pd.read_csv(mercado_hotelero_url, encoding="latin1")
        submercados = pd.read_csv(submercados_url, encoding="latin1")
        visitantes = pd.read_csv(visitantes_url, encoding="latin1")
        financiamiento = pd.read_csv(financiamiento_url, encoding="latin1")
        marketing_roi = pd.read_csv(marketing_roi_url, encoding="latin1")
        clientes = pd.read_csv(clientes_url, encoding="latin1")
        ubicacion = pd.read_csv(ubicacion_url, encoding="latin1")
        return mercado_hotelero, submercados, visitantes, financiamiento, marketing_roi, clientes, ubicacion
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None, None, None, None


# ✅ Carga los datos
data = load_data()
mercado_hotelero, submercados, visitantes, financiamiento, marketing_roi, clientes, ubicacion = data

# 🏷️ Título principal
st.title("Finca Luna Nueva Lodge - Expansión a Miami")
st.markdown("Dashboard interactivo para el análisis de mercado y estrategia de expansión")

# --- Sección 1: Mercado Hotelero ---
st.header("📊 Mercado Hotelero en Miami")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        mercado_hotelero,
        x="Año",
        y="Habitaciones",
        title="Inventario de Habitaciones (2023-2025)",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        submercados,
        names="Zona",
        values="Porcentaje (%)",
        title="Distribución por Zona (2025)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Sección 2: Visitantes y Financiamiento ---
st.header("👥 Demanda Turística")
tab1, tab2 = st.tabs(["Visitantes", "Financiamiento"])

with tab1:
    fig3 = px.bar(
        visitantes,
        x="Tipo",
        y="Millones",
        color="Tipo",
        title="Turistas en Miami (2023)"
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.dataframe(
        financiamiento,
        column_config={
            "Fuente": "Fuente de Financiamiento",
            "Tasa (%)": st.column_config.NumberColumn("Tasa de Interés", format="%.2f%%")
        },
        hide_index=True
    )

# --- Sección 3: Perfil de Clientes ---
st.header("🎯 Segmentación de Clientes")
st.dataframe(
    clientes,
    column_config={
        "Categoría": "Perfil",
        "Detalle": "Características"
    },
    hide_index=True,
    use_container_width=True
)

# --- Sección 4: Ubicación (Redland) ---
st.header("📍 Ubicación Propuesta: Redland")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ventajas Clave")
    st.dataframe(
        ubicacion[ubicacion['Variable'].str.contains('Ventaja')],
        column_config={
            "Variable": "Beneficio",
            "Valor": "Detalle"
        },
        hide_index=True
    )

with col2:
    st.subheader("Consideraciones")
    st.dataframe(
        ubicacion[ubicacion['Variable'].str.contains('Desafío|Requisito')],
        column_config={
            "Variable": "Aspecto",
            "Valor": "Detalle"
        },
        hide_index=True
    )

# --- Sección 5: Estrategias de Marketing ---
st.header("📈 ROI por Red Social")
fig4 = px.bar(
    marketing_roi,
    x="Red Social",
    y="ROI (%)",
    color="Ingresos Generados (USD)",
    title="Retorno de Inversión por Plataforma (2025)"
)
st.plotly_chart(fig4, use_container_width=True)

# --- Datos completos (opcional) ---
with st.expander("📁 Ver todos los datos crudos"):
    tabs = st.tabs(["Mercado Hotelero", "Visitantes", "Financiamiento", "Clientes", "Ubicación"])
    with tabs[0]:
        st.dataframe(mercado_hotelero)
    with tabs[1]:
        st.dataframe(visitantes)
    with tabs[2]:
        st.dataframe(financiamiento)
    with tabs[3]:
        st.dataframe(clientes)
    with tabs[4]:
        st.dataframe(ubicacion)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Finca Luna Nueva Lodge | Datos actualizados a Mayo 2025")
