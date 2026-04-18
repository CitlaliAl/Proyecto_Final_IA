import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from scipy import stats
from scipy.stats import norm
import json
import time
import datetime

# ==============================================================================
# SECCIÓN 1: MOTOR DE IDENTIDAD Y ESTILOS (UI/UX ENGINE)
# ==============================================================================
# Configuración de página con mayor control de layout
st.set_page_config(
    page_title="Snoopy Estadístico Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS avanzado para animaciones y tipografía
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Pacifico&family=Quicksand:wght@400;700&display=swap');
    
    /* Variables de Color y Transiciones */
    :root {
        --primary-blue: #1976d2;
        --secondary-pink: #f06292;
        --soft-blue: #e3f2fd;
    }

    html, body, [class*="css"] { 
        font-family: 'Quicksand', sans-serif; 
        background-color: #f8fbff;
    }

    /* Animación de entrada suave para todos los componentes */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stTabs, .diag-card, .stPlotlyChart, .description-box { 
        animation: fadeInUp 0.8s ease-out; 
    }

    /* Título Snoopy Estadístico */
    .lettering-title {
        font-family: 'Pacifico', cursive;
        color: var(--primary-blue); font-size: 4.5rem; text-align: center;
        background: -webkit-linear-gradient(45deg, #0d47a1, #64b5f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Firma Citlali M. */
    .citlali-signature {
        font-family: 'Dancing Script', cursive;
        color: var(--secondary-pink); font-size: 2.3rem; text-align: center;
        margin-top: -20px; margin-bottom: 20px;
    }

    /* Contenedores de Descripción con Estilo */
    .description-box {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px; border-radius: 15px; border-left: 6px solid var(--primary-blue);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 10px; margin-bottom: 25px;
        color: #34495e; font-size: 1rem;
    }

    /* Estilización de Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--soft-blue) 0%, #ffffff 100%) !important;
        border-right: 2px solid #bbdefb;
    }

    /* Botones Pro */
    .stButton>button {
        background: linear-gradient(45deg, var(--primary-blue), var(--secondary-pink));
        color: white; border: none; border-radius: 30px;
        padding: 12px 35px; font-weight: 700; transition: 0.4s;
        box-shadow: 0 4px 15px rgba(240, 98, 146, 0.3);
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(240, 98, 146, 0.5); }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN 2: CORE LÓGICO Y CÁLCULOS (ENGINEERING BACKEND)
# ==============================================================================

def secure_json_serializer(obj):
    """Maneja la conversión de tipos NumPy/Pandas a JSON estándar (Solución al error anterior)."""
    if isinstance(obj, (np.int64, np.int32, np.int16)): return int(obj)
    if isinstance(obj, (np.float64, np.float32)): return float(obj)
    if isinstance(obj, (datetime.datetime, datetime.date)): return obj.isoformat()
    return str(obj)

def run_z_test_logic(mean_sample, mean_null, std_dev, sample_size, alpha_level, tails):
    """Ejecuta el algoritmo de inferencia estadística para pruebas Z."""
    standard_error = std_dev / np.sqrt(sample_size)
    z_calc = (mean_sample - mean_null) / standard_error
    
    if tails == "Bilateral (≠)":
        p_val = 2 * (1 - norm.cdf(abs(z_calc)))
    elif tails == "Cola Derecha (>)":
        p_val = 1 - norm.cdf(z_calc)
    else:
        p_val = norm.cdf(z_calc)
        
    outcome = "Rechazar Hipótesis Nula (H0)" if p_val < alpha_level else "No Rechazar Hipótesis Nula (H0)"
    return z_calc, p_val, outcome

# ==============================================================================
# SECCIÓN 3: ESTRUCTURA DE LA INTERFAZ (UI COMPONENTS)
# ==============================================================================

# Branding Superior
left_sp, center_logo, right_sp = st.columns([1, 0.2, 1])
with center_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/5/53/Snoopy_Peanuts.png", width=90)

st.markdown('<p class="lettering-title">Snoopy Estadístico</p>', unsafe_allow_html=True)
st.markdown('<p class="citlali-signature">Design & Stats by Citlali M.</p>', unsafe_allow_html=True)

# Sidebar de Gestión de Datos
with st.sidebar:
    st.markdown("### 🛠️ Configuración de Datos")
    input_method = st.radio("Método de Entrada:", ["Subir Archivo CSV", "Generar Datos de Control"])
    st.divider()
    st.write("**Estado del Sistema:** Activo ✅")
    st.info("Citlali M. - v4.0.0 (Engineering Edition)")

df = None
if input_method == "Subir Archivo CSV":
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo (ej. Redes sociales.csv)", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
else:
    if st.sidebar.button("✨ Generar Dataset de Prueba"):
        df = pd.DataFrame({'Variable_Analitica': np.random.normal(50, 10, 100)})

# ==============================================================================
# SECCIÓN 4: DASHBOARD ANALÍTICO (MAIN WORKSPACE)
# ==============================================================================

if df is not None:
    # Identificación automática de columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.error("⚠️ El archivo cargado no contiene columnas numéricas compatibles.")
    else:
        # Selector de Variable
        target_var = st.selectbox("🎯 Variable a Procesar:", numeric_cols)
        working_data = df[target_var].dropna()

        # Organización en Tabs (Pestañas)
        tab_viz, tab_inf, tab_ia, tab_api = st.tabs(["🎨 Galería Gráfica", "🧪 Laboratorio Estadístico", "🤖 Snoopy-GPT", "🔌 API Dev"])

        # --- TAB 1: VISUALIZACIÓN ---
        with tab_viz:
            st.subheader("📊 Análisis Visual de la Distribución")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### Histograma")
                fig_h = px.histogram(df, x=target_var, nbins=20, color_discrete_sequence=['#1976d2'], template="plotly_white")
                st.plotly_chart(fig_h, use_container_width=True)
                st.markdown("""<div class="description-box"><b>Breve Explicación:</b> El histograma permite observar la forma en que se agrupan los datos. Nos ayuda a identificar si la distribución tiene una tendencia central o si hay huecos importantes en la información.</div>""", unsafe_allow_html=True)
            
            with c2:
                st.markdown("##### Boxplot (Caja y Bigotes)")
                fig_b = px.box(df, y=target_var, color_discrete_sequence=['#f06292'], points="all")
                st.plotly_chart(fig_b, use_container_width=True)
                st.markdown("""<div class="description-box"><b>Breve Explicación:</b> Este gráfico muestra la mediana y los cuartiles. Es la mejor herramienta para detectar 'outliers' o valores atípicos que se alejan demasiado del comportamiento normal.</div>""", unsafe_allow_html=True)
            
            # RECUPERACIÓN DE GRÁFICA KDE
            st.divider()
            st.markdown("##### 📈 Gráfica de Densidad (KDE)")
            fig_kde = ff.create_distplot([working_data], [target_var], show_hist=False, colors=['#64b5f6'])
            st.plotly_chart(fig_kde, use_container_width=True)
            st.markdown("""<div class="description-box"><b>Breve Explicación:</b> La estimación de densidad por kernel (KDE) es una curva suavizada que representa la probabilidad de que la variable tome un valor específico. Es fundamental para verificar la normalidad de la muestra.</div>""", unsafe_allow_html=True)

        # --- TAB 2: INFERENCIA ---
        with tab_inf:
            st.subheader("🧪 Pruebas de Hipótesis (Z-Test)")
            st.markdown('<div class="description-box">Aquí configuramos los parámetros matemáticos para decidir si los resultados son estadísticamente significativos o pura casualidad.</div>', unsafe_allow_html=True)
            
            inf_c1, inf_c2 = st.columns(2)
            with inf_c1:
                h0_val = st.number_input("Hipótesis Nula (μ0):", value=float(working_data.mean()))
                sigma_val = st.number_input("Desviación Estándar (σ) Conocida:", value=float(working_data.std()), min_value=0.01)
            with inf_c2:
                alpha_val = st.select_slider("Nivel de Error (α):", options=[0.01, 0.05, 0.1], value=0.05)
                direction = st.selectbox("Dirección de la Prueba:", ["Bilateral (≠)", "Cola Derecha (>)", "Cola Izquierda (<)"])
            
            if st.button("🚀 Ejecutar Algoritmo"):
                with st.spinner("Realizando cálculos de inferencia..."):
                    time.sleep(1)
                    z_res, p_res, final_decision = run_z_test_logic(working_data.mean(), h0_val, sigma_val, len(working_data), alpha_val, direction)
                    
                    # Guardamos en estado de sesión para las otras pestañas
                    st.session_state.update({'z_val': z_res, 'p_val': p_res, 'decision': final_decision, 'computed': True})
                    
                    st.divider()
                    st.success(f"Análisis Completado: {final_decision}")
                    r1, r2, r3 = st.columns(3)
                    r1.metric("Z Calculado", f"{z_res:.4f}")
                    r2.metric("P-Valor", f"{p_res:.4f}")
                    r3.metric("n (Muestra)", len(working_data))

        # --- TAB 3: IA ---
        with tab_ia:
            st.subheader("🤖 Snoopy-GPT: Interpretación Neural")
            if st.session_state.get('computed'):
                if st.button("🪄 Generar Conclusión Inteligente"):
                    st.balloons()
                    st.markdown(f"""
                    <div class="description-box">
                    <b>Reporte para Citlali M:</b><br><br>
                    Tras analizar la variable <b>{target_var}</b> con una muestra de {len(working_data)} casos, el sistema ha determinado que el veredicto es <b>{st.session_state['decision']}</b>. 
                    Esto indica que existe una {'fuerte evidencia estadística' if 'Rechazar' in st.session_state['decision'] else 'falta de evidencia suficiente'} para afirmar cambios en el proceso analizado.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Snoopy necesita que primero ejecutes la prueba en la pestaña del Laboratorio.")

        # --- TAB 4: API ---
        with tab_api:
            st.subheader("🔌 Dev API Endpoint (Módulo JSON)")
            st.markdown('<div class="description-box">Este apartado genera un objeto JSON listo para integrarse con sistemas externos, resolviendo errores de compatibilidad de datos.</div>', unsafe_allow_html=True)
            
            # Generamos el payload asegurando que no haya errores de serialización
            raw_payload = {
                "header": {
                    "developer": "Citlali M.",
                    "app": "Snoopy Estadístico",
                    "timestamp": datetime.datetime.now().isoformat()
                },
                "statistics": {
                    "mean": working_data.mean(),
                    "std_dev": working_data.std(),
                    "sample_size": len(working_data)
                },
                "test_results": {
                    "z_score": st.session_state.get('z_val', 0),
                    "p_value": st.session_state.get('p_val', 0),
                    "verdict": st.session_state.get('decision', "Pending")
                }
            }
            
            # Aplicamos limpieza de tipos
            clean_payload = {k: (secure_json_serializer(v) if not isinstance(v, dict) else {sk: secure_json_serializer(sv) for sk, sv in v.items()}) for k, v in raw_payload.items()}
            
            st.json(clean_payload)
            st.code(json.dumps(clean_payload, indent=4), language="json")

else:
    # Landing Page mejorada
    st.markdown("""
        <div style="text-align: center; padding: 80px; border: 3px dashed #bbdefb; border-radius: 40px; background: rgba(255,255,255,0.5);">
            <h2 style="color: #0d47a1;">✨ ¡Bienvenida al Studio de Ingeniería!</h2>
            <p style="font-size: 1.2rem;">Snoopy está esperando tus archivos CSV para comenzar la magia estadística.</p>
            <p>Utiliza el panel de la izquierda para cargar tu dataset.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer Profesional
st.markdown("<br><hr><center><b>© 2026 Snoopy Estadístico | Citlali M. | Ingeniería y Ciencia de Datos</b></center>", unsafe_allow_html=True)