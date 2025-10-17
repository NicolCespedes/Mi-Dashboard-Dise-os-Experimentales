"""
Análisis de Diseño Completamente al Azar (DCA) Bifactorial con Submuestreo
Caso: Criminalidad en Puno - Octubre 2025

Estudiante: Ruth Sandra Anccori Cespedes
Código: 215386
Curso: Diseños Experimentales I
Docente: César Augusto Lluen Vallejos
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
from scipy.stats import shapiro, levene, f_oneway

# Configuración de visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("ANÁLISIS DCA BIFACTORIAL CON SUBMUESTREO")
print("Criminalidad en Puno - Octubre 2025")
print("="*80)

# ============================================================================
# 1. GENERACIÓN DE DATOS EXPERIMENTALES
# ============================================================================

print("\n[1] GENERACIÓN DE DATOS DEL EXPERIMENTO\n")

# Definir factores
zonas = ['Centro Histórico', 'Zona Comercial', 'Zona Residencial', 'Periferia']
tipos_delito = ['Hurto', 'Robo', 'Asalto']
replicas = [1, 2, 3]

# Crear dataset con submuestreo no balanceado
datos = []

# Centro Histórico - Hurto
datos.extend([
    ['Centro Histórico', 'Hurto', 1, 1, 12], ['Centro Histórico', 'Hurto', 1, 2, 15], ['Centro Histórico', 'Hurto', 1, 3, 13],
    ['Centro Histórico', 'Hurto', 2, 1, 14], ['Centro Histórico', 'Hurto', 2, 2, 16], ['Centro Histórico', 'Hurto', 2, 3, 15],
    ['Centro Histórico', 'Hurto', 3, 1, 13], ['Centro Histórico', 'Hurto', 3, 2, 14]
])

# Centro Histórico - Robo
datos.extend([
    ['Centro Histórico', 'Robo', 1, 1, 8], ['Centro Histórico', 'Robo', 1, 2, 9], ['Centro Histórico', 'Robo', 1, 3, 10],
    ['Centro Histórico', 'Robo', 2, 1, 9], ['Centro Histórico', 'Robo', 2, 2, 11],
    ['Centro Histórico', 'Robo', 3, 1, 7], ['Centro Histórico', 'Robo', 3, 2, 8], ['Centro Histórico', 'Robo', 3, 3, 9]
])

# Centro Histórico - Asalto
datos.extend([
    ['Centro Histórico', 'Asalto', 1, 1, 5], ['Centro Histórico', 'Asalto', 1, 2, 6],
    ['Centro Histórico', 'Asalto', 2, 1, 6], ['Centro Histórico', 'Asalto', 2, 2, 7], ['Centro Histórico', 'Asalto', 2, 3, 5],
    ['Centro Histórico', 'Asalto', 3, 1, 4], ['Centro Histórico', 'Asalto', 3, 2, 5], ['Centro Histórico', 'Asalto', 3, 3, 6]
])

# Zona Comercial - Hurto
datos.extend([
    ['Zona Comercial', 'Hurto', 1, 1, 18], ['Zona Comercial', 'Hurto', 1, 2, 20], ['Zona Comercial', 'Hurto', 1, 3, 19],
    ['Zona Comercial', 'Hurto', 2, 1, 17], ['Zona Comercial', 'Hurto', 2, 2, 19],
    ['Zona Comercial', 'Hurto', 3, 1, 19], ['Zona Comercial', 'Hurto', 3, 2, 21], ['Zona Comercial', 'Hurto', 3, 3, 20]
])

# Zona Comercial - Robo
datos.extend([
    ['Zona Comercial', 'Robo', 1, 1, 11], ['Zona Comercial', 'Robo', 1, 2, 12],
    ['Zona Comercial', 'Robo', 2, 1, 10], ['Zona Comercial', 'Robo', 2, 2, 11], ['Zona Comercial', 'Robo', 2, 3, 12],
    ['Zona Comercial', 'Robo', 3, 1, 12], ['Zona Comercial', 'Robo', 3, 2, 13]
])

# Zona Comercial - Asalto
datos.extend([
    ['Zona Comercial', 'Asalto', 1, 1, 7], ['Zona Comercial', 'Asalto', 1, 2, 8], ['Zona Comercial', 'Asalto', 1, 3, 9],
    ['Zona Comercial', 'Asalto', 2, 1, 8], ['Zona Comercial', 'Asalto', 2, 2, 9],
    ['Zona Comercial', 'Asalto', 3, 1, 6], ['Zona Comercial', 'Asalto', 3, 2, 7], ['Zona Comercial', 'Asalto', 3, 3, 8]
])

# Zona Residencial - Hurto
datos.extend([
    ['Zona Residencial', 'Hurto', 1, 1, 8], ['Zona Residencial', 'Hurto', 1, 2, 9],
    ['Zona Residencial', 'Hurto', 2, 1, 7], ['Zona Residencial', 'Hurto', 2, 2, 8], ['Zona Residencial', 'Hurto', 2, 3, 9],
    ['Zona Residencial', 'Hurto', 3, 1, 9], ['Zona Residencial', 'Hurto', 3, 2, 10], ['Zona Residencial', 'Hurto', 3, 3, 8]
])

# Zona Residencial - Robo
datos.extend([
    ['Zona Residencial', 'Robo', 1, 1, 4], ['Zona Residencial', 'Robo', 1, 2, 5], ['Zona Residencial', 'Robo', 1, 3, 6],
    ['Zona Residencial', 'Robo', 2, 1, 5], ['Zona Residencial', 'Robo', 2, 2, 6],
    ['Zona Residencial', 'Robo', 3, 1, 3], ['Zona Residencial', 'Robo', 3, 2, 4], ['Zona Residencial', 'Robo', 3, 3, 5]
])

# Zona Residencial - Asalto
datos.extend([
    ['Zona Residencial', 'Asalto', 1, 1, 2], ['Zona Residencial', 'Asalto', 1, 2, 3],
    ['Zona Residencial', 'Asalto', 2, 1, 3], ['Zona Residencial', 'Asalto', 2, 2, 4], ['Zona Residencial', 'Asalto', 2, 3, 3],
    ['Zona Residencial', 'Asalto', 3, 1, 2], ['Zona Residencial', 'Asalto', 3, 2, 3], ['Zona Residencial', 'Asalto', 3, 3, 4]
])

# Periferia - Hurto
datos.extend([
    ['Periferia', 'Hurto', 1, 1, 5], ['Periferia', 'Hurto', 1, 2, 6], ['Periferia', 'Hurto', 1, 3, 7],
    ['Periferia', 'Hurto', 2, 1, 6], ['Periferia', 'Hurto', 2, 2, 7],
    ['Periferia', 'Hurto', 3, 1, 4], ['Periferia', 'Hurto', 3, 2, 5], ['Periferia', 'Hurto', 3, 3, 6]
])

# Periferia - Robo
datos.extend([
    ['Periferia', 'Robo', 1, 1, 6], ['Periferia', 'Robo', 1, 2, 7],
    ['Periferia', 'Robo', 2, 1, 5], ['Periferia', 'Robo', 2, 2, 6], ['Periferia', 'Robo', 2, 3, 7],
    ['Periferia', 'Robo', 3, 1, 7], ['Periferia', 'Robo', 3, 2, 8], ['Periferia', 'Robo', 3, 3, 6]
])

# Periferia - Asalto
datos.extend([
    ['Periferia', 'Asalto', 1, 1, 8], ['Periferia', 'Asalto', 1, 2, 9], ['Periferia', 'Asalto', 1, 3, 10],
    ['Periferia', 'Asalto', 2, 1, 9], ['Periferia', 'Asalto', 2, 2, 10],
    ['Periferia', 'Asalto', 3, 1, 7], ['Periferia', 'Asalto', 3, 2, 8], ['Periferia', 'Asalto', 3, 3, 9]
])

# Crear DataFrame
df = pd.DataFrame(datos, columns=['Zona', 'TipoDelito', 'Replica', 'Submuestra', 'Incidentes'])

print("Estructura del dataset:")
print(df.head(10))
print(f"\nTotal de observaciones: {len(df)}")
print(f"Factores: Zona (4 niveles) × TipoDelito (3 niveles) = 12 tratamientos")
print(f"Réplicas balanceadas: 3 por tratamiento (36 unidades experimentales)")
print(f"Submuestreo no balanceado: 2-3 observaciones por réplica")

# ============================================================================
# 2. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================================

print("\n" + "="*80)
print("[2] ESTADÍSTICAS DESCRIPTIVAS")
print("="*80 + "\n")

# Calcular medias por tratamiento
medias_tratamiento = df.groupby(['Zona', 'TipoDelito'])['Incidentes'].agg(['mean', 'std', 'count'])
medias_tratamiento.columns = ['Media', 'Desv.Std', 'n']
print("Medias por tratamiento (Zona × TipoDelito):")
print(medias_tratamiento.round(2))

# Medias marginales
print("\n\nMedias marginales por Zona:")
print(df.groupby('Zona')['Incidentes'].mean().round(2))

print("\nMedias marginales por Tipo de Delito:")
print(df.groupby('TipoDelito')['Incidentes'].mean().round(2))

# ============================================================================
# 3. ANÁLISIS DE VARIANZA (ANOVA) BIFACTORIAL
# ============================================================================

print("\n" + "="*80)
print("[3] TABLA ANOVA BIFACTORIAL CON SUBMUESTREO")
print("="*80 + "\n")

# Crear variable de unidad experimental (combinación zona-delito-replica)
df['UE'] = df['Zona'] + '_' + df['TipoDelito'] + '_' + df['Replica'].astype(str)

# Modelo completo con interacción
modelo = ols('Incidentes ~ C(Zona) + C(TipoDelito) + C(Zona):C(TipoDelito) + C(UE)', data=df).fit()
tabla_anova = anova_lm(modelo, typ=2)

print("Tabla ANOVA:")
print(tabla_anova)

# Extraer valores F y p
f_zona = tabla_anova.loc['C(Zona)', 'F']
p_zona = tabla_anova.loc['C(Zona)', 'PR(>F)']
f_delito = tabla_anova.loc['C(TipoDelito)', 'F']
p_delito = tabla_anova.loc['C(TipoDelito)', 'PR(>F)']
f_interaccion = tabla_anova.loc['C(Zona):C(TipoDelito)', 'F']
p_interaccion = tabla_anova.loc['C(Zona):C(TipoDelito)', 'PR(>F)']

print("\n" + "-"*80)
print("INTERPRETACIÓN DE RESULTADOS ANOVA:")
print("-"*80)
print(f"\n1. Efecto Principal Factor A (Zona):")
print(f"   F({int(tabla_anova.loc['C(Zona)', 'df'])}, {int(tabla_anova.loc['Residual', 'df'])}) = {f_zona:.2f}, p = {p_zona:.4f}")
if p_zona < 0.05:
    print("   ✓ SIGNIFICATIVO: La zona urbana afecta significativamente la incidencia delictiva")
else:
    print("   ✗ NO SIGNIFICATIVO: No hay diferencias significativas entre zonas")

print(f"\n2. Efecto Principal Factor B (Tipo de Delito):")
print(f"   F({int(tabla_anova.loc['C(TipoDelito)', 'df'])}, {int(tabla_anova.loc['Residual', 'df'])}) = {f_delito:.2f}, p = {p_delito:.4f}")
if p_delito < 0.05:
    print("   ✓ SIGNIFICATIVO: El tipo de delito afecta significativamente la incidencia")
else:
    print("   ✗ NO SIGNIFICATIVO: No hay diferencias significativas entre tipos de delito")

print(f"\n3. Interacción Zona × Tipo de Delito:")
print(f"   F({int(tabla_anova.loc['C(Zona):C(TipoDelito)', 'df'])}, {int(tabla_anova.loc['Residual', 'df'])}) = {f_interaccion:.2f}, p = {p_interaccion:.4f}")
if p_interaccion < 0.05:
    print("   ✓ SIGNIFICATIVO: Existe interacción entre zona y tipo de delito")
    print("   Interpretación: El efecto del tipo de delito depende de la zona urbana")
else:
    print("   ✗ NO SIGNIFICATIVO: No hay interacción entre factores")

# ============================================================================
# 4. VERIFICACIÓN DE SUPUESTOS
# ============================================================================

print("\n" + "="*80)
print("[4] VERIFICACIÓN DE SUPUESTOS DEL MODELO")
print("="*80 + "\n")

# Test de Normalidad (Shapiro-Wilk)
residuos = modelo.resid
stat_shapiro, p_shapiro = shapiro(residuos)
print(f"1. Test de Normalidad (Shapiro-Wilk):")
print(f"   Estadístico W = {stat_shapiro:.4f}, p-valor = {p_shapiro:.4f}")
if p_shapiro > 0.05:
    print("   ✓ Los residuos siguen una distribución normal (p > 0.05)")
else:
    print("   ⚠ Evidencia de desviación de la normalidad (p < 0.05)")

# Test de Homocedasticidad (Levene)
grupos = [df[df['Zona'] == zona]['Incidentes'].values for zona in zonas]
stat_levene, p_levene = levene(*grupos)
print(f"\n2. Test de Homocedasticidad (Levene):")
print(f"   Estadístico F = {stat_levene:.4f}, p-valor = {p_levene:.4f}")
if p_levene > 0.05:
    print("   ✓ Las varianzas son homogéneas entre grupos (p > 0.05)")
else:
    print("   ⚠ Evidencia de heterocedasticidad (p < 0.05)")

print(f"\n3. Independencia:")
print("   ✓ Asumida por diseño del experimento (observaciones independientes)")

# ============================================================================
# 5. PRUEBAS DE COMPARACIONES MÚLTIPLES (BONFERRONI)
# ============================================================================

print("\n" + "="*80)
print("[5] PRUEBAS DE COMPARACIONES MÚLTIPLES - BONFERRONI")
print("="*80 + "\n")

# Función para comparaciones con Bonferroni manual
def bonferroni_comparisons(df, factor, alpha=0.05):
    grupos = df[factor].unique()
    n_comparaciones = len(grupos) * (len(grupos) - 1) // 2
    alpha_ajustado = alpha / n_comparaciones
    
    print(f"\nComparaciones para {factor}:")
    print(f"Nivel de significancia ajustado (Bonferroni): α' = {alpha:.3f} / {n_comparaciones} = {alpha_ajustado:.4f}\n")
    print(f"{'Comparación':<40} {'Dif.Medias':<12} {'p-valor':<12} {'Sig.'}")
    print("-" * 75)
    
    resultados = []
    for i in range(len(grupos)):
        for j in range(i+1, len(grupos)):
            grupo1 = df[df[factor] == grupos[i]]['Incidentes']
            grupo2 = df[df[factor] == grupos[j]]['Incidentes']
            
            # t-test
            t_stat, p_val = stats.ttest_ind(grupo1, grupo2)
            dif_medias = grupo1.mean() - grupo2.mean()
            
            significativo = "***" if p_val < alpha_ajustado else "NS"
            
            print(f"{grupos[i]:20} - {grupos[j]:20} {dif_medias:>10.2f}  {p_val:>10.4f}  {significativo:>5}")
            resultados.append({
                'Comp': f"{grupos[i]} - {grupos[j]}",
                'Dif': dif_medias,
                'p': p_val,
                'Sig': p_val < alpha_ajustado
            })
    
    return pd.DataFrame(resultados)

# Comparaciones para Factor A (Zona)
print("\n" + "-"*80)
print("FACTOR A: ZONA URBANA")
print("-"*80)
comp_zona = bonferroni_comparisons(df, 'Zona')

# Comparaciones para Factor B (Tipo de Delito)
print("\n" + "-"*80)
print("FACTOR B: TIPO DE DELITO")
print("-"*80)
comp_delito = bonferroni_comparisons(df, 'TipoDelito')

print("\n*** p < α' (significativo); NS = No significativo")

# ============================================================================
# 6. VISUALIZACIONES
# ============================================================================

print("\n" + "="*80)
print("[6] GENERANDO VISUALIZACIONES")
print("="*80 + "\n")

# Gráfico 1: Medias por tratamiento
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análisis de Criminalidad en Puno - Octubre 2025', fontsize=16, fontweight='bold')

# Boxplot por Zona
df.boxplot(column='Incidentes', by='Zona', ax=axes[0,0])
axes[0,0].set_title('Incidentes por Zona Urbana')
axes[0,0].set_xlabel('Zona')
axes[0,0].set_ylabel('Número de Incidentes')
plt.sca(axes[0,0])
plt.xticks(rotation=45, ha='right')

# Boxplot por Tipo de Delito
df.boxplot(column='Incidentes', by='TipoDelito', ax=axes[0,1])
axes[0,1].set_title('Incidentes por Tipo de Delito')
axes[0,1].set_xlabel('Tipo de Delito')
axes[0,1].set_ylabel('Número de Incidentes')

# Gráfico de interacción
medias_interaccion = df.groupby(['Zona', 'TipoDelito'])['Incidentes'].mean().unstack()
medias_interaccion.plot(ax=axes[1,0], marker='o', linewidth=2)
axes[1,0].set_title('Gráfico de Interacción Zona × Tipo de Delito')
axes[1,0].set_xlabel('Zona')
axes[1,0].set_ylabel('Media de Incidentes')
axes[1,0].legend(title='Tipo de Delito', bbox_to_anchor=(1.05, 1))
axes[1,0].grid(True, alpha=0.3)
plt.sca(axes[1,0])
plt.xticks(rotation=45, ha='right')

# Heatmap de medias
pivot_medias = df.groupby(['Zona', 'TipoDelito'])['Incidentes'].mean().unstack()
sns.heatmap(pivot_medias, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1,1], cbar_kws={'label': 'Incidentes'})
axes[1,1].set_title('Mapa de Calor: Medias por Tratamiento')
axes[1,1].set_xlabel('Tipo de Delito')
axes[1,1].set_ylabel('Zona')

plt.tight_layout()
plt.savefig('analisis_criminalidad_puno.png', dpi=300, bbox_inches='tight')
print("✓ Visualizaciones guardadas en 'analisis_criminalidad_puno.png'")

# ============================================================================
# 7. RESUMEN EJECUTIVO
# ============================================================================

print("\n" + "="*80)
print("[7] RESUMEN EJECUTIVO")
print("="*80 + "\n")

print("HALLAZGOS PRINCIPALES:")
print("-" * 80)
print(f"\n1. Zona con mayor incidencia delictiva:")
zona_max = df.groupby('Zona')['Incidentes'].mean().idxmax()
media_max = df.groupby('Zona')['Incidentes'].mean().max()
print(f"   {zona_max}: {media_max:.2f} incidentes promedio")

print(f"\n2. Tipo de delito más frecuente:")
delito_max = df.groupby('TipoDelito')['Incidentes'].mean().idxmax()
media_delito_max = df.groupby('TipoDelito')['Incidentes'].mean().max()
print(f"   {delito_max}: {media_delito_max:.2f} incidentes promedio")

print(f"\n3. Combinación zona-delito más crítica:")
comb_max = medias_tratamiento['Media'].idxmax()
val_max = medias_tratamiento['Media'].max()
print(f"   {comb_max[0]} + {comb_max[1]}: {val_max:.2f} incidentes")

print(f"\n4. Combinación zona-delito más segura:")
comb_min = medias_tratamiento['Media'].idxmin()
val_min = medias_tratamiento['Media'].min()
print(f"   {comb_min[0]} + {comb_min[1]}: {val_min:.2f} incidentes")

print("\n" + "="*80)
print("ANÁLISIS COMPLETADO EXITOSAMENTE")
print("="*80)
print(f"\nArchivos generados:")
print(f"  - analisis_criminalidad_puno.png (visualizaciones)")
print(f"\nPara más detalles, revisar el sistema interactivo React.")
print("="*80)