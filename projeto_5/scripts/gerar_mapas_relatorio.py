"""
Script para gerar mapas leves (PNG) para o relatório HTML interativo.
- Mapa do Brasil colorido por clusters K=3 (modelo melhorado)
- Mapa do Brasil colorido por clusters K=4 (V3) para comparação
- Mapa por regiões do Brasil
- Perfis dos clusters K=4 para comparação no relatório
"""

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE = r'c:\Users\guilhermecorrea\Downloads\Gui\Projetos\PortifolioProjetos\projeto_5'
SHP = os.path.join(BASE, 'data', 'raw', 'municipios_brasil', 'BR_Municipios_2022.shp')
CSV_MELHORADO = os.path.join(BASE, 'outputs', 'results', 'municipios_clusters_melhorado.csv')
OUT_FIG = os.path.join(BASE, 'outputs', 'figures')
OUT_RES = os.path.join(BASE, 'outputs', 'results')

print("Carregando dados...")
df = pd.read_csv(CSV_MELHORADO)
print(f"  Municípios com clusters K=3: {len(df)}")

# === 1. Gerar clusters K=4 com V3 ===
print("\nGerando clusters K=4 (V3)...")
features_v3 = [
    'log_populacao', 'log_densidade', 'pib_per_capita',
    'taxa_alfabetizacao', 'mortalidade_infantil', 'esgoto_adequado',
    'saude_per_10k', 'indice_desenvolvimento_social',
    'indice_infraestrutura', 'urbanizacao_proxy'
]

X = df[features_v3].values
km4 = KMeans(n_clusters=4, random_state=42, n_init=20)
df['cluster_k4'] = km4.fit_predict(X)

# Silhouette K=4
from sklearn.metrics import silhouette_score
sil_k4 = silhouette_score(X, df['cluster_k4'])
print(f"  Silhueta K=4: {sil_k4:.4f}")

# Perfis K=4
print("\nPerfis K=4:")
perfil_k4 = {}
for c in sorted(df['cluster_k4'].unique()):
    sub = df[df['cluster_k4'] == c]
    perfil_k4[int(c)] = {
        'n': len(sub),
        'pct': round(len(sub)/len(df)*100, 1),
        'pib_pc_medio': round(sub['pib_per_capita_original'].median(), 0),
        'ids_medio': round(sub['indice_desenvolvimento_social'].mean(), 3),
        'pop_mediana': round(sub['populacao_original'].median(), 0),
        'regioes': sub['regiao'].value_counts().head(3).to_dict()
    }
    print(f"  Cluster {c}: {perfil_k4[int(c)]['n']} munic. ({perfil_k4[int(c)]['pct']}%)")

# Salvar perfis K=4
with open(os.path.join(OUT_RES, 'perfis_k4_v3.json'), 'w', encoding='utf-8') as f:
    json.dump(perfil_k4, f, ensure_ascii=False, indent=2)

# Salvar CSV com ambos clusters
df.to_csv(os.path.join(OUT_RES, 'municipios_clusters_k3_k4.csv'), index=False)
print(f"\nCSV salvo com K=3 e K=4: {len(df)} municípios")

# === 2. Carregar shapefile ===
print("\nCarregando shapefile...")
gdf = gpd.read_file(SHP)
gdf = gdf.to_crs(epsg=4326)
print(f"  Geometrias no shapefile: {len(gdf)}")

# Merge - garantir código compatível
gdf['CD_MUN'] = gdf['CD_MUN'].astype(str).str[:7]
df['codigo_ibge'] = df['codigo_ibge'].astype(str).str[:7]

gdf_merged = gdf.merge(
    df[['codigo_ibge', 'cluster_melhorado', 'cluster_k4', 'regiao']],
    left_on='CD_MUN', right_on='codigo_ibge', how='left'
)
matched = gdf_merged['cluster_melhorado'].notna().sum()
missing = gdf_merged['cluster_melhorado'].isna().sum()
print(f"  Municípios pareados: {matched}")
print(f"  Sem dados (no shapefile mas não no dataset): {missing}")

# Simplificar geometria para PNGs leves
gdf_merged['geometry'] = gdf_merged['geometry'].simplify(tolerance=0.01, preserve_topology=True)

# === 3. Mapa K=3 ===
print("\nGerando mapa K=3...")
colors_k3 = ['#F28C28', '#1B7F5C', '#F7BA7E']
cmap_k3 = ListedColormap(colors_k3)

fig, ax = plt.subplots(1, 1, figsize=(12, 12), facecolor='#111827')
ax.set_facecolor('#111827')

# Municípios sem cluster (cinza)
no_cluster = gdf_merged[gdf_merged['cluster_melhorado'].isna()]
if len(no_cluster) > 0:
    no_cluster.plot(ax=ax, color='#374151', edgecolor='none', linewidth=0)

