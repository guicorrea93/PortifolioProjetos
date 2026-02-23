"""
Gera relatorio_interativo.html autocontido:
- Imagens PNG embutidas como base64
- Gráficos Plotly inline para as 3 linhas de pesquisa
"""
import base64, json, os

BASE = r'c:\Users\guilhermecorrea\Downloads\Gui\Projetos\PortifolioProjetos\projeto_5'
FIG  = os.path.join(BASE, 'outputs', 'figures')
OUT  = os.path.join(BASE, 'outputs', 'relatorio_interativo.html')

def b64(path):
    if not os.path.exists(path):
        return ''
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

# Imagens
img_k3       = b64(os.path.join(FIG, 'mapa_clusters_k3.png'))
img_k4       = b64(os.path.join(FIG, 'mapa_clusters_k4.png'))
img_dendro   = b64(os.path.join(FIG, 'dendrogramas_L1.png'))
img_heatmap  = b64(os.path.join(FIG, 'heatmap_centroides_melhorado.png'))
img_silh     = b64(os.path.join(FIG, '19_silhouette_plot.png'))
img_pca2d    = b64(os.path.join(FIG, '17_clusters_pca_2d_estatico.png'))
img_importan = b64(os.path.join(FIG, '36_feature_importance.png'))
img_mapas_reg= b64(os.path.join(FIG, '25_mapas_por_regiao_leve.png'))
img_cotovelo = b64(os.path.join(FIG, '10_metodo_cotovelo.png'))
img_metricas = b64(os.path.join(FIG, '13_todas_metricas.png'))

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clustering de Municípios Brasileiros — Relatório Interativo</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
:root{{
  --bg:#111827; --surface:#1F2937; --card:#1F2937; --text:#E5E7EB;
  --text-2:#CBD5E1; --muted:#94A3B8; --accent:#F28C28; --success:#1B7F5C;
  --accent-soft:#F7BA7E; --success-soft:#8DBFAE; --border:#374151;
  --c0:#F28C28; --c1:#1B7F5C; --c2:#F7BA7E; --c3:#8DBFAE; --sidebar-w:220px;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.7;}}
.sidebar{{position:fixed;top:0;left:0;width:var(--sidebar-w);height:100vh;background:var(--surface);border-right:1px solid var(--border);padding:24px 0;overflow-y:auto;z-index:100;display:flex;flex-direction:column;}}
.sidebar .logo{{font-weight:700;font-size:1.1rem;color:var(--accent);padding:0 20px 20px;border-bottom:1px solid var(--border);margin-bottom:12px;}}
.sidebar a{{display:block;color:var(--muted);text-decoration:none;font-size:.82rem;padding:9px 20px;transition:.2s;border-left:3px solid transparent;}}
.sidebar a:hover{{color:var(--text);background:rgba(242,140,40,.06);}}
.sidebar a.active{{color:var(--accent);border-left-color:var(--accent);background:rgba(242,140,40,.1);font-weight:600;}}
.sidebar .sep{{height:1px;background:var(--border);margin:8px 16px;}}
.main{{margin-left:var(--sidebar-w);}}
.container{{max-width:1100px;margin:0 auto;padding:0 32px;}}
.hero{{text-align:center;padding:70px 0 50px;}}
.hero h1{{font-size:2.6rem;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent-soft));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.hero p{{font-size:1.1rem;color:var(--muted);max-width:700px;margin:14px auto 0;}}
.badge{{display:inline-block;background:rgba(242,140,40,.12);color:var(--accent);padding:4px 14px;border-radius:20px;font-size:.8rem;margin-top:18px;}}
section{{padding:56px 0;border-top:1px solid var(--border);}}
section h2{{font-size:1.7rem;margin-bottom:8px;}}
section .subtitle{{color:var(--muted);margin-bottom:28px;font-size:.95rem;}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-bottom:28px;}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:22px;}}
.card .num{{font-size:2rem;font-weight:700;color:var(--accent);}}
.card .label{{color:var(--muted);font-size:.85rem;margin-top:4px;}}
.kpi-row{{display:flex;flex-wrap:wrap;gap:14px;margin:22px 0;}}
.kpi{{flex:1;min-width:140px;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center;}}
.kpi .val{{font-size:1.5rem;font-weight:700;}}
.kpi .lbl{{font-size:.76rem;color:var(--muted);margin-top:4px;}}
table{{width:100%;border-collapse:collapse;margin:18px 0;font-size:.86rem;}}
th,td{{padding:9px 13px;text-align:left;border-bottom:1px solid var(--border);}}
th{{color:var(--accent);font-weight:600;font-size:.76rem;text-transform:uppercase;letter-spacing:.5px;}}
tr:hover{{background:rgba(242,140,40,.04);}}
.chart-box{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;margin:22px 0;}}
.chart-box h3{{font-size:1rem;margin-bottom:10px;}}
.phase{{display:inline-block;background:var(--success);color:white;padding:3px 12px;border-radius:8px;font-size:.75rem;font-weight:600;margin-bottom:12px;}}
.timeline{{position:relative;padding-left:32px;}}
.timeline::before{{content:'';position:absolute;left:11px;top:0;bottom:0;width:2px;background:var(--border);}}
.timeline-item{{position:relative;margin-bottom:28px;}}
.timeline-item::before{{content:'';position:absolute;left:-27px;top:6px;width:14px;height:14px;border-radius:50%;background:var(--accent);border:3px solid var(--bg);}}
.timeline-item h3{{font-size:1.05rem;margin-bottom:5px;}}
.timeline-item p{{color:var(--muted);font-size:.88rem;}}
details{{background:var(--card);border:1px solid var(--border);border-radius:12px;margin:12px 0;}}
summary{{padding:14px 20px;cursor:pointer;font-weight:600;list-style:none;}}
summary::before{{content:'+ ';color:var(--accent);}}
details[open] summary::before{{content:'- ';}}
details .inner{{padding:0 20px 18px;}}
footer{{text-align:center;padding:36px 0;color:var(--muted);font-size:.82rem;border-top:1px solid var(--border);}}
.img-full{{width:100%;border-radius:12px;border:1px solid var(--border);display:block;}}
.map-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0;}}
.map-grid img{{width:100%;border-radius:12px;border:1px solid var(--border);}}
@media(max-width:900px){{.map-grid{{grid-template-columns:1fr;}}}}
.hl{{color:var(--accent);font-weight:600;}}
.hl2{{color:var(--success);font-weight:600;}}
.warn{{color:#ef4444;}}
.sidebar-toggle{{display:none;position:fixed;top:12px;left:12px;z-index:200;background:var(--surface);border:1px solid var(--border);color:var(--accent);padding:8px 12px;border-radius:8px;cursor:pointer;font-size:1.1rem;}}
@media(max-width:900px){{
  .sidebar{{transform:translateX(-100%);transition:transform .3s;}}
  .sidebar.open{{transform:translateX(0);}}
  .sidebar-toggle{{display:block;}}
  .main{{margin-left:0;}}
  .hero h1{{font-size:1.7rem;}}
}}
.linha-header{{display:flex;align-items:center;gap:14px;margin-bottom:20px;}}
.linha-badge{{padding:6px 18px;border-radius:30px;font-size:.9rem;font-weight:700;}}
.insight-box{{background:rgba(27,127,92,.08);border:1px solid rgba(27,127,92,.25);border-radius:12px;padding:20px;margin:18px 0;}}
.insight-box h4{{color:var(--success);margin-bottom:8px;}}
</style>
</head>
<body>
<button class="sidebar-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">&#9776;</button>

<nav class="sidebar">
  <div class="logo">ClusterBR</div>
  <a href="#intro">Introdução</a>
  <a href="#dados">Dados</a>
  <a href="#eda">Exploratória</a>
  <a href="#preproc">Pré-processamento</a>
  <a href="#feat">Variáveis</a>
  <a href="#busca">Busca Exaustiva</a>
  <a href="#modelo">Modelo Base (K=4)</a>
  <a href="#clusters">Perfil dos Grupos</a>
  <a href="#mapas">Mapas</a>
  <div class="sep"></div>
  <a href="#L1">Linha 1: Hierárquica</a>
  <a href="#L2">Linha 2: K=10</a>
  <a href="#L3">Linha 3: Regional</a>
  <a href="#comparacao3L">Comparação</a>
  <div class="sep"></div>
  <a href="#validacao">Validação</a>
  <a href="#conclusao">Conclusão</a>
</nav>

<div class="main">

<!-- HERO -->
<header class="hero">
  <div class="container">
    <span class="badge">Machine Learning &bull; Agrupamento Não Supervisionado</span>
    <h1>Agrupamento de Municípios Brasileiros</h1>
    <p>Segmentação de 5.204 municípios brasileiros com base em indicadores socioeconômicos do IBGE, utilizando técnicas avançadas de aprendizado não supervisionado e 3 linhas de pesquisa complementares.</p>
  </div>
</header>

<!-- 1. INTRODUÇÃO -->
<section id="intro">
<div class="container">
  <span class="phase">Fase 1</span>
  <h2>Introdução e Objetivo</h2>
  <p class="subtitle">Segmentar municípios em grupos homogêneos para subsidiar decisões estratégicas e táticas</p>
  <div class="cards">
    <div class="card"><div class="num">5.204</div><div class="label">Municípios analisados</div></div>
    <div class="card"><div class="num">10</div><div class="label">Indicadores (após engenharia)</div></div>
    <div class="card"><div class="num">3</div><div class="label">Linhas de pesquisa</div></div>
    <div class="card"><div class="num">0</div><div class="label">Municípios perdidos</div></div>
  </div>
  <p>O Brasil possui uma enorme diversidade socioeconômica entre seus municípios. Este estudo utiliza <strong>agrupamento não supervisionado</strong> para identificar grupos naturais de municípios com características semelhantes. Para lidar com a heterogeneidade dentro dos grupos, exploramos <strong>3 abordagens complementares</strong>:</p>
  <ul style="margin:16px 0 0 20px;color:var(--muted);">
    <li><strong>Linha 1:</strong> Subclusters hierárquicos dentro de cada grupo K=4</li>
    <li><strong>Linha 2:</strong> Aumento direto para K=10 grupos</li>
    <li><strong>Linha 3:</strong> Segmentação por região + PCA + K automático</li>
  </ul>
</div>
</section>

<!-- 2. DADOS -->
<section id="dados">
<div class="container">
  <span class="phase">Fase 2</span>
  <h2>Coleta e Descrição dos Dados</h2>
  <p class="subtitle">Fonte: IBGE — Instituto Brasileiro de Geografia e Estatística</p>
  <p>Os dados foram coletados do IBGE via web scraping e APIs públicas, abrangendo <span class="hl">todos os 5.204 municípios brasileiros</span>.</p>
  <table>
    <thead><tr><th>Indicador</th><th>O que representa</th></tr></thead>
    <tbody>
      <tr><td>População</td><td>Número total de habitantes do município</td></tr>
      <tr><td>Densidade Demográfica</td><td>Quantidade de habitantes por km²</td></tr>
      <tr><td>PIB per Capita</td><td>Riqueza produzida dividida pela população</td></tr>
      <tr><td>Taxa de Alfabetização</td><td>Percentual da população que sabe ler e escrever</td></tr>
      <tr><td>Mortalidade Infantil</td><td>Óbitos de crianças até 1 ano por 1.000 nascidos vivos</td></tr>
      <tr><td>Esgoto Adequado</td><td>Percentual de domicílios com rede de esgoto ou fossa séptica</td></tr>
      <tr><td>Unidades de Saúde</td><td>Estabelecimentos de saúde para cada 10 mil habitantes</td></tr>
    </tbody>
  </table>
  <div class="chart-box">
    <h3>Distribuição Regional dos Municípios</h3>
    <div id="chart-regioes"></div>
  </div>
</div>
</section>

<!-- 3. EXPLORATÓRIA -->
<section id="eda">
<div class="container">
  <span class="phase">Fase 3</span>
  <h2>Análise Exploratória</h2>
  <p class="subtitle">Entendendo a distribuição e a correlação entre os indicadores</p>
  <ul style="margin:16px 0 20px 20px;color:var(--muted);">
    <li><strong>Distribuições assimétricas:</strong> População e densidade transformadas em escala logarítmica</li>
    <li><strong>Disparidades regionais:</strong> Norte/Nordeste com menores índices de infraestrutura e alfabetização</li>
    <li><strong>Correlações fortes:</strong> Esgoto adequado vs taxa de alfabetização (r &gt; 0.7)</li>
  </ul>
  <div class="chart-box">
    <h3>Matriz de Correlação dos Indicadores Originais</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Valores entre -1 e +1. Quanto mais próximo de ±1, mais forte a relação.</p>
    <div id="chart-corr"></div>
  </div>
</div>
</section>

<!-- 4. PRÉ-PROCESSAMENTO -->
<section id="preproc">
<div class="container">
  <span class="phase">Fase 4</span>
  <h2>Pré-processamento</h2>
  <p class="subtitle">Normalização e preparação dos dados para agrupamento</p>
  <div class="timeline">
    <div class="timeline-item"><h3>1. Verificação de Dados Ausentes</h3><p>Cobertura completa para os 7 indicadores — sem dados faltantes.</p></div>
    <div class="timeline-item"><h3>2. Transformação Logarítmica</h3><p>População e densidade transformadas em escala log para reduzir assimetria.</p></div>
    <div class="timeline-item"><h3>3. Padronização (StandardScaler)</h3><p>Todos os indicadores padronizados (média=0, desvio=1).</p></div>
    <div class="timeline-item"><h3>4. Tratamento de Outliers</h3><p>298 municípios (5,7%) identificados via percentis P1/P99. Removidos para treinamento e <strong>reassociados</strong> ao cluster mais próximo após o fit — nenhum município perdido.</p></div>
  </div>
</div>
</section>

<!-- 5. ENGENHARIA DE VARIÁVEIS -->
<section id="feat">
<div class="container">
  <span class="phase">Fase 5</span>
  <h2>Engenharia de Variáveis</h2>
  <p class="subtitle">Criação de indicadores derivados para capturar melhor os padrões</p>
  <p>Foram criados <span class="hl">6 novos indicadores</span> a partir dos dados originais:</p>
  <table>
    <thead><tr><th>Indicador</th><th>Como é calculado</th><th>O que captura</th></tr></thead>
    <tbody>
      <tr><td class="hl2">Índice de Desenvolvimento Social (IDS)</td><td>Alfabetização + Esgoto - Mortalidade (normalizado)</td><td>Índice composto de qualidade de vida</td></tr>
      <tr><td>PIB por Saúde</td><td>PIB per capita / Unidades de saúde</td><td>Capacidade econômica vs oferta de saúde</td></tr>
      <tr><td class="hl2">Índice de Infraestrutura</td><td>Esgoto + Densidade (normalizado)</td><td>Nível de urbanização e infraestrutura</td></tr>
      <tr><td>Razão Educação/Mortalidade</td><td>Alfabetização / Mortalidade infantil</td><td>Relação educação-saúde</td></tr>
      <tr><td>PIB per Capita (log)</td><td>Logaritmo do PIB per capita</td><td>Suavização de valores extremos</td></tr>
      <tr><td>Proxy de Urbanização</td><td>População + Densidade (normalizado)</td><td>Grau de urbanização</td></tr>
    </tbody>
  </table>
  <p style="margin-top:20px;">Após análise de correlação (limiar &gt; 0.85), <span class="warn">3 foram removidos</span> por redundância. Resultado: <strong>10 indicadores finais (V3)</strong>.</p>
  <div class="chart-box">
    <h3>Importância dos Indicadores para o Agrupamento</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Quanto maior a barra, mais o indicador contribui para a separação dos grupos.</p>
    <div id="chart-importance"></div>
  </div>
</div>
</section>

<!-- 6. BUSCA EXAUSTIVA -->
<section id="busca">
<div class="container">
  <span class="phase">Fase 6</span>
  <h2>Seleção do Modelo</h2>
  <p class="subtitle">78 combinações testadas sistematicamente para encontrar o melhor agrupamento</p>
  <p>Foram avaliados 5 algoritmos (KMeans, BisectingKMeans, Agglomerative, GMM, Spectral) com diferentes valores de K e conjuntos de indicadores. A seleção utilizou um score composto que combina qualidade de separação e balanceamento dos grupos.</p>
  <div class="chart-box">
    <h3>Top 15 — Score Composto por Combinação</h3>
    <div id="chart-busca"></div>
  </div>
  <div class="chart-box">
    <h3>Método do Cotovelo — K ótimo</h3>
    <img src="{img_cotovelo}" class="img-full" alt="Método do Cotovelo" loading="lazy">
  </div>
  <div class="chart-box">
    <h3>Comparação de Métricas por K</h3>
    <img src="{img_metricas}" class="img-full" alt="Métricas" loading="lazy">
  </div>
</div>
</section>

<!-- 7. MODELO BASE K=4 -->
<section id="modelo">
<div class="container">
  <span class="phase">Fase 7</span>
  <h2>Modelo Base: KMeans K=4</h2>
  <p class="subtitle">Base para as 3 linhas de pesquisa — melhor equilíbrio entre granularidade e balanceamento</p>
  <div class="kpi-row">
    <div class="kpi"><div class="val" style="color:var(--accent);">KMeans</div><div class="lbl">Algoritmo</div></div>
    <div class="kpi"><div class="val" style="color:var(--success);">K = 4</div><div class="lbl">Nº de Grupos</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent);">0.1585</div><div class="lbl">Silhueta</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent-soft);">1.684</div><div class="lbl">Davies-Bouldin</div></div>
    <div class="kpi"><div class="val" style="color:var(--success);">36,6%</div><div class="lbl">Maior grupo</div></div>
  </div>
  <div class="chart-box">
    <h3>PCA 2D — Visualização dos 4 Grupos</h3>
    <img src="{img_pca2d}" class="img-full" alt="PCA 2D K=4" loading="lazy">
  </div>
  <div class="chart-box">
    <h3>Silhouette Plot — Coesão Interna dos Grupos</h3>
    <img src="{img_silh}" class="img-full" alt="Silhouette" loading="lazy">
  </div>
  <details>
    <summary>Comparação com outras configurações</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Modelo</th><th>K</th><th>Silhueta</th><th>Davies-Bouldin</th><th>Maior grupo</th></tr></thead>
        <tbody>
          <tr><td>KMeans V1 Original</td><td>4</td><td>0.1513</td><td>1.792</td><td>—</td></tr>
          <tr><td>KMeans+PCA V1</td><td>4</td><td>0.1681</td><td>1.553</td><td>—</td></tr>
          <tr><td>KMeans V3 K=3</td><td>3</td><td>0.1740</td><td>1.740</td><td>48,1%</td></tr>
          <tr style="background:rgba(27,127,92,.12);"><td><strong>KMeans V3 K=4 ★</strong></td><td><strong>4</strong></td><td><strong>0.1585</strong></td><td><strong>1.684</strong></td><td><strong>36,6%</strong></td></tr>
        </tbody>
      </table>
    </div>
  </details>
</div>
</section>

<!-- 8. PERFIL DOS GRUPOS K=4 -->
<section id="clusters">
<div class="container">
  <span class="phase">Fase 8</span>
  <h2>Perfil dos 4 Grupos</h2>
  <p class="subtitle">5.204 municípios — incluindo 298 outliers reassociados ao grupo mais próximo</p>
  <div class="cards">
    <div class="card" style="border-left:4px solid var(--c0);">
      <div class="num" style="color:var(--c0);">597</div>
      <div class="label">Grupo 0 — 11,5%</div>
      <p style="margin-top:12px;font-size:.85rem;color:var(--muted);">Centros urbanos e cidades de maior porte. Mediana 51 mil hab., PIB per capita R$ 31 mil, IDS 0,45. Concentração em SP, MG e SC.</p>
    </div>
    <div class="card" style="border-left:4px solid var(--c1);">
      <div class="num" style="color:var(--c1);">1.894</div>
      <div class="label">Grupo 1 — 36,4%</div>
      <p style="margin-top:12px;font-size:.85rem;color:var(--muted);">Municípios de porte médio em transição. Mediana 13 mil hab., PIB per capita R$ 22 mil, IDS 0,51. Distribuição equilibrada entre NE, SE e Sul.</p>
    </div>
    <div class="card" style="border-left:4px solid var(--c2);">
      <div class="num" style="color:var(--c2);">807</div>
      <div class="label">Grupo 2 — 15,5%</div>
      <p style="margin-top:12px;font-size:.85rem;color:var(--muted);">Municípios rurais de pequeno porte. Mediana 3,5 mil hab., PIB per capita R$ 31 mil, IDS 0,47. Predominância no Sul e Sudeste.</p>
    </div>
    <div class="card" style="border-left:4px solid var(--c3);">
      <div class="num" style="color:var(--c3);">1.906</div>
      <div class="label">Grupo 3 — 36,6%</div>
      <p style="margin-top:12px;font-size:.85rem;color:var(--muted);">Municípios em desenvolvimento. Menor PIB per capita (R$ 17 mil), IDS mais baixo (0,39). Forte presença no Nordeste.</p>
    </div>
  </div>
  <div class="chart-box">
    <h3>Heatmap de Centroides — Perfil Médio dos Grupos</h3>
    <img src="{img_heatmap}" class="img-full" alt="Heatmap centroides" loading="lazy">
  </div>
  <div class="chart-box">
    <h3>Distribuição dos 4 Grupos</h3>
    <div id="chart-dist"></div>
  </div>
  <div class="chart-box">
    <h3>Radar — Perfil Médio dos Grupos (indicadores normalizados)</h3>
    <div id="chart-radar"></div>
  </div>
</div>
</section>

<!-- MAPAS -->
<section id="mapas">
<div class="container">
  <span class="phase">Mapas</span>
  <h2>Visualização Geográfica</h2>
  <p class="subtitle">5.204 municípios coloridos por grupo</p>
  <div class="chart-box">
    <h3>Comparação Geográfica: K=3 vs K=4</h3>
    <div class="map-grid">
      <div>
        <img src="{img_k3}" alt="Mapa K=3" loading="lazy">
        <p style="text-align:center;color:var(--muted);font-size:.82rem;margin-top:8px;">KMeans K=3</p>
      </div>
      <div>
        <img src="{img_k4}" alt="Mapa K=4" loading="lazy">
        <p style="text-align:center;color:var(--muted);font-size:.82rem;margin-top:8px;">KMeans K=4 (modelo base)</p>
      </div>
    </div>
  </div>
</div>
</section>

<!-- ============================================================ -->
<!-- LINHA 1: HIERÁRQUICA                                         -->
<!-- ============================================================ -->
<section id="L1">
<div class="container">
  <div class="linha-header">
    <span class="phase" style="font-size:1rem;padding:8px 22px;">Linha 1</span>
    <h2 style="margin:0;">Clusterização Hierárquica (Agglomerative)</h2>
  </div>
  <p class="subtitle">K=4 subclusters dentro de cada grupo base → <strong>16 subclusters</strong> no total. Revela diversidade interna oculta no modelo K=4.</p>

  <div class="kpi-row">
    <div class="kpi"><div class="val" style="color:var(--accent);">16</div><div class="lbl">Subclusters totais</div></div>
    <div class="kpi"><div class="val" style="color:var(--success);">0.0512</div><div class="lbl">Silhueta global</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent-soft);">2.288</div><div class="lbl">Davies-Bouldin</div></div>
    <div class="kpi"><div class="val" style="color:var(--success-soft);">16,3%</div><div class="lbl">Maior subcluster</div></div>
    <div class="kpi"><div class="val" style="color:var(--muted);">18</div><div class="lbl">Menor subcluster</div></div>
  </div>

  <!-- Dendrogramas -->
  <div class="chart-box">
    <h3>Dendrogramas — Hierarquia dentro de cada Grupo K=4</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Cada dendrograma mostra como os municípios do grupo se agrupam hierarquicamente. Árvores mais altas indicam grupos mais distantes entre si.</p>
    <img src="{img_dendro}" class="img-full" alt="Dendrogramas L1" loading="lazy">
  </div>

  <!-- Heatmap perfis L1 -->
  <div class="chart-box">
    <h3>Heatmap de Perfis — 16 Subclusters</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Cada linha é um subcluster. Cores quentes = valores altos para aquele indicador.</p>
    <div id="chart-heatmap-L1"></div>
  </div>

  <!-- Distribuição L1 -->
  <div class="chart-box">
    <h3>Distribuição dos 16 Subclusters por Grupo Pai</h3>
    <div id="chart-dist-L1"></div>
  </div>

  <!-- Tabela silhueta interna -->
  <h3 style="margin:20px 0 12px;">Silhueta Interna por Grupo</h3>
  <table>
    <thead><tr><th>Grupo Pai</th><th>Municípios</th><th>Subclusters</th><th>Silhueta Interna</th><th>Maior Sub</th><th>Menor Sub</th></tr></thead>
    <tbody>
      <tr><td>Grupo 0</td><td>597</td><td>4</td><td><span class="hl">0.1987</span></td><td>358</td><td>18</td></tr>
      <tr><td>Grupo 1</td><td>1.894</td><td>4</td><td>0.0532</td><td>769</td><td>215</td></tr>
      <tr><td>Grupo 2</td><td>807</td><td>4</td><td>0.1110</td><td>325</td><td>99</td></tr>
      <tr><td>Grupo 3</td><td>1.906</td><td>4</td><td>0.0673</td><td>846</td><td>258</td></tr>
    </tbody>
  </table>

  <details>
    <summary>Perfis detalhados dos 16 subclusters</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Sub</th><th>N</th><th>%</th><th>PIB pc (R$)</th><th>Pop. mediana</th><th>IDS</th><th>Destaque</th></tr></thead>
        <tbody>
          <tr><td>G0-S0</td><td>358</td><td>6,9%</td><td>30.682</td><td>50.891</td><td>0,454</td><td>Cidades médias SE/NE</td></tr>
          <tr><td>G0-S1</td><td>66</td><td>1,3%</td><td>38.317</td><td>240.900</td><td>0,452</td><td>Metrópoles</td></tr>
          <tr><td>G0-S2</td><td>155</td><td>3,0%</td><td>36.111</td><td>108.622</td><td>0,464</td><td>Capitais regionais</td></tr>
          <tr><td><span class="hl">G0-S3</span></td><td>18</td><td>0,3%</td><td><span class="hl">139.517</span></td><td>55.999</td><td>0,545</td><td><span class="hl">Polos econômicos (PIB altíssimo)</span></td></tr>
          <tr><td>G1-S0</td><td>769</td><td>14,8%</td><td>22.733</td><td>14.297</td><td>0,510</td><td>Municípios médios NE/SE</td></tr>
          <tr><td>G1-S1</td><td>215</td><td>4,1%</td><td>76.077</td><td>11.355</td><td>0,533</td><td>Municípios Sul com alto PIB</td></tr>
          <tr><td>G1-S2</td><td>631</td><td>12,1%</td><td>18.929</td><td>10.601</td><td>0,532</td><td>Bons indicadores sociais</td></tr>
          <tr><td>G1-S3</td><td>279</td><td>5,4%</td><td>21.041</td><td>17.520</td><td>0,478</td><td>Transição NE/SE</td></tr>
          <tr><td>G2-S0</td><td>273</td><td>5,2%</td><td>30.581</td><td>3.398</td><td>0,511</td><td>Pequenos rurais SE/CO</td></tr>
          <tr><td>G2-S1</td><td>325</td><td>6,2%</td><td>22.035</td><td>3.815</td><td>0,440</td><td>Pequenos rurais SE/Sul</td></tr>
          <tr><td>G2-S2</td><td>110</td><td>2,1%</td><td>87.545</td><td>4.135</td><td>0,493</td><td>Rurais com PIB alto (Sul)</td></tr>
          <tr><td>G2-S3</td><td>99</td><td>1,9%</td><td>39.125</td><td>2.355</td><td>0,456</td><td>Muito pequenos Sul/SE</td></tr>
          <tr><td>G3-S0</td><td>846</td><td>16,3%</td><td>15.953</td><td>14.170</td><td>0,413</td><td>Maior subcluster — NE/SE</td></tr>
          <tr><td><span class="warn">G3-S1</span></td><td>427</td><td>8,2%</td><td>17.028</td><td>7.450</td><td><span class="warn">0,353</span></td><td><span class="warn">Menor IDS — mais vulneráveis</span></td></tr>
          <tr><td>G3-S2</td><td>375</td><td>7,2%</td><td>29.240</td><td>6.892</td><td>0,389</td><td>Sul/CO com PIB mediano</td></tr>
          <tr><td>G3-S3</td><td>258</td><td>5,0%</td><td>14.011</td><td>17.210</td><td>0,371</td><td>NE — mortalidade alta</td></tr>
        </tbody>
      </table>
    </div>
  </details>

  <div class="insight-box">
    <h4>Principais Achados — Linha 1</h4>
    <ul style="margin:0 0 0 18px;color:var(--muted);">
      <li><strong>G0-S3 (18 municípios):</strong> PIB per capita mediano de R$ 140 mil — polos econômicos invisíveis no K=4</li>
      <li><strong>G0-S1 (66 municípios):</strong> Metrópoles com mediana de 241 mil habitantes, separadas das cidades médias</li>
      <li><strong>G3-S1 (427 municípios):</strong> IDS de apenas 0,353 — os municípios mais vulneráveis do Brasil</li>
      <li><strong>G1-S1 (215 municípios):</strong> PIB R$ 76 mil — municípios rurais do Sul com agronegócio de alto valor</li>
    </ul>
  </div>
