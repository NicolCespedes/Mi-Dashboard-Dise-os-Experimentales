import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Dashboard Experimental", page_icon="📊", layout="wide")

# Título principal
st.title("Dashboard: Análisis Experimental con Diseño Completamente al Azar (DCA) - Dos Factores")
st.write("---")

# Información del estudiante
st.subheader("Información del Estudiante")
st.write("**Nombre del curso:** Diseños Experimentales I")
st.write("**Nombre del estudiante:** Ruth Sandra Anccori Cespedes")
st.write("**Código:** 215386")
st.write("**Nombre del docente:** Cesar Augusto Lluen Vallejos")
st.write("**Título del caso en específico:** [Aquí va el título del caso]")

st.write("---")

# Sidebar con botones
st.sidebar.title("Navegación")
opciones = [
    "Contexto del Caso",
    "Teoría del Modelo",
    "Datos del Experimento Bifactorial",
    "Tabla ANOVA con Interpretaciones",
    "Prueba de Comparaciones Múltiples",
    "Interpretaciones"
]

seccion = st.sidebar.radio("Selecciona una sección:", opciones)

# Mostrar contenido según la sección seleccionada
if seccion == "Contexto del Caso":
    st.header("Contexto del Caso")
    st.write("""
    Aquí puedes describir el problema experimental, los objetivos, factores, niveles, unidad experimental, unidad de submuestreo, etc.
    """)
    # Puedes agregar gráficos, tablas, etc.

elif seccion == "Teoría del Modelo":
    st.header("Teoría del Modelo")
    st.write("""
    El modelo estadístico para un Diseño Completamente al Azar (DCA) con dos factores es:
    """)
    st.latex(r'''
    Y_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \epsilon_{ijk}
    ''')
    st.write("""
    Donde:
    - $Y_{ijk}$: Observación del k-ésimo submuestreo en el i-ésimo nivel del factor A y j-ésimo nivel del factor B.
    - $\mu$: Media general.
    - $\alpha_i$: Efecto del i-ésimo nivel del factor A.
    - $\beta_j$: Efecto del j-ésimo nivel del factor B.
    - $(\alpha\beta)_{ij}$: Efecto de la interacción entre A y B.
    - $\epsilon_{ijk}$: Error aleatorio.
    """)

elif seccion == "Datos del Experimento Bifactorial":
    st.header("Datos del Experimento Bifactorial")
    st.write("Aquí puedes mostrar la tabla de datos o una visualización.")
    # Ejemplo de tabla
    data = pd.DataFrame({
        "Factor A": ["A1", "A1", "A2", "A2"],
        "Factor B": ["B1", "B2", "B1", "B2"],
        "Replica": [1, 1, 1, 1],
        "Valor": [10, 12, 11, 13]
    })
    st.dataframe(data)
    # Ejemplo de gráfico
    fig, ax = plt.subplots()
    sns.barplot(data=data, x="Factor A", y="Valor", hue="Factor B", ax=ax)
    ax.set_title("Gráfico de Barras de Valores por Factores")
    st.pyplot(fig)

elif seccion == "Tabla ANOVA con Interpretaciones":
    st.header("Tabla ANOVA con Interpretaciones")
    st.write("Aquí puedes incluir la tabla ANOVA generada.")
    anova_data = {
        "Fuente": ["Factor A", "Factor B", "Interacción", "Error", "Total"],
        "GL": [2, 2, 4, 20, 28],
        "SC": [50, 40, 30, 100, 220],
        "CM": [25, 20, 7.5, 5, ""],
        "F": [5.0, 4.0, 1.5, "", ""],
        "p-valor": [0.01, 0.03, 0.25, "", ""]
    }
    df_anova = pd.DataFrame(anova_data)
    st.table(df_anova)
    st.write("""
    - Factor A: p < 0.05 → Significativo.
    - Factor B: p < 0.05 → Significativo.
    - Interacción: p > 0.05 → No significativa.
    """)

elif seccion == "Prueba de Comparaciones Múltiples":
    st.header("Prueba de Comparaciones Múltiples")
    st.write("Aquí puedes mostrar los resultados de Tukey o Scheffé.")
    # Ejemplo de tabla de comparaciones
    tukey_data = {
        "Comparación": ["A1 vs A2", "A1 vs A3", "A2 vs A3"],
        "Diferencia": [1.2, 0.8, -0.4],
        "p-ajustado": [0.02, 0.15, 0.60]
    }
    df_tukey = pd.DataFrame(tukey_data)
    st.table(df_tukey)

elif seccion == "Interpretaciones":
    st.header("Interpretaciones")
    st.write("""
    - El factor A tiene un efecto significativo sobre la variable respuesta.
    - El factor B también es significativo.
    - No hay interacción significativa entre A y B.
    - Se recomienda el tratamiento A2 con B1 para maximizar la respuesta.
    """)