# Municípios com cluster
with_cluster = gdf_merged[gdf_merged['cluster_melhorado'].notna()].copy()
with_cluster['cluster_melhorado'] = with_cluster['cluster_melhorado'].astype(int)
with_cluster.plot(
    ax=ax, column='cluster_melhorado', cmap=cmap_k3,
    edgecolor='#1F2937', linewidth=0.1, legend=False
)

# Legenda
from matplotlib.patches import Patch
legend_k3 = [
    Patch(facecolor=colors_k3[0], label=f'Grupo 0 — 2.154 munic. (41,4%)'),
    Patch(facecolor=colors_k3[1], label=f'Grupo 1 — 545 munic. (10,5%)'),
    Patch(facecolor=colors_k3[2], label=f'Grupo 2 — 2.505 munic. (48,1%)'),
    Patch(facecolor='#374151', label=f'Sem dados — {missing} munic.'),
]
ax.legend(handles=legend_k3, loc='lower left', fontsize=10,
          facecolor='#1F2937', edgecolor='#374151', labelcolor='#E5E7EB',
          framealpha=0.95)

ax.set_title('Agrupamento dos Municípios — KMeans K=3 (V3)',
             color='#E5E7EB', fontsize=16, fontweight='bold', pad=15)
ax.set_axis_off()
ax.set_xlim(-74, -34)
ax.set_ylim(-34, 6)

fig.tight_layout()
path_k3 = os.path.join(OUT_FIG, 'mapa_clusters_k3.png')
fig.savefig(path_k3, dpi=150, bbox_inches='tight', facecolor='#111827')
plt.close(fig)
size_kb = os.path.getsize(path_k3) / 1024
print(f"  Salvo: {path_k3} ({size_kb:.0f} KB)")

# === 4. Mapa K=4 ===
print("\nGerando mapa K=4...")
colors_k4 = ['#F28C28', '#1B7F5C', '#F7BA7E', '#8DBFAE']
cmap_k4 = ListedColormap(colors_k4)

fig, ax = plt.subplots(1, 1, figsize=(12, 12), facecolor='#111827')
ax.set_facecolor('#111827')

if len(no_cluster) > 0:
    no_cluster.plot(ax=ax, color='#374151', edgecolor='none', linewidth=0)

with_cluster_k4 = gdf_merged[gdf_merged['cluster_k4'].notna()].copy()
with_cluster_k4['cluster_k4'] = with_cluster_k4['cluster_k4'].astype(int)
with_cluster_k4.plot(
    ax=ax, column='cluster_k4', cmap=cmap_k4,
    edgecolor='#1F2937', linewidth=0.1, legend=False
)

# Legenda K=4
legend_k4_items = []
for c in range(4):
    n = perfil_k4[c]['n']
    pct = perfil_k4[c]['pct']
    legend_k4_items.append(Patch(facecolor=colors_k4[c], label=f'Grupo {c} — {n:,} munic. ({pct}%)'.replace(',', '.')))
legend_k4_items.append(Patch(facecolor='#374151', label=f'Sem dados — {missing} munic.'))

ax.legend(handles=legend_k4_items, loc='lower left', fontsize=10,
          facecolor='#1F2937', edgecolor='#374151', labelcolor='#E5E7EB',
          framealpha=0.95)

ax.set_title('Agrupamento dos Municípios — KMeans K=4 (V3)',
             color='#E5E7EB', fontsize=16, fontweight='bold', pad=15)
ax.set_axis_off()
ax.set_xlim(-74, -34)
ax.set_ylim(-34, 6)

fig.tight_layout()
path_k4 = os.path.join(OUT_FIG, 'mapa_clusters_k4.png')
fig.savefig(path_k4, dpi=150, bbox_inches='tight', facecolor='#111827')
plt.close(fig)
size_kb = os.path.getsize(path_k4) / 1024
print(f"  Salvo: {path_k4} ({size_kb:.0f} KB)")

# === 5. Mapa por Regiões ===
print("\nGerando mapa por regiões...")
regiao_map = {
    'Norte': '#1B7F5C',
    'Nordeste': '#F28C28',
    'Sudeste': '#F7BA7E',
    'Sul': '#8DBFAE',
    'Centro-Oeste': '#E5E7EB'
}

# Usar SIGLA_UF do shapefile para mapear regiões
uf_to_regiao = {
    'AC':'Norte','AM':'Norte','AP':'Norte','PA':'Norte','RO':'Norte','RR':'Norte','TO':'Norte',
    'AL':'Nordeste','BA':'Nordeste','CE':'Nordeste','MA':'Nordeste','PB':'Nordeste',
    'PE':'Nordeste','PI':'Nordeste','RN':'Nordeste','SE':'Nordeste',
    'ES':'Sudeste','MG':'Sudeste','RJ':'Sudeste','SP':'Sudeste',
    'PR':'Sul','RS':'Sul','SC':'Sul',
    'DF':'Centro-Oeste','GO':'Centro-Oeste','MS':'Centro-Oeste','MT':'Centro-Oeste'
}
gdf_merged['regiao_geo'] = gdf_merged['SIGLA_UF'].map(uf_to_regiao)

