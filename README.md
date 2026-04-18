# 🐾 Snoopy Estadístico Pro: Dashboard de Análisis de Datos e IA
## Proyecto Final - Ingeniería en Sistemas / Ciencias de Datos

Este repositorio contiene una herramienta avanzada de análisis estadístico desarrollada íntegramente en Python. El objetivo de la aplicación es proporcionar un entorno intuitivo y profesional para la interpretación de conjuntos de datos mediante estadística descriptiva, inferencial y visualizaciones de alta calidad.

---

## 👨‍💻 Detalles del Desarrollador
* **Autor:** Citlali Montserrat Alvarado Pérez
* **Institución:** Facultad de Ingeniería
* **Materia:** Inteligencia Artificial / Fundamentos de Programación
* **Fecha:** Abril 2026

---

## 🛠️ Especificaciones Técnicas (Stack Tecnológico)
El proyecto ha sido construido utilizando las librerías más robustas del ecosistema de Ciencia de Datos en Python:
* **Streamlit:** Framework principal para la creación de la interfaz de usuario (UI) moderna y reactiva.
* **Pandas & NumPy:** Motores de procesamiento de datos para la manipulación de matrices y DataFrames.
* **Seaborn & Matplotlib:** Bibliotecas de visualización para la generación de gráficos estadísticos de grado científico.
* **Git:** Sistema de control de versiones utilizado para el seguimiento del ciclo de vida del software.

---

## 📊 Módulos Funcionales

### 1. Análisis Descriptivo
Cálculo en tiempo real de los estadísticos fundamentales:
- **Tendencia Central:** Media y Mediana.
- **Dispersión:** Varianza, Desviación Estándar y Rango.
- **Limpieza de Datos:** Manejo de valores nulos y detección de tipos de datos.

### 2. Visualización de Datos
Generación dinámica de gráficos basados en la selección de variables:
- **Histogramas:** Con estimación de densidad de kernel (KDE) para analizar distribuciones.
- **Boxplots (Diagramas de Caja):** Para la detección visual de valores atípicos (outliers) y cuartiles.

### 3. Inferencia Estadística (Módulo de IA)
Implementación de pruebas de hipótesis para la toma de decisiones basada en datos:
- **Prueba Z:** Comparación de medias para muestras grandes.
- **Interpretación:** Cálculo automático de P-Value y niveles de significancia para validar o rechazar hipótesis nulas.

### 4. Interfaz Personalizada
- **Temática:** Estética inspirada en "Snoopy" con un enfoque limpio y académico.
- **Sidebar:** Menú de navegación lateral para una experiencia de usuario fluida.
- **API integration:** Estructura preparada para la serialización de resultados en formato JSON.

---

## 📂 Estructura del Proyecto
```text
├── app.py              # Código fuente principal (Lógica y UI)
├── README.md           # Documentación técnica del proyecto
└── .gitignore          # Exclusión de archivos temporales de Python