import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración DEBE SER PRIMERO
st.set_page_config(
    page_title="🌿 Finca Luna Nueva Lodge - Miami",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URLs corregidas (sin '/blob')
base_url = "https://raw.githubusercontent.com/Aramos301991/HotelLunaNuevaMiami/main/"
urls = {
    "mercado_hotelero": base_url + "mercado_hotelero.csv",
    "submercados": base_url + "submercados.csv",
    "visitantes": base_url + "visitantes.csv",
    "financiamiento": base_url + "financiamiento.csv",
    "marketing_roi": base_url + "marketing_roi.csv",
    "clientes": base_url + "clientes.csv",
    "ubicacion": base_url + "ubicacion.csv"
}

@st.cache_data
def load_data():
    data = {}
    try:
        for name, url in urls.items():
            # Lee con codificación explícita y manejo de errores
            data[name] = pd.read_csv(url, encoding='utf-8', on_bad_lines='skip')
            
            if data[name].empty:
                st.error(f"⚠️ El archivo {name}.csv está vacío o no se pudo leer")
                return None
            
        # Conversiones y validaciones específicas
        data['visitantes']['Millones'] = pd.to_numeric(data['visitantes']['Millones'], errors='coerce')
        data['submercados']['Porcentaje (%)'] = pd.to_numeric(data['submercados']['Porcentaje (%)'], errors='coerce')
        data['financiamiento']['Tasa (%)'] = pd.to_numeric(data['financiamiento']['Tasa (%)'], errors='coerce')
        
        return data
        
    except Exception as e:
        st.error(f"❌ Error crítico cargando datos: {str(e)}")
        return None

# ---------------------------
# INTERFAZ PRINCIPAL
# ---------------------------

st.title("🏨 Finca Luna Nueva Lodge - Expansión a Miami")
st.markdown("### Dashboard interactivo para el análisis de mercado y estrategia de expansión")

# Carga de datos
data = load_data()

if data is None:
    st.error("No se pudieron cargar los datos necesarios. Verifica los archivos CSV.")
    st.stop()

# ---------------------------
# SECCIÓN 1: MERCADO HOTELERO
# ---------------------------
st.header("📊 Mercado Hotelero en Miami", divider="green")
col1, col2 = st.columns(2)

with col1:
    try:
        fig1 = px.line(
            data['mercado_hotelero'],
            x="Año",
            y="Habitaciones",
            title="Inventario de Habitaciones (2023-2025)",
            markers=True,
            color_discrete_sequence=["#2ecc71"]
        )
        st.plotly_chart(fig1, use_container_width=True)
    except Exception as e:
        st.error(f"Error en gráfico de inventario: {str(e)}")

with col2:
    try:
        fig2 = px.pie(
            data['submercados'],
            names="Zona",
            values="Porcentaje (%)",
            title="Distribución por Zona (2025)",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error en gráfico de distribución: {str(e)}")

# ---------------------------
# SECCIÓN 2: DEMANDA TURÍSTICA
# ---------------------------
st.header("👥 Demanda Turística", divider="green")
tab1, tab2 = st.tabs(["Visitantes", "Financiamiento"])

with tab1:
    try:
        fig3 = px.bar(
            data['visitantes'],
            x="Tipo",
            y="Millones",
            color="Tipo",
            title="Turistas en Miami (2023)",
            labels={"Millones": "Visitantes (millones)"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f"Error en gráfico de visitantes: {str(e)}")

with tab2:
    try:
        st.dataframe(
            data['financiamiento'],
            column_config={
                "Fuente": st.column_config.TextColumn("Fuente", width="medium"),
                "Tasa (%)": st.column_config.ProgressColumn(
                    "Tasa de Interés",
                    format="%.2f%%",
                    min_value=0,
                    max_value=10
                )
            },
            hide_index=True,
            use_container_width=True
        )
        st.caption("Fuentes de financiamiento disponibles para el proyecto")
    except Exception as e:
        st.error(f"Error mostrando financiamiento: {str(e)}")

# ---------------------------
# SECCIÓN 3: PERFIL DE CLIENTES
# ---------------------------
st.header("🎯 Segmentación de Clientes", divider="green")

try:
    clientes_data = data['clientes'].set_index('Categoría')
    st.dataframe(
        clientes_data,
        column_config={
            "Detalle": st.column_config.TextColumn("Características", width="large")
        },
        use_container_width=True
    )
    
    with st.expander("📊 Análisis Demográfico"):
        st.markdown("""
        - **Edad 25-55 años**: Público principal con capacidad económica
        - **Ingresos ≥ $50K**: Clientes con poder adquisitivo para turismo premium
        - **Intereses**: Enfoque en sostenibilidad y experiencias naturales
        """)
        
except Exception as e:
    st.error(f"Error mostrando segmentación: {str(e)}")

# ---------------------------
# SECCIÓN 4: UBICACIÓN (REDLAND)
# ---------------------------
st.header("📍 Ubicación Propuesta: Redland", divider="green")

try:
    ubicacion_data = data['ubicacion']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Ventajas Clave", divider="gray")
        ventajas = ubicacion_data[ubicacion_data['Variable'].str.contains('Ventaja')]
        for _, row in ventajas.iterrows():
            st.markdown(f"- {row['Valor']}")
        
        st.subheader("🌳 Características Ambientales")
        st.image("https://images.unsplash.com/photo-1519046904884-53103b34b206?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                caption="Área natural de Redland")
    
    with col2:
        st.subheader("⚠️ Consideraciones", divider="gray")
        desafios = ubicacion_data[ubicacion_data['Variable'].str.contains('Desafío|Requisito')]
        for _, row in desafios.iterrows():
            st.markdown(f"- **{row['Variable']}**: {row['Valor']}")
            
except Exception as e:
    st.error(f"Error mostrando ubicación: {str(e)}")

# ---------------------------
# SECCIÓN 5: ESTRATEGIA MARKETING
# ---------------------------
st.header("📈 Estrategias de Marketing", divider="green")

try:
    fig4 = px.bar(
        data['marketing_roi'],
        x="Red Social",
        y="ROI (%)",
        color="Ingresos Generados (USD)",
        title="Retorno de Inversión por Plataforma (2025)",
        barmode="group",
        color_continuous_scale="greens"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    with st.expander("🔍 Detalles de Campañas"):
        st.write("""
        **Estrategia multicanal:**
        - YouTube: Contenido visual de experiencias en el lodge
        - Instagram: Marketing de influencers y stories
        - LinkedIn: Enfoque en turismo corporativo sostenible
        """)
        
except Exception as e:
    st.error(f"Error en estrategia marketing: {str(e)}")

# ---------------------------
# SECCIÓN 6: DATOS COMPLETOS
# ---------------------------
st.header("📁 Base de Datos Completa", divider="green")

tab_names = [
    "Mercado Hotelero", 
    "Submercados", 
    "Visitantes", 
    "Financiamiento", 
    "Clientes", 
    "Ubicación",
    "Marketing ROI"
]

tabs = st.tabs(tab_names)

for i, (tab, df_name) in enumerate(zip(tabs, data.keys())):
    with tab:
        try:
            st.dataframe(
                data[df_name],
                hide_index=True,
                use_container_width=True,
                height=300
            )
            st.download_button(
                label="Descargar CSV",
                data=data[df_name].to_csv(index=False).encode('utf-8'),
                file_name=f"{df_name}.csv",
                mime="text/csv",
                key=f"download_{i}"
            )
        except Exception as e:
            st.error(f"Error mostrando {df_name}: {str(e)}")

# ---------------------------
# FOOTER
# ---------------------------
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.9em;">
    © 2025 Finca Luna Nueva Lodge | Datos actualizados a Mayo 2025<br>
    <span style="font-size: 0.8em;">Dashboard desarrollado por el equipo de Expansión Internacional</span>
</div>
""", unsafe_allow_html=True)
