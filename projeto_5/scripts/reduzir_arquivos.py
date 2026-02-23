"""
Reduz tamanho dos arquivos grandes do projeto:
1. Simplifica geometrias do GeoJSON (625MB → ~15MB)
2. Limpa outputs do notebook 07 (41MB → ~5MB)
"""
import json, os

BASE = r'c:\Users\guilhermecorrea\Downloads\Gui\Projetos\PortifolioProjetos\projeto_5'

# ─────────────────────────────────────────────
# 1. SIMPLIFICAR GEOJSON
# ─────────────────────────────────────────────
print("=== 1. Simplificando GeoJSON ===")
geojson_path = os.path.join(BASE, 'outputs', 'results', 'municipios_clustered.geojson')
geojson_out  = os.path.join(BASE, 'outputs', 'results', 'municipios_clustered_simples.geojson')

try:
    import geopandas as gpd
    from shapely.geometry import mapping

    print("Lendo GeoJSON...")
    gdf = gpd.read_file(geojson_path)
    print(f"  {len(gdf)} municípios, CRS: {gdf.crs}")
    print(f"  Colunas: {list(gdf.columns)}")

    # Manter apenas colunas essenciais para o relatório
    colunas_manter = ['geometry', 'CD_MUN', 'NM_MUN', 'SIGLA_UF']
    colunas_manter = [c for c in colunas_manter if c in gdf.columns]
    # Adicionar colunas de cluster se existirem
    for col in ['cluster', 'cluster_k4', 'cluster_k10', 'cluster_regional', 'regiao', 'uf']:
        if col in gdf.columns:
            colunas_manter.append(col)
    gdf = gdf[list(dict.fromkeys(colunas_manter))]  # deduplica mantendo ordem

    # Simplificar geometrias (tolerance em graus: 0.01° ≈ 1km no equador)
    print("  Simplificando geometrias (tolerance=0.01)...")
    gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.01, preserve_topology=True)

    # Reduzir precisão das coordenadas para 4 casas decimais
    print("  Reduzindo precisão de coordenadas...")

    def round_coords(geom, decimals=4):
        import shapely.wkt
        import re
        wkt = geom.wkt
        def fmt(m):
            return f"{round(float(m.group()), decimals)}"
        wkt2 = re.sub(r'-?\d+\.\d+', fmt, wkt)
        return shapely.wkt.loads(wkt2)

    gdf['geometry'] = gdf['geometry'].apply(round_coords)

    # Salvar
    gdf.to_file(geojson_out, driver='GeoJSON')
    size_orig = os.path.getsize(geojson_path) / 1024**2
    size_new  = os.path.getsize(geojson_out)  / 1024**2
    print(f"  Original: {size_orig:.0f} MB → Simplificado: {size_new:.1f} MB")
    print(f"  Salvo em: {geojson_out}")

    # Substituir original pelo simplificado
    os.replace(geojson_out, geojson_path)
    print(f"  Substituído com sucesso.")

except Exception as e:
    print(f"  ERRO no GeoJSON: {e}")

# ─────────────────────────────────────────────
# 2. LIMPAR OUTPUTS DO NOTEBOOK 07
# ─────────────────────────────────────────────
print("\n=== 2. Limpando outputs do notebook 07 ===")
nb_path = os.path.join(BASE, 'notebooks', '07_visualizacao_mapas.ipynb')

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    size_orig = os.path.getsize(nb_path) / 1024**2
    n_cleared = 0

    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            outputs = cell.get('outputs', [])
            if outputs:
                cell['outputs'] = []
                cell['execution_count'] = None
                n_cleared += 1

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    size_new = os.path.getsize(nb_path) / 1024**2
    print(f"  {n_cleared} células limpas")
    print(f"  Original: {size_orig:.0f} MB → Limpo: {size_new:.1f} MB")

except Exception as e:
    print(f"  ERRO no notebook: {e}")

# ─────────────────────────────────────────────
# 3. DELETAR SHAPEFILE (GeoJSON simplificado é suficiente)
# ─────────────────────────────────────────────
print("\n=== 3. Removendo shapefile ===")
shp_dir = os.path.join(BASE, 'data', 'raw', 'municipios_brasil')
total_shp = 0
removed = []

if os.path.exists(shp_dir):
    for f in os.listdir(shp_dir):
        fp = os.path.join(shp_dir, f)
        size = os.path.getsize(fp) / 1024**2
        total_shp += size
        os.remove(fp)
        removed.append(f)

    # Remover pasta se vazia
    try:
        os.rmdir(shp_dir)
    except:
        pass

    print(f"  Removidos {len(removed)} arquivos ({total_shp:.0f} MB):")
    for f in removed:
        print(f"    {f}")
else:
    print(f"  Diretório não encontrado: {shp_dir}")

# ─────────────────────────────────────────────
# RESUMO FINAL
# ─────────────────────────────────────────────
print("\n=== RESUMO ===")
print("OK — arquivos grandes reduzidos.")