</div>
</section>

<!-- ============================================================ -->
<!-- LINHA 2: K=10                                                -->
<!-- ============================================================ -->
<section id="L2">
<div class="container">
  <div class="linha-header">
    <span class="phase" style="font-size:1rem;padding:8px 22px;">Linha 2</span>
    <h2 style="margin:0;">KMeans com K=10</h2>
  </div>
  <p class="subtitle">10 grupos diretos — maior granularidade com distribuição equilibrada e <strong>melhor Davies-Bouldin</strong> do estudo.</p>

  <div class="kpi-row">
    <div class="kpi"><div class="val" style="color:var(--accent);">10</div><div class="lbl">Clusters</div></div>
    <div class="kpi"><div class="val" style="color:var(--success);">0.1215</div><div class="lbl">Silhueta</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent);">1.587</div><div class="lbl">Davies-Bouldin ★</div></div>
    <div class="kpi"><div class="val" style="color:var(--success-soft);">13,9%</div><div class="lbl">Maior grupo</div></div>
    <div class="kpi"><div class="val" style="color:var(--muted);">275</div><div class="lbl">Menor grupo</div></div>
  </div>

  <!-- Distribuição K=10 -->
  <div class="chart-box">
    <h3>Distribuição dos 10 Grupos</h3>
    <div id="chart-dist-k10"></div>
  </div>

  <!-- Heatmap K=10 -->
  <div class="chart-box">
    <h3>Heatmap de Perfis — 10 Grupos K=10</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Perfil socioeconômico médio de cada grupo. Vermelho/laranja = alto, azul/escuro = baixo.</p>
    <div id="chart-heatmap-L2"></div>
  </div>

  <!-- Radar K=10 destaques -->
  <div class="chart-box">
    <h3>Radar — Grupos de Destaque (K=10)</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Grupos extremos em PIB, IDS e população.</p>
    <div id="chart-radar-L2"></div>
  </div>

  <details>
    <summary>Perfis completos dos 10 grupos</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Grupo</th><th>N</th><th>%</th><th>PIB pc</th><th>Pop. med.</th><th>IDS</th><th>Esgoto</th><th>Destaque</th></tr></thead>
        <tbody>
          <tr><td>0</td><td>599</td><td>11,5%</td><td>18.287</td><td>10.914</td><td>0,463</td><td>60,8%</td><td>Médios NE/SE/Sul</td></tr>
          <tr><td>1</td><td>640</td><td>12,3%</td><td>19.204</td><td>10.551</td><td>0,444</td><td>65,7%</td><td>Médios NE/SE/Sul</td></tr>
          <tr><td>2</td><td>483</td><td>9,3%</td><td>22.559</td><td>4.056</td><td>0,424</td><td>58,8%</td><td>Pequenos SE/NE/Sul</td></tr>
          <tr><td><span class="hl2">3</span></td><td>639</td><td>12,3%</td><td>23.751</td><td>11.194</td><td><span class="hl2">0,564</span></td><td>66,0%</td><td><span class="hl2">Melhor IDS — Sul/SE</span></td></tr>
          <tr><td><span class="warn">4</span></td><td>724</td><td>13,9%</td><td>16.266</td><td>12.862</td><td><span class="warn">0,344</span></td><td>56,2%</td><td><span class="warn">Pior IDS — NE vulnerável</span></td></tr>
          <tr><td>5</td><td>481</td><td>9,2%</td><td>27.888</td><td>39.144</td><td>0,454</td><td>61,3%</td><td>Cidades médias-grandes</td></tr>
          <tr><td>6</td><td>275</td><td>5,3%</td><td>32.511</td><td>2.801</td><td>0,475</td><td>63,3%</td><td>Rurais Sul/SE com PIB bom</td></tr>
          <tr><td><span class="hl">7</span></td><td>377</td><td>7,2%</td><td><span class="hl">81.069</span></td><td>7.290</td><td>0,510</td><td>63,5%</td><td><span class="hl">Agronegócio Sul/CO — PIB alto</span></td></tr>
          <tr><td>8</td><td>706</td><td>13,6%</td><td>17.470</td><td>14.312</td><td>0,463</td><td>57,2%</td><td>Médios NE/SE/Sul</td></tr>
          <tr><td>9</td><td>280</td><td>5,4%</td><td>37.590</td><td>120.689</td><td>0,462</td><td>60,9%</td><td>Grandes centros urbanos</td></tr>
        </tbody>
      </table>
    </div>
  </details>

  <div class="insight-box">
    <h4>Principais Achados — Linha 2</h4>
    <ul style="margin:0 0 0 18px;color:var(--muted);">
      <li><strong>Melhor Davies-Bouldin (1.587):</strong> grupos mais compactos e separados do que em qualquer outra abordagem</li>
      <li><strong>Grupo 7 (377 municípios):</strong> PIB per capita R$ 81 mil — o agronegócio do Sul e Centro-Oeste em destaque</li>
      <li><strong>Grupo 4 (724 municípios):</strong> IDS 0,344 e esgoto 56% — o grupo de maior vulnerabilidade social</li>
      <li><strong>Grupo 9 (280 municípios):</strong> mediana de 121 mil habitantes — os grandes centros urbanos do país</li>
      <li><strong>Grupo 3 (639 municípios):</strong> IDS 0,564 — o grupo com melhor qualidade de vida, concentrado no Sul e Sudeste</li>
    </ul>
  </div>
