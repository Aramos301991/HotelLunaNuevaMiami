import streamlit as st
import pandas as pd
import plotly.express as px

# URLs corregidas (sin '/blob')
mercado_hotelero_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/mercado_hotelero.csv"
submercados_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/submercados.csv"
visitantes_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/visitantes.csv"
financiamiento_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/financiamiento.csv"
marketing_roi_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/marketing_roi.csv"
clientes_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/clientes.csv"
ubicacion_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/ubicacion.csv"

@st.cache_data
def load_data():
    try:
        # Carga los datos
        mercado_hotelero = pd.read_csv(mercado_hotelero_url)
        submercados = pd.read_csv(submercados_url)
        visitantes = pd.read_csv(visitantes_url)
        financiamiento = pd.read_csv(financiamiento_url)
        marketing_roi = pd.read_csv(marketing_roi_url)
        clientes = pd.read_csv(clientes_url)
        ubicacion = pd.read_csv(ubicacion_url)
        
        # Conversión de tipos de datos
        visitantes['Millones'] = visitantes['Millones'].astype(float)
        
        return mercado_hotelero, submercados, visitantes, financiamiento, marketing_roi, clientes, ubicacion
        
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return None, None, None, None, None, None, None

data = load_data()
mercado_hotelero, submercados, visitantes, financiamiento, marketing_roi, clientes, ubicacion = data

# Configuración de la página
st.set_page_config(
    page_title="🌿 Finca Luna Nueva Lodge - Miami",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
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
        values="Porcentaje (%)",  # Nombre exacto de la columna
        title="Distribución por Zona (2025)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Sección 2: Visitantes y Financiamiento ---
st.header("👥 Demanda Turística")
tab1, tab2 = st.tabs(["Visitantes", "Financiamiento"])

with tab1:
    # Convertir millones a formato correcto
    visitantes['Millones'] = visitantes['Millones'] / 1000  # Convierte a millones
    
    fig3 = px.bar(
        visitantes,
        x="Tipo",
        y="Millones",
        color="Tipo",
        title="Turistas en Miami (2023)",
        labels={"Millones": "Visitantes (millones)"}
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.dataframe(
        financiamiento,
        column_config={
            "Fuente": "Fuente de Financiamiento",
            "Tasa (%)": st.column_config.NumberColumn("Tasa de Interés", format="%.2f%%")
        },
        hide_index=True,
        use_container_width=True
    )

# --- Resto de tu código (secciones de clientes, ubicación, etc.) ---
# ... (mantén las otras secciones igual)

# --- Sección 3: Perfil de Clientes ---
if clientes is not None:
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
if ubicacion is not None:
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
if marketing_roi is not None:
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
        if mercado_hotelero is not None:
            st.dataframe(mercado_hotelero)
    with tabs[1]:
        if visitantes is not None:
            st.dataframe(visitantes)
    with tabs[2]:
        if financiamiento is not None:
            st.dataframe(financiamiento)
    with tabs[3]:
        if clientes is not None:
            st.dataframe(clientes)
    with tabs[4]:
        if ubicacion is not None:
            st.dataframe(ubicacion)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Finca Luna Nueva Lodge | Datos actualizados a Mayo 2025")
