# Portifolio de Projetos

Repositorio de projetos publicaveis do portfolio de Guilherme Correa, cobrindo
Power BI, dashboards HTML, analise exploratoria, Machine Learning e relatorios
interativos.

## Projetos

| Pasta | Projeto | Tipo | Entrega principal |
| --- | --- | --- | --- |
| `projeto_1/` | Dashboard Macroeconomico - Banco Central do Brasil | Power BI | Arquivo `.pbix` e documentacao. |
| `projeto_2/` | Superstore - EDA e dashboard interativo | Python, HTML e JavaScript | Relatorio em `report/index.html`. |
| `projeto_3/` | E-commerce 360 - Performance e negocios | Power BI | Documentacao, dados e materiais de apoio. |
| `projeto_4/` | Rossmann Sales Prediction | Machine Learning e series temporais | Relatorio HTML em `index.html`. |
| `projeto_5/` | ClusterBR - Segmentacao de municipios brasileiros | Machine Learning nao supervisionado | Relatorio HTML em `index.html`. |

## Estrutura Geral

Cada projeto tem README proprio e deve ser tratado como uma entrega
independente. As pastas podem conter:

- notebooks de exploracao/modelagem;
- dados brutos, processados ou amostras;
- dashboards HTML;
- imagens e graficos gerados;
- arquivos Power BI;
- scripts de apoio;
- documentacao complementar.

## Como Navegar

Leia primeiro o README da pasta do projeto desejado. Quando houver entrega HTML,
abra o `index.html` ou use um servidor local:

```powershell
python -m http.server 8000
```

## Manutencao

- Mantenha cada README de projeto atualizado com objetivo, dados, metodologia,
  tecnologias e forma de execucao.
- Se adicionar novo projeto, crie `projeto_6/` com README antes de publicar.
- Evite versionar ambientes virtuais. A pasta `projeto_4/.venv/` existe no
  workspace, mas nao deve ser usada como padrao para novos projetos.
- Preserve arquivos grandes que sejam parte explicita da entrega, como `.pbix` e
  HTMLs finais.