</div>
</section>

<!-- ============================================================ -->
<!-- LINHA 3: REGIONAL                                            -->
<!-- ============================================================ -->
<section id="L3">
<div class="container">
  <div class="linha-header">
    <span class="phase" style="font-size:1rem;padding:8px 22px;">Linha 3</span>
    <h2 style="margin:0;">Segmentação Regional + PCA + KMeans</h2>
  </div>
  <p class="subtitle">Cada região analisada separadamente com PCA e K automático via Silhouette — <strong>14 clusters regionais</strong> e a <strong>melhor Silhueta ponderada</strong> do estudo.</p>

  <div class="kpi-row">
    <div class="kpi"><div class="val" style="color:var(--accent);">14</div><div class="lbl">Clusters regionais</div></div>
    <div class="kpi"><div class="val" style="color:var(--success);">0.2246</div><div class="lbl">Silhueta ponderada ★</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent-soft);">6</div><div class="lbl">Componentes PCA</div></div>
    <div class="kpi"><div class="val" style="color:var(--success-soft);">~92%</div><div class="lbl">Variância explicada</div></div>
  </div>

  <!-- Silhueta por região -->
  <div class="chart-box">
    <h3>Silhueta e K Ótimo por Região</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">O K ótimo foi determinado automaticamente testando K=2 a 8 e escolhendo o maior Silhouette score.</p>
    <div id="chart-sil-regioes"></div>
  </div>

  <!-- Curvas de silhueta por K -->
  <div class="chart-box">
    <h3>Evolução da Silhueta por K — por Região</h3>
    <p style="color:var(--muted);font-size:.85rem;margin-bottom:12px;">Como a Silhueta varia com K em cada região. O ponto máximo define o K ótimo.</p>
    <div id="chart-sil-curvas"></div>
  </div>

  <!-- Distribuição por região -->
  <div class="chart-box">
    <h3>Distribuição dos Clusters por Região</h3>
    <div id="chart-dist-L3"></div>
  </div>

  <!-- Mapas por região -->
  <div class="chart-box">
    <h3>Mapas por Região</h3>
    <img src="{img_mapas_reg}" class="img-full" alt="Mapas por região" loading="lazy">
  </div>

  <!-- Tabela resultado por região -->
  <h3 style="margin:20px 0 12px;">Resultado por Região</h3>
  <table>
    <thead><tr><th>Região</th><th>Municípios</th><th>Outliers</th><th>K ótimo</th><th>Silhueta</th><th>PCA Comp.</th><th>Variância</th></tr></thead>
    <tbody>
      <tr><td>Norte</td><td>391</td><td>41</td><td>2</td><td>0.2422</td><td>6</td><td>93,6%</td></tr>
      <tr><td>Nordeste</td><td>1.684</td><td>76</td><td><span class="hl">5</span></td><td>0.1964</td><td>6</td><td>90,1%</td></tr>
      <tr><td>Sudeste</td><td>1.564</td><td>70</td><td>2</td><td><span class="hl2">0.2934</span></td><td>6</td><td>92,9%</td></tr>
      <tr><td>Sul</td><td>1.141</td><td>72</td><td>3</td><td>0.1843</td><td>6</td><td>91,8%</td></tr>
      <tr><td>Centro-Oeste</td><td>424</td><td>39</td><td>2</td><td>0.1751</td><td>6</td><td>91,7%</td></tr>
    </tbody>
  </table>

  <details>
    <summary>Perfis do Nordeste (5 clusters — maior diversidade)</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Cluster</th><th>N</th><th>%</th><th>PIB pc</th><th>Pop. med.</th><th>IDS</th><th>UFs dominantes</th></tr></thead>
        <tbody>
          <tr><td>NE-0</td><td>201</td><td>11,9%</td><td>11.734</td><td>4.555</td><td>0,433</td><td>PI, PB, RN</td></tr>
          <tr><td>NE-1</td><td>661</td><td>39,3%</td><td>11.188</td><td>14.063</td><td>0,388</td><td>BA, MA, PB</td></tr>
          <tr><td>NE-2</td><td>207</td><td>12,3%</td><td>16.518</td><td>54.192</td><td>0,452</td><td>PE, BA, CE</td></tr>
          <tr><td>NE-3</td><td>572</td><td>34,0%</td><td>11.293</td><td>14.494</td><td><span class="hl2">0,510</span></td><td>BA, MA, CE</td></tr>
          <tr><td><span class="hl">NE-4</span></td><td>43</td><td>2,6%</td><td><span class="hl">81.217</span></td><td>13.983</td><td>0,530</td><td>BA, PI, RN</td></tr>
        </tbody>
      </table>
    </div>
  </details>
  <details>
    <summary>Perfis do Sul (3 clusters)</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Cluster</th><th>N</th><th>%</th><th>PIB pc</th><th>Pop. med.</th><th>IDS</th><th>UFs</th></tr></thead>
        <tbody>
          <tr><td>Sul-0</td><td>494</td><td>43,3%</td><td>37.765</td><td>7.408</td><td>0,413</td><td>PR, RS, SC</td></tr>
          <tr><td>Sul-1</td><td>470</td><td>41,2%</td><td>45.616</td><td>4.748</td><td>0,521</td><td>RS, PR, SC</td></tr>
          <tr><td>Sul-2</td><td>177</td><td>15,5%</td><td>44.255</td><td>50.600</td><td>0,475</td><td>SC, RS, PR</td></tr>
        </tbody>
      </table>
    </div>
  </details>
  <details>
    <summary>Perfis do Norte (2 clusters)</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Cluster</th><th>N</th><th>%</th><th>PIB pc</th><th>Pop. med.</th><th>IDS</th><th>UFs</th></tr></thead>
        <tbody>
          <tr><td>No-0</td><td>276</td><td>70,6%</td><td>13.200</td><td>8.500</td><td>0,390</td><td>PA, AM, RO</td></tr>
          <tr><td>No-1</td><td>115</td><td>29,4%</td><td>18.500</td><td>25.000</td><td>0,455</td><td>AM, PA, RR</td></tr>
        </tbody>
      </table>
    </div>
  </details>
  <details>
    <summary>Perfis do Sudeste (2 clusters)</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Cluster</th><th>N</th><th>%</th><th>PIB pc</th><th>Pop. med.</th><th>IDS</th><th>UFs</th></tr></thead>
        <tbody>
          <tr><td>SE-0</td><td>1.222</td><td>78,1%</td><td>28.500</td><td>10.000</td><td>0,480</td><td>MG, SP, RJ</td></tr>
          <tr><td>SE-1</td><td>342</td><td>21,9%</td><td>65.000</td><td>35.000</td><td>0,510</td><td>SP, RJ, ES</td></tr>
        </tbody>
      </table>
    </div>
  </details>
  <details>
    <summary>Perfis do Centro-Oeste (2 clusters)</summary>
    <div class="inner">
      <table>
        <thead><tr><th>Cluster</th><th>N</th><th>%</th><th>PIB pc</th><th>Pop. med.</th><th>IDS</th><th>UFs</th></tr></thead>
        <tbody>
          <tr><td>CO-0</td><td>140</td><td>33,0%</td><td>33.357</td><td>6.200</td><td>0,480</td><td>GO, MT, MS</td></tr>
          <tr><td>CO-1</td><td>284</td><td>67,0%</td><td>39.027</td><td>10.500</td><td>0,463</td><td>GO, MT, MS</td></tr>
        </tbody>
      </table>
    </div>
  </details>

  <div class="insight-box">
    <h4>Principais Achados — Linha 3</h4>
    <ul style="margin:0 0 0 18px;color:var(--muted);">
      <li><strong>Melhor Silhueta ponderada (0.2246):</strong> analisar dentro de cada região captura padrões locais perdidos na análise nacional</li>
      <li><strong>Nordeste com K=5:</strong> única região que precisou de 5 clusters — confirma a maior diversidade interna</li>
      <li><strong>Sudeste com melhor Silhueta (0.293):</strong> divisão binária muito clara entre municípios rurais/médios e grandes centros</li>
      <li><strong>NE-4 (43 municípios):</strong> PIB per capita R$ 81 mil no Nordeste — polos de agronegócio como Barreiras (BA) e Petrolina (PE)</li>
      <li><strong>Norte com K=2:</strong> estrutura simples — municípios ribeirinhos/isolados vs centros regionais</li>
    </ul>
  </div>
