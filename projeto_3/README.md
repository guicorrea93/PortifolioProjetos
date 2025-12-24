# E-commerce 360° — Do Dado Bruto à Estratégia de Negócio

## 📌 Visão Geral
Este projeto apresenta uma **análise estratégica completa de um e-commerce**, construída de ponta a ponta:  
**desde a extração dos dados via API**, passando por **tratamento, modelagem dimensional e criação de métricas em DAX**, até a entrega de um **dashboard executivo no Power BI Service**.

O objetivo é demonstrar domínio não apenas de visualização, mas de **todo o ciclo de dados**, com foco em **tomada de decisão baseada em dados reais**.

---

## 🎯 Objetivos do Projeto
- Construir um pipeline analítico completo (extração → modelagem → análise)
- Criar um dashboard executivo e analítico de e-commerce
- Explorar vendas, clientes, pagamentos, qualidade e operação
- Aplicar técnicas como **Pareto, sazonalidade, recorrência e segmentação**
- Transformar dados complexos em **insights acionáveis**

---

## 🛠️ Tecnologias Utilizadas
- **Power BI Desktop & Power BI Service**
- **Power Query (ETL)**
- **DAX (medidas avançadas)**
- **Modelagem Dimensional**
- **API REST (extração de dados)**
- **GitHub (documentação e portfólio)**

---

## 🔄 Pipeline de Dados (End-to-End)

### 1️⃣ Extração de Dados
Os dados foram **extraídos via API**, simulando um cenário real de integração com sistemas externos de e-commerce.  
Essa etapa incluiu:
- Consumo de endpoints REST
- Estruturação dos dados brutos
- Padronização de campos e tipos
- Preparação para ingestão analítica

> Essa abordagem reflete um ambiente corporativo real, onde os dados raramente chegam “prontos”.

---

### 2️⃣ Tratamento e Transformação (ETL)
Realizado no **Power Query**, incluindo:
- Limpeza de registros inválidos
- Criação de dimensões (datas, categorias, localização)
- Padronização de chaves
- Remoção de inconsistências (ex.: produtos sem categoria)
- Criação de tabelas fato e dimensões

---

### 3️⃣ Modelagem Dimensional
Modelo desenvolvido seguindo boas práticas:
- Fatos e dimensões bem definidas
- Relacionamentos consistentes
- Separação clara de responsabilidades
- Base preparada para análises avançadas e escaláveis

Principais tabelas:
- **Fato_Vendas**
- **Fato_Pagamentos**
- **Fato_Avaliacoes**
- **Dim_Produto**
- **Dim_Categoria**
- **Dim_Cliente**
- **Dim_Vendedor**
- **Dim_Geolocalizacao**
- **Dim_Calendario**
- **Dim_Pedido**

---

### 4️⃣ Métricas e Regras de Negócio (DAX)
Criação de medidas analíticas como:
- Faturamento total, entregue e não entregue
- Ticket médio
- Margem estimada
- Recorrência de clientes
- Pareto (Top 80%)
- Indicadores dinâmicos via seleção
- Análises MoM e YoY
- Métricas específicas por pagamento, categoria e vendedor

---

### 5️⃣ Visualização & Storytelling
Construção de um dashboard com:
- Layout limpo e profissional
- Paleta de cores consistente
- Hierarquia visual clara
- Navegação intuitiva
- Foco em leitura executiva e análise exploratória

---

## 📊 Estrutura do Dashboard

### 📄 Página 1 — Resumo Executivo
- KPIs principais de negócio
- Evolução do faturamento
- Distribuição geográfica
- Ranking de categorias

### 📄 Página 2 — Análise por Categoria (Pareto)
- Pareto de faturamento
- Justificativa analítica para foco nas categorias estratégicas

### 📄 Página 3 — Análise Detalhada de Categorias
- KPIs apenas das categorias que compõem 80% do faturamento
- Comparações e concentração

### 📄 Página 4 — Análise Temporal & Sazonalidade
- Evolução mensal
- MoM e YoY
- Picos e padrões sazonais

### 📄 Página 5 — Análise Geográfica & Logística
- Faturamento por estado
- Concentração regional
- Visão territorial das vendas

### 📄 Página 6 — Análise de Clientes
- Clientes únicos
- Recorrência
- Pedidos por cliente
- Faixas de faturamento

### 📄 Página 7 — Análise de Pagamentos
- À vista vs parcelado
- Impacto no ticket médio
- Distribuição por meios de pagamento

### 📄 Página 8 — Qualidade & Avaliações
- Nota média
- Avaliações por categoria
- Volume x qualidade
- Risco reputacional

### 📄 Página 9 — Operação & Vendedores
- Análise geográfica dos vendedores
- Concentração por estado/cidade
- Nota média por faixa de volume vendido

---

## 🔍 Principais Insights
- Forte concentração de faturamento em poucas categorias
- Parcelamento como alavanca de ticket médio
- Alta satisfação média, com pontos de atenção específicos
- Dependência operacional de polos geográficos de vendedores

---

## 🔗 Acesso ao Dashboard
👉 [**Visualizar Dashboard**](https://app.powerbi.com/view?r=eyJrIjoiN2JmMDFiOGItMzAxMS00NjI1LWE2ZGMtNmIzOTI0YzBlMjk4IiwidCI6IjhjYzJkZWQ2LWEzYjktNDk4My04ZDcxLTY3OGZjN2E2NjRiZSJ9)

---

### 🌐 Embed HTML
```html
<iframe title="Visão Estratégica de E-commerce"
        width="600"
        height="373.5"
        src="https://app.powerbi.com/view?r=eyJrIjoiN2JmMDFiOGItMzAxMS00NjI1LWE2ZGMtNmIzOTI0YzBlMjk4IiwidCI6IjhjYzJkZWQ2LWEzYjktNDk4My04ZDcxLTY3OGZjN2E2NjRiZSJ9"
        frameborder="0"
        allowFullScreen="true">
</iframe>
```
---

### 👤 Autor

Guilherme Quaglio Corrêa
Analista de BI | Power BI | SQL | Python

---

### 🏁 Considerações Finais

Este projeto foi desenvolvido com foco em cenários reais de negócio, cobrindo desde a origem dos dados (API) até a entrega executiva, reforçando habilidades de:
- Engenharia analítica
- BI corporativo
- Modelagem de dados
- Storytelling com dados