fig, ax = plt.subplots(1, 1, figsize=(12, 12), facecolor='#111827')
ax.set_facecolor('#111827')

for regiao, cor in regiao_map.items():
    subset = gdf_merged[gdf_merged['regiao_geo'] == regiao]
    if len(subset) > 0:
        subset.plot(ax=ax, color=cor, edgecolor='#1F2937', linewidth=0.1)

legend_reg = [Patch(facecolor=c, label=r) for r, c in regiao_map.items()]
ax.legend(handles=legend_reg, loc='lower left', fontsize=11,
          facecolor='#1F2937', edgecolor='#374151', labelcolor='#E5E7EB',
          framealpha=0.95)

ax.set_title('Regiões do Brasil — 5.572 Municípios',
             color='#E5E7EB', fontsize=16, fontweight='bold', pad=15)
ax.set_axis_off()
ax.set_xlim(-74, -34)
ax.set_ylim(-34, 6)

fig.tight_layout()
path_reg = os.path.join(OUT_FIG, 'mapa_regioes_brasil.png')
fig.savefig(path_reg, dpi=150, bbox_inches='tight', facecolor='#111827')
plt.close(fig)
size_kb = os.path.getsize(path_reg) / 1024
print(f"  Salvo: {path_reg} ({size_kb:.0f} KB)")

# === 6. Métricas comparativas K=3 vs K=4 ===
print("\nMétricas comparativas:")
sil_k3 = silhouette_score(X, df['cluster_melhorado'])
from sklearn.metrics import davies_bouldin_score, calinski_harabasz_score

metrics = {
    'K=3': {
        'silhouette': round(sil_k3, 4),
        'davies_bouldin': round(davies_bouldin_score(X, df['cluster_melhorado']), 4),
        'calinski': round(calinski_harabasz_score(X, df['cluster_melhorado']), 1),
        'n_clusters': 3,
        'distribuicao': df['cluster_melhorado'].value_counts().sort_index().to_dict(),
        'max_cluster_pct': round(df['cluster_melhorado'].value_counts().max() / len(df) * 100, 1)
    },
    'K=4': {
        'silhouette': round(sil_k4, 4),
        'davies_bouldin': round(davies_bouldin_score(X, df['cluster_k4']), 4),
        'calinski': round(calinski_harabasz_score(X, df['cluster_k4']), 1),
        'n_clusters': 4,
        'distribuicao': df['cluster_k4'].value_counts().sort_index().to_dict(),
        'max_cluster_pct': round(df['cluster_k4'].value_counts().max() / len(df) * 100, 1)
    }
}

for k, v in metrics.items():
    print(f"  {k}: Sil={v['silhouette']}, DB={v['davies_bouldin']}, Cal={v['calinski']}, Max={v['max_cluster_pct']}%")
    for c, n in v['distribuicao'].items():
        print(f"    Cluster {c}: {n} ({n/len(df)*100:.1f}%)")

with open(os.path.join(OUT_RES, 'comparacao_k3_k4.json'), 'w', encoding='utf-8') as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)

# === 7. Perfis detalhados K=4 para o relatório ===
print("\nPerfis detalhados K=4:")
perfis_detalhados_k4 = {}
for c in range(4):
    sub = df[df['cluster_k4'] == c]
    perfis_detalhados_k4[c] = {
        'n': len(sub),
        'pct': round(len(sub)/len(df)*100, 1),
        'pib_pc_mediano': round(sub['pib_per_capita_original'].median(), 0),
        'pop_mediana': round(sub['populacao_original'].median(), 0),
        'ids_medio': round(sub['indice_desenvolvimento_social'].mean(), 3),
        'esgoto_medio': round(sub['esgoto_adequado_original'].mean(), 1),
        'mortalidade_media': round(sub['mortalidade_infantil_original'].mean(), 1),
        'alfabetizacao_media': round(sub['taxa_alfabetizacao_original'].mean(), 1),
        'top_regioes': sub['regiao'].value_counts().head(3).to_dict(),
        'top_ufs': sub['uf'].value_counts().head(5).to_dict()
    }
    p = perfis_detalhados_k4[c]
    print(f"  Grupo {c}: {p['n']} munic., PIB R${p['pib_pc_mediano']:,.0f}, IDS={p['ids_medio']:.3f}, Pop mediana={p['pop_mediana']:,.0f}")

with open(os.path.join(OUT_RES, 'perfis_detalhados_k4.json'), 'w', encoding='utf-8') as f:
    json.dump(perfis_detalhados_k4, f, ensure_ascii=False, indent=2, default=str)

print("\n=== Concluído! ===")
print(f"Mapas salvos em: {OUT_FIG}")
print(f"Dados salvos em: {OUT_RES}")