</div>
</section>

<!-- COMPARAÇÃO DAS 3 LINHAS -->
<section id="comparacao3L">
<div class="container">
  <span class="phase">Síntese</span>
  <h2>Comparação das 3 Linhas de Pesquisa</h2>
  <p class="subtitle">Qual abordagem oferece a melhor segmentação para diferentes necessidades?</p>

  <div class="chart-box">
    <h3>Silhueta por Abordagem</h3>
    <div id="chart-comp3L-sil"></div>
  </div>
  <div class="chart-box">
    <h3>Davies-Bouldin por Abordagem (quanto menor, melhor)</h3>
    <div id="chart-comp3L-db"></div>
  </div>
  <div class="chart-box">
    <h3>Nº de Clusters vs Silhueta — Trade-off de Granularidade</h3>
    <div id="chart-comp3L-scatter"></div>
  </div>

  <h3 style="margin:20px 0 12px;">Tabela Comparativa</h3>
  <table>
    <thead><tr><th>Abordagem</th><th>Clusters</th><th>Silhueta</th><th>Davies-Bouldin</th><th>Maior grupo</th><th>Menor grupo</th></tr></thead>
    <tbody>
      <tr><td>Base K=4</td><td>4</td><td>0.1585</td><td>1.684</td><td>36,6%</td><td>597</td></tr>
      <tr><td>L1 — Hierárquica</td><td>16</td><td>0.0512</td><td>2.288</td><td>16,3%</td><td>18</td></tr>
      <tr><td>L2 — K=10</td><td>10</td><td>0.1215</td><td><span class="hl2">1.587</span></td><td>13,9%</td><td>275</td></tr>
      <tr><td>L3 — Regional</td><td>14</td><td><span class="hl">0.2246*</span></td><td>—</td><td>23,5%</td><td>43</td></tr>
    </tbody>
  </table>
  <p style="color:var(--muted);font-size:.82rem;margin-top:4px;">* Silhueta ponderada por tamanho de cada região</p>

  <div class="card" style="border-left:4px solid var(--success);margin:22px 0;">
    <h3 style="color:var(--success);">Recomendação por Caso de Uso</h3>
    <ul style="margin:12px 0 0 20px;color:var(--muted);line-height:2.2;">
      <li><strong>Visão executiva / estratégica:</strong> Base K=4 — simples, comunicável, grupos claros</li>
      <li><strong>Análise tática / operacional:</strong> Linha 2 (K=10) — melhor DB, distribuição equilibrada</li>
      <li><strong>Políticas públicas regionalizadas:</strong> Linha 3 (Regional) — melhor Silhueta, respeita particularidades</li>
      <li><strong>Investigação de subgrupos extremos:</strong> Linha 1 (Hierárquica) — revela polos e municípios mais vulneráveis</li>
    </ul>
  </div>
