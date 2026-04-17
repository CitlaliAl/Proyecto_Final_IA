import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="App Estadística con IA", layout="wide")

# Decoración con CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { border-radius: 20px; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Monitor Estadístico Pro")

if "data" not in st.session_state:
    st.session_state.data = None

menu = st.sidebar.selectbox("Navegación", ["Carga de Datos", "Visualización", "Prueba Z", "Asistente IA"])

if menu == "Carga de Datos":
    st.header("📂 Carga de Archivos")
    opcion = st.radio("Origen de datos:", ["Subir CSV", "Generar Sintéticos"])
    
    if opcion == "Subir CSV":
        archivo = st.file_uploader("Carga tu archivo CSV")
        if archivo:
            st.session_state.data = pd.read_csv(archivo)
            st.success("¡Datos cargados con éxito!")
            st.write(st.session_state.data.head())
    else:
        if st.button("Generar 100 datos (Normal)"):
            datos = np.random.normal(50, 10, 100)
            st.session_state.data = pd.DataFrame(datos, columns=["Valores"])
            st.success("Datos generados correctamente")
            st.write(st.session_state.data.head())
    
elif menu == "Visualización":
    st.header("📈 Análisis Visual de Datos")
    if st.session_state.data is not None:
        df = st.session_state.data
        # Solo mostrar columnas numéricas
        cols_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        col = st.selectbox("Selecciona la variable a analizar", cols_numericas)
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax, color="skyblue")
            st.pyplot(fig)
        with col2:
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[col], ax=ax2, color="lightgreen")
            st.pyplot(fig2)
        
        st.subheader("📝 Interpretación del Estudiante")
        st.info("Responde estas preguntas para tu reporte:")
        st.radio("1. ¿La distribución parece normal?", ["Sí", "No", "Tiene sesgo"])
        st.text_area("2. ¿Detectas outliers o valores extraños?")
    else:
        st.warning("⚠️ Primero carga datos en el menú lateral.")