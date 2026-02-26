# Data Science: Regressão Linear - Transformação de Variáveis

Estudo de regressão linear múltipla com transformação logarítmica para precificação de imóveis e hospedagens, desenvolvido no curso da [Alura](https://www.alura.com.br/).

**[Ver página do estudo](https://guicorrea93.github.io/PortifolioProjetos/projeto_alura_01/)**

---

## Objetivo

Construir modelos de Machine Learning capazes de estimar preços de imóveis e hospedagens a partir de suas características, aplicando técnicas de transformação de variáveis para melhorar a qualidade do ajuste.

## Estudos Realizados

### 1. Precificação de Imóveis

Modelo para estimar o valor de venda de casas com base em área, presença de segundo andar e proximidade ao metrô.

- **Dataset:** 1.460 registros, 6 variáveis (adaptado do [Kaggle House Prices](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques))
- **R² Treino:** 0.759 | **R² Teste:** 0.738
- **Features finais:** `area_primeiro_andar`, `existe_segundo_andar`, `area_quintal`, `dist_metro`
- **Variável removida:** `dist_parque` (p-valor = 0.251, não significante)

### 2. Desafio: Precificação de Hospedagens

Aplicação das mesmas técnicas para precificar hospedagens de temporada.

- **Dataset:** 5.000 registros, 5 variáveis
- **R² Treino:** 0.811 | **R² Teste:** 0.808
- **Features finais:** `area`, `dist_praia`, `piscina`
- **Variável removida:** `dist_mercado` (p-valor = 0.725, não significante)

## Técnicas Utilizadas

| Técnica | Descrição |
|---------|-----------|
| Análise de Correlação | Correlação de Pearson para identificar variáveis mais influentes |
| Análise Exploratória | Boxplots, histogramas, pairplots e estatísticas descritivas |
| Transformação Logarítmica | `np.log` e `np.log1p` para normalizar distribuições assimétricas |
| Modelo Log-Log | Regressão com variáveis em escala log (coeficientes = elasticidades) |
| Train/Test Split | Divisão 70/30 com `random_state=1991` |
| OLS (Statsmodels) | Avaliação de p-valores, IC 95%, F-statistic e AIC |
| Análise de Resíduos | Homocedasticidade, normalidade e gráfico Previsão vs Real |

## Pipeline

```
Coleta → Exploração → Visualização → Transformação Log → Modelagem → Avaliação
```

## Estrutura do Projeto

```
projeto_alura_01/
├── Estudo - Regressão Linear.ipynb          # Notebook principal (imóveis)
├── Estudo - Regressão Linear - Desafio.ipynb # Notebook do desafio (hospedagens)
├── casas_a_precificar.csv                    # 10 imóveis para precificação
├── index.html                                # Página interativa do estudo
└── README.md
```

## Principais Resultados

**Modelo de Imóveis (Log-Log):**

```
ln(Valor) = 11.198 + 0.498·ln(Área1ºAndar) + 0.187·Dummy2ºAndar + 0.079·ln(ÁreaQuintal) - 0.261·ln(DistMetrô)
```

- +1% na área do 1º andar → +0.50% no valor
- Ter 2º andar → +20.6% no valor
- +1% na distância ao metrô → -0.26% no valor

**Modelo de Hospedagens (Log-Log):**

```
ln(Valor) = 2.574 + 1.003·ln(Área) - 0.465·ln(1+DistPraia) + 0.163·Piscina
```

- +1% na área → +1.0% no valor (elasticidade unitária)
- +1% na distância à praia → -0.47% no valor
- Ter piscina → +17.74% no valor

## Tecnologias

- **Python 3** | **Pandas** | **NumPy**
- **Scikit-learn** (LinearRegression, train_test_split, metrics)
- **Statsmodels** (OLS, summary)
- **Seaborn** / **Matplotlib** (regplot, pairplot, boxplot, histplot)
- **Jupyter Notebook**

## Como Executar

1. Abra os notebooks no [Google Colab](https://colab.research.google.com/) ou Jupyter local
2. Os datasets são carregados diretamente do GitHub (não precisa baixar)
3. Execute as células sequencialmente

## Aprendizados

- Distribuições assimétricas à direita devem ser transformadas com log antes de aplicar regressão linear
- Variáveis com p-valor > 0.05 devem ser removidas para simplificar o modelo sem perder performance
- No modelo log-log, coeficientes representam elasticidades (interpretação direta em %)
- Variáveis dummy (binárias) têm impacto calculado por `100 × (e^β - 1)`
- Análise de resíduos (homocedasticidade + normalidade) valida as premissas do modelo