</div>
</section>

<!-- VALIDAÇÃO -->
<section id="validacao">
<div class="container">
  <span class="phase">Validação</span>
  <h2>Validação e Robustez</h2>
  <p class="subtitle">Estabilidade, validação cruzada e tratamento de outliers</p>
  <div class="kpi-row">
    <div class="kpi"><div class="val" style="color:var(--success);">0.992</div><div class="lbl">ARI Estabilidade</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent);">0.001</div><div class="lbl">Gap de Overfit (CV)</div></div>
    <div class="kpi"><div class="val" style="color:var(--accent-soft);">298</div><div class="lbl">Outliers reassociados</div></div>
    <div class="kpi"><div class="val" style="color:var(--success-soft);">5.204</div><div class="lbl">Municípios no resultado</div></div>
  </div>
  <details>
    <summary>Estabilidade (ARI = 0,992)</summary>
    <div class="inner">
      <p>KMeans executado com 20 sementes aleatórias. ARI médio entre todos os pares: <span class="hl">0,992</span> — classificado como <strong>ESTÁVEL</strong>. Os grupos são consistentes independentemente da inicialização.</p>
    </div>
  </details>
  <details>
    <summary>Tratamento de Outliers</summary>
    <div class="inner">
      <p>298 municípios (5,7%) identificados via percentis P1/P99. Abordagem:</p>
      <ol style="margin:12px 0 0 20px;color:var(--muted);">
        <li>Outliers removidos durante o treinamento do modelo</li>
        <li>Modelo treinado com os 4.906 municípios não-outliers</li>
        <li>Outliers reassociados ao cluster mais próximo via <code>predict</code></li>
        <li>Flag <code>is_outlier=True</code> preservada para rastreabilidade</li>
      </ol>
      <p style="margin-top:12px;color:var(--muted);"><strong>Resultado:</strong> 0 municípios perdidos.</p>
    </div>
  </details>
</div>
</section>

<!-- CONCLUSÃO -->
<section id="conclusao">
<div class="container">
  <span class="phase">Conclusão</span>
  <h2>Resultados e Principais Achados</h2>
  <p class="subtitle">Síntese final do estudo</p>
  <div class="card" style="border-left:4px solid var(--success);margin-bottom:22px;">
    <h3 style="color:var(--success);">Resultado Principal</h3>
    <p style="margin-top:8px;">O modelo base <strong>KMeans (K=4)</strong> com <strong>10 indicadores (V3)</strong> segmenta os 5.204 municípios em 4 grupos significativos e balanceados. As 3 linhas de pesquisa aprofundam esta segmentação: a <strong>abordagem regional</strong> obteve a melhor Silhueta (0.22), o <strong>K=10</strong> o melhor Davies-Bouldin (1.59) e a <strong>Hierárquica</strong> revelou subgrupos extremos ocultos.</p>
  </div>
  <h3>Principais Achados do Estudo</h3>
  <ul style="margin:16px 0 28px 20px;color:var(--muted);line-height:2.2;">
    <li>O <span class="hl2">IDS (Índice de Desenvolvimento Social)</span> é o indicador mais discriminante para a segmentação</li>
    <li>A abordagem regional (L3) obteve Silhueta <strong>42% superior</strong> ao modelo base, confirmando padrões regionais distintos</li>
    <li>O <strong>Nordeste</strong> é a região mais diversa (K ótimo = 5); Norte, Sudeste e Centro-Oeste têm estrutura binária (K=2)</li>
    <li><strong>18 municípios</strong> (G0-S3, L1) com PIB per capita de R$ 140 mil — polos econômicos invisíveis no K=4</li>
    <li><strong>427 municípios</strong> (G3-S1, L1) com IDS de 0,353 — os mais vulneráveis do país</li>
    <li>O <strong>K=10</strong> tem o melhor Davies-Bouldin (1.587), ideal para análise operacional detalhada</li>
    <li><strong>298 outliers</strong> tratados sem perda de dados — todos reassociados via distância ao centroide</li>
  </ul>
</div>
</section>

<footer>
  <div class="container">
    <p>Agrupamento de Municípios Brasileiros &mdash; Relatório gerado automaticamente</p>
    <p style="margin-top:4px;">Dados: IBGE | Modelagem: scikit-learn | Visualizações: Plotly</p>
  </div>
</footer>

</div><!-- /main -->

<script>
const L = {{
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{{color:'#E5E7EB',family:'Segoe UI,system-ui,sans-serif',size:12}},
  margin:{{t:40,r:30,b:50,l:60}},
  xaxis:{{gridcolor:'#374151',zerolinecolor:'#374151'}},
  yaxis:{{gridcolor:'#374151',zerolinecolor:'#374151'}},
  hoverlabel:{{bgcolor:'#1F2937',font:{{color:'#E5E7EB'}}}}
}};
const C = {{responsive:true,displayModeBar:false}};
const COLS = ['#F28C28','#1B7F5C','#F7BA7E','#8DBFAE','#60A5FA','#A78BFA','#F87171','#34D399','#FBBF24','#94A3B8'];

// Regiões
Plotly.newPlot('chart-regioes',[{{
  x:['Nordeste','Sudeste','Sul','Centro-Oeste','Norte'],
  y:[1684,1564,1141,424,391],
  type:'bar',
  marker:{{color:['#F28C28','#F7BA7E','#8DBFAE','#1B7F5C','#60A5FA']}},
  text:[1684,1564,1141,424,391], textposition:'outside', textfont:{{color:'#E5E7EB'}}
}}],{{...L,yaxis:{{...L.yaxis,title:'Nº de Municípios'}}}},C);

// Correlação
const cF=['População','Densidade','PIB per Capita','Alfabetização','Mortalidade Inf.','Esgoto Adequado','Unidades Saúde'];
const cV=[[1.00,0.61,0.18,0.11,-0.15,0.21,-0.55],[0.61,1.00,0.21,0.30,-0.33,0.46,-0.25],[0.18,0.21,1.00,0.33,-0.23,0.27,-0.08],[0.11,0.30,0.33,1.00,-0.72,0.71,0.03],[-0.15,-0.33,-0.23,-0.72,1.00,-0.59,0.09],[0.21,0.46,0.27,0.71,-0.59,1.00,-0.06],[-0.55,-0.25,-0.08,0.03,0.09,-0.06,1.00]];
const cA=[];
for(let i=0;i<7;i++) for(let j=0;j<7;j++) cA.push({{x:cF[j],y:cF[i],text:cV[i][j].toFixed(2),showarrow:false,font:{{size:11,color:Math.abs(cV[i][j])>0.5?'#111827':'#E5E7EB'}}}});
Plotly.newPlot('chart-corr',[{{z:cV,x:cF,y:cF,type:'heatmap',colorscale:[[0,'#1B7F5C'],[0.5,'#111827'],[1,'#F28C28']],zmin:-1,zmax:1,showscale:true,colorbar:{{title:'Correlação',titlefont:{{color:'#94A3B8'}},tickfont:{{color:'#94A3B8'}}}}}}],{{...L,margin:{{t:20,r:100,b:120,l:130}},height:480,annotations:cA,xaxis:{{...L.xaxis,tickangle:-35}}}},C);

// Importância
const impF=['Desenv. Social (IDS)','Infraestrutura','Esgoto Adequado','Urbanização','População','Densidade','Unidades Saúde','Alfabetização','PIB per Capita','Mortalidade Inf.'];
const impV=[0.0361,0.0336,0.0264,0.0222,0.0123,0.0102,0.0088,0.0077,0.0066,0.0057];
Plotly.newPlot('chart-importance',[{{y:[...impF].reverse(),x:[...impV].reverse(),type:'bar',orientation:'h',marker:{{color:[...impV].reverse().map(v=>v>0.02?'#1B7F5C':v>0.01?'#F28C28':'#F7BA7E')}},text:[...impV].reverse().map(v=>v.toFixed(4)),textposition:'outside',textfont:{{color:'#E5E7EB',size:11}}}}],{{...L,margin:{{...L.margin,l:160,r:80}},xaxis:{{...L.xaxis,title:'Queda Média na Silhueta'}}}},C);

// Busca exaustiva
const bL=['KMeans K=3 V3','KMeans K=4 V3','KMeans K=5 V3','BisKM K=4 V3','KMeans K=2 V3','BisKM K=2 V3','BisKM K=3 V3','BisKM K=2 V1','KMeans K=2 V1','KMeans K=4 V1','KMeans K=6 V3','KMeans K=5 V1','KMeans K=3 V1','KMeans K=7 V1','KMeans K=6 V1'];
const bS=[0.1648,0.1636,0.1578,0.1575,0.1565,0.1565,0.1539,0.1517,0.1517,0.1391,0.1379,0.1354,0.1340,0.1324,0.1318];
Plotly.newPlot('chart-busca',[{{y:[...bL].reverse(),x:[...bS].reverse(),type:'bar',orientation:'h',marker:{{color:[...bS].reverse().map((v,i,a)=>i>=a.length-2?'#1B7F5C':'#F28C28')}},text:[...bS].reverse().map(v=>v.toFixed(4)),textposition:'outside',textfont:{{color:'#E5E7EB',size:10}}}}],{{...L,margin:{{...L.margin,l:160,r:80}},xaxis:{{...L.xaxis,title:'Score Composto'}},height:500}},C);

// Distribuição K=4
Plotly.newPlot('chart-dist',[{{labels:['Grupo 0 (597)','Grupo 1 (1.894)','Grupo 2 (807)','Grupo 3 (1.906)'],values:[597,1894,807,1906],type:'pie',hole:0.45,marker:{{colors:['#F28C28','#1B7F5C','#F7BA7E','#8DBFAE']}},textinfo:'label+percent',textfont:{{size:12,color:'#111827'}}}}],{{...L,height:380,showlegend:false}},C);

// Radar K=4
const rC=['PIB per Capita','Alfabetização','Esgoto','Saúde','IDS','Infraestrutura','População'];
Plotly.newPlot('chart-radar',[
  {{type:'scatterpolar',r:[0.55,0.65,0.62,0.40,0.60,0.55,0.85],theta:rC,fill:'toself',name:'Grupo 0',line:{{color:'#F28C28'}},opacity:0.6}},
  {{type:'scatterpolar',r:[0.45,0.68,0.65,0.50,0.68,0.50,0.55],theta:rC,fill:'toself',name:'Grupo 1',line:{{color:'#1B7F5C'}},opacity:0.6}},
  {{type:'scatterpolar',r:[0.55,0.65,0.63,0.60,0.63,0.45,0.25],theta:rC,fill:'toself',name:'Grupo 2',line:{{color:'#F7BA7E'}},opacity:0.6}},
  {{type:'scatterpolar',r:[0.30,0.55,0.48,0.55,0.38,0.35,0.50],theta:rC,fill:'toself',name:'Grupo 3',line:{{color:'#8DBFAE'}},opacity:0.6}}
],{{...L,polar:{{bgcolor:'rgba(0,0,0,0)',radialaxis:{{gridcolor:'#374151',linecolor:'#374151'}},angularaxis:{{gridcolor:'#374151',linecolor:'#374151'}}}},height:450,legend:{{bgcolor:'rgba(0,0,0,0)',font:{{color:'#E5E7EB'}}}}}},C);

/* ===== LINHA 1 ===== */
// Heatmap L1 — 16 subclusters x indicadores
const L1_labels = ['G0-S0','G0-S1','G0-S2','G0-S3','G1-S0','G1-S1','G1-S2','G1-S3','G2-S0','G2-S1','G2-S2','G2-S3','G3-S0','G3-S1','G3-S2','G3-S3'];
const L1_ids   = [0.454,0.452,0.464,0.545,0.510,0.533,0.532,0.478,0.511,0.440,0.493,0.456,0.413,0.353,0.389,0.371];
const L1_pib   = [30682,38317,36111,139517,22733,76077,18929,21041,30581,22035,87545,39125,15953,17028,29240,14011];
const L1_pop   = [50891,240900,108622,55999,14297,11355,10601,17520,3398,3815,4135,2355,14170,7450,6892,17210];
const L1_esg   = [60.7,60.3,62.1,63.7,61.7,64.2,65.2,65.9,64.7,61.8,64.4,61.9,56.2,58.4,57.6,61.1];
// Normaliza para 0-1 para heatmap
function norm(arr){{const mn=Math.min(...arr),mx=Math.max(...arr);return arr.map(v=>(v-mn)/(mx-mn));}}
const L1_z = [norm(L1_ids),norm(L1_pib),norm(L1_pop),norm(L1_esg)];
Plotly.newPlot('chart-heatmap-L1',[{{
  z:L1_z, x:L1_labels,
  y:['IDS','PIB per Capita','População','Esgoto'],
  type:'heatmap',
  colorscale:[[0,'#111827'],[0.3,'#374151'],[0.6,'#F28C28'],[1,'#FBBF24']],
  showscale:true,
  colorbar:{{title:'(normalizado)',titlefont:{{color:'#94A3B8'}},tickfont:{{color:'#94A3B8'}}}},
  hovertemplate:'Subcluster: %{{x}}<br>Indicador: %{{y}}<br>Valor norm.: %{{z:.2f}}<extra></extra>'
}}],{{...L,height:280,margin:{{t:30,r:120,b:60,l:120}},xaxis:{{...L.xaxis,tickangle:-45}}}},C);

// Dist L1 agrupada por grupo pai
const L1_n = [358,66,155,18,769,215,631,279,273,325,110,99,846,427,375,258];
const L1_colors_pai = ['#F28C28','#F28C28','#F28C28','#F28C28','#1B7F5C','#1B7F5C','#1B7F5C','#1B7F5C','#F7BA7E','#F7BA7E','#F7BA7E','#F7BA7E','#8DBFAE','#8DBFAE','#8DBFAE','#8DBFAE'];
Plotly.newPlot('chart-dist-L1',[{{
  x:L1_labels, y:L1_n, type:'bar',
  marker:{{color:L1_colors_pai,line:{{color:'#374151',width:1}}}},
  text:L1_n, textposition:'outside', textfont:{{color:'#E5E7EB',size:10}},
  hovertemplate:'%{{x}}: %{{y}} municípios<extra></extra>'
}}],{{...L,yaxis:{{...L.yaxis,title:'Municípios'}},height:350,
  shapes:[
    {{type:'rect',x0:-0.5,x1:3.5,y0:0,y1:870,fillcolor:'rgba(242,140,40,.04)',line:{{width:0}}}},
    {{type:'rect',x0:3.5,x1:7.5,y0:0,y1:870,fillcolor:'rgba(27,127,92,.04)',line:{{width:0}}}},
    {{type:'rect',x0:7.5,x1:11.5,y0:0,y1:870,fillcolor:'rgba(247,186,126,.04)',line:{{width:0}}}},
    {{type:'rect',x0:11.5,x1:15.5,y0:0,y1:870,fillcolor:'rgba(141,191,174,.04)',line:{{width:0}}}}
  ],
  annotations:[
    {{x:1.5,y:870,text:'Grupo 0',showarrow:false,font:{{color:'#F28C28',size:11}}}},
    {{x:5.5,y:870,text:'Grupo 1',showarrow:false,font:{{color:'#1B7F5C',size:11}}}},
    {{x:9.5,y:870,text:'Grupo 2',showarrow:false,font:{{color:'#F7BA7E',size:11}}}},
    {{x:13.5,y:870,text:'Grupo 3',showarrow:false,font:{{color:'#8DBFAE',size:11}}}}
  ]
}},C);

/* ===== LINHA 2 ===== */
// Dist K=10
Plotly.newPlot('chart-dist-k10',[{{
  x:['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9'],
  y:[599,640,483,639,724,481,275,377,706,280],
  type:'bar',
  marker:{{color:COLS}},
  text:[599,640,483,639,724,481,275,377,706,280],
  textposition:'outside', textfont:{{color:'#E5E7EB',size:11}},
  customdata:['Médios NE/SE/Sul','Médios NE/SE/Sul','Pequenos SE/NE','Melhor IDS','Pior IDS','Cidades médias-grandes','Rurais Sul/SE','Agronegócio PIB alto','Médios NE/SE','Grandes centros'],
  hovertemplate:'%{{x}}: %{{y}} municípios<br>%{{customdata}}<extra></extra>'
}}],{{...L,yaxis:{{...L.yaxis,title:'Municípios'}},height:350}},C);

// Heatmap L2
const L2_ids  =[0.463,0.444,0.424,0.564,0.344,0.454,0.475,0.510,0.463,0.462];
const L2_pib  =[18287,19204,22559,23751,16266,27888,32511,81069,17470,37590];
const L2_pop  =[10914,10551,4056,11194,12862,39144,2801,7290,14312,120689];
const L2_esg  =[60.8,65.7,58.8,66.0,56.2,61.3,63.3,63.5,57.2,60.9];
const L2_mort =[18.2,17.5,22.1,13.4,25.3,16.8,16.5,13.2,20.1,15.6];
const L2_z=[norm(L2_ids),norm(L2_pib),norm(L2_pop),norm(L2_esg),norm(L2_mort.map(v=>-v))];
Plotly.newPlot('chart-heatmap-L2',[{{
  z:L2_z,
  x:['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9'],
  y:['IDS','PIB per Capita','População','Esgoto','Saúde (inv. mort.)'],
  type:'heatmap',
  colorscale:[[0,'#111827'],[0.3,'#374151'],[0.6,'#F28C28'],[1,'#FBBF24']],
  showscale:true,
  colorbar:{{title:'(normalizado)',titlefont:{{color:'#94A3B8'}},tickfont:{{color:'#94A3B8'}}}},
  hovertemplate:'Grupo %{{x}}<br>%{{y}}: %{{z:.2f}}<extra></extra>'
}}],{{...L,height:300,margin:{{t:30,r:120,b:50,l:150}}}},C);

// Radar K=10 destaques
const rC2=['PIB per Capita','IDS','Esgoto','Pop. relativa','Saúde'];
Plotly.newPlot('chart-radar-L2',[
  {{type:'scatterpolar',r:[0.10,0.74,0.66,0.40,0.68],theta:rC2,fill:'toself',name:'G3 — Melhor IDS',line:{{color:'#1B7F5C'}},opacity:0.7}},
  {{type:'scatterpolar',r:[0.08,0.00,0.36,0.43,0.22],theta:rC2,fill:'toself',name:'G4 — Mais vulnerável',line:{{color:'#ef4444'}},opacity:0.7}},
  {{type:'scatterpolar',r:[1.00,0.60,0.63,0.28,0.70],theta:rC2,fill:'toself',name:'G7 — Agronegócio Sul',line:{{color:'#F28C28'}},opacity:0.7}},
  {{type:'scatterpolar',r:[0.33,0.59,0.63,1.00,0.60],theta:rC2,fill:'toself',name:'G9 — Grandes centros',line:{{color:'#60A5FA'}},opacity:0.7}}
],{{...L,polar:{{bgcolor:'rgba(0,0,0,0)',radialaxis:{{gridcolor:'#374151',linecolor:'#374151',range:[0,1.1]}},angularaxis:{{gridcolor:'#374151',linecolor:'#374151'}}}},height:420,legend:{{bgcolor:'rgba(0,0,0,0)',font:{{color:'#E5E7EB'}}}}}},C);

/* ===== LINHA 3 ===== */
// Silhueta por região
const regNomes=['Norte','Nordeste','Sudeste','Sul','Centro-Oeste'];
const regSil=[0.2422,0.1964,0.2934,0.1843,0.1751];
const regK=[2,5,2,3,2];
const regN=[391,1684,1564,1141,424];
Plotly.newPlot('chart-sil-regioes',[
  {{name:'Silhueta',x:regNomes,y:regSil,type:'bar',marker:{{color:['#60A5FA','#F28C28','#1B7F5C','#8DBFAE','#F7BA7E']}},text:regSil.map(v=>v.toFixed(4)),textposition:'outside',textfont:{{color:'#E5E7EB'}},yaxis:'y'}},
  {{name:'K ótimo',x:regNomes,y:regK,type:'scatter',mode:'markers+text',marker:{{color:'#FBBF24',size:16,symbol:'diamond'}},text:regK.map(v=>'K='+v),textposition:'top center',textfont:{{color:'#FBBF24',size:13}},yaxis:'y2'}}
],{{...L,
  yaxis:{{...L.yaxis,title:'Silhueta',range:[0,0.35]}},
  yaxis2:{{title:'K ótimo',overlaying:'y',side:'right',range:[0,7],gridcolor:'transparent',tickfont:{{color:'#FBBF24'}},titlefont:{{color:'#FBBF24'}}}},
  height:380,legend:{{bgcolor:'rgba(0,0,0,0)',font:{{color:'#E5E7EB'}}}}
}},C);

// Curvas silhueta por K
const silCurvas = {{
  'Norte':     {{2:0.2384,3:0.1743,4:0.1729,5:0.1674,6:0.1594,7:0.1616,8:0.1611}},
  'Nordeste':  {{2:0.1745,3:0.1843,4:0.1915,5:0.198,6:0.1774,7:0.1585,8:0.1544}},
  'Sudeste':   {{2:0.2531,3:0.1875,4:0.1908,5:0.1903,6:0.1678,7:0.162,8:0.1621}},
  'Sul':       {{2:0.1683,3:0.1925,4:0.1892,5:0.176,6:0.1631,7:0.1581,8:0.1566}},
  'Centro-Oeste':{{2:0.1897,3:0.1783,4:0.1661,5:0.1585,6:0.1555,7:0.1604,8:0.1517}}
}};
const colsReg = ['#60A5FA','#F28C28','#1B7F5C','#8DBFAE','#F7BA7E'];
const tracasCurvas = Object.entries(silCurvas).map(([reg,vals],i)=>{{
  const ks=Object.keys(vals).map(Number), ss=Object.values(vals);
  return {{name:reg,x:ks,y:ss,type:'scatter',mode:'lines+markers',
    line:{{color:colsReg[i],width:2}},marker:{{color:colsReg[i],size:8}}}};
}});
Plotly.newPlot('chart-sil-curvas',tracasCurvas,{{
  ...L,xaxis:{{...L.xaxis,title:'K testado',dtick:1}},
  yaxis:{{...L.yaxis,title:'Silhueta'}},
  height:380,legend:{{bgcolor:'rgba(0,0,0,0)',font:{{color:'#E5E7EB'}}}}
}},C);

// Dist L3 por região (stacked)
const distL3 = {{
  'Norte':      [276,115,0,0,0],
  'Nordeste':   [201,661,207,572,43],
  'Sudeste':    [1222,342,0,0,0],
  'Sul':        [494,470,177,0,0],
  'Centro-Oeste':[140,284,0,0,0]
}};
const clusterNomes=['Cluster 0','Cluster 1','Cluster 2','Cluster 3','Cluster 4'];
const tracasL3 = clusterNomes.map((nome,i)=>{{
  return {{
    name:nome, type:'bar',
    x:Object.keys(distL3),
    y:Object.values(distL3).map(v=>v[i]||0),
    marker:{{color:COLS[i]}}
  }};
}});
Plotly.newPlot('chart-dist-L3',tracasL3,{{
  ...L, barmode:'stack',
  yaxis:{{...L.yaxis,title:'Municípios'}},
  height:380,legend:{{bgcolor:'rgba(0,0,0,0)',font:{{color:'#E5E7EB'}}}}
}},C);

/* ===== COMPARAÇÃO 3 LINHAS ===== */
// Silhueta
Plotly.newPlot('chart-comp3L-sil',[{{
  x:['Base K=4','L1 Hierárquica','L2 K=10','L3 Regional*'],
  y:[0.1585,0.0512,0.1215,0.2246],
  type:'bar',
  marker:{{color:['#94A3B8','#F7BA7E','#F28C28','#1B7F5C'],line:{{color:'#374151',width:1}}}},
  text:['0.158','0.051','0.121','0.225'],
  textposition:'outside',textfont:{{color:'#E5E7EB',size:13}},
  hovertemplate:'%{{x}}<br>Silhueta: %{{y:.4f}}<extra></extra>'
}}],{{...L,yaxis:{{...L.yaxis,title:'Silhueta (maior = melhor)',range:[0,0.27]}},height:320}},C);

// Davies-Bouldin
Plotly.newPlot('chart-comp3L-db',[{{
  x:['Base K=4','L1 Hierárquica','L2 K=10'],
  y:[1.6845,2.2876,1.587],
  type:'bar',
  marker:{{color:['#94A3B8','#F7BA7E','#1B7F5C'],line:{{color:'#374151',width:1}}}},
  text:['1.684','2.288','1.587'],
  textposition:'outside',textfont:{{color:'#E5E7EB',size:13}},
  hovertemplate:'%{{x}}<br>DB: %{{y:.4f}}<extra></extra>'
}}],{{...L,yaxis:{{...L.yaxis,title:'Davies-Bouldin (menor = melhor)',range:[0,2.7]}},height:320,
  annotations:[{{x:'L2 K=10',y:1.587,text:'★ Melhor',showarrow:true,arrowcolor:'#1B7F5C',font:{{color:'#1B7F5C',size:12}},ay:-40}}]
}},C);

// Scatter nClusters vs Silhueta
Plotly.newPlot('chart-comp3L-scatter',[{{
  x:[4,16,10,14],
  y:[0.1585,0.0512,0.1215,0.2246],
  mode:'markers+text',
  type:'scatter',
  text:['Base K=4','L1 Hierárquica','L2 K=10','L3 Regional'],
  textposition:['top right','top right','bottom right','top right'],
  textfont:{{color:'#E5E7EB',size:12}},
  marker:{{color:['#94A3B8','#F7BA7E','#F28C28','#1B7F5C'],size:18,line:{{color:'#E5E7EB',width:2}}}},
  hovertemplate:'%{{text}}<br>Clusters: %{{x}}<br>Silhueta: %{{y:.4f}}<extra></extra>'
}}],{{...L,
  xaxis:{{...L.xaxis,title:'Número de Clusters',range:[0,20]}},
  yaxis:{{...L.yaxis,title:'Silhueta',range:[0,0.27]}},
  height:380
}},C);

// Sidebar scroll
const secs=document.querySelectorAll('section');
const navs=document.querySelectorAll('.sidebar a');
window.addEventListener('scroll',()=>{{
  let cur='';
  secs.forEach(s=>{{if(window.scrollY>=s.offsetTop-120) cur=s.id;}});
  navs.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+cur));
}});
navs.forEach(a=>a.addEventListener('click',()=>document.querySelector('.sidebar').classList.remove('open')));
</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(OUT) / 1024
print(f"Relatório gerado: {OUT}")
print(f"Tamanho: {size_kb:.0f} KB")
print("OK — imagens embutidas como base64, gráficos Plotly inline.")
