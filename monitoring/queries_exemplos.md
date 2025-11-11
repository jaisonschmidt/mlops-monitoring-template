# Queries PromQL - Exemplos Úteis

Este documento contém queries PromQL organizadas por categoria para análise das métricas do sistema MLOps.

## 📊 Métricas de Performance da API

### Taxa de Requisições

```promql
# Taxa de requisições por segundo (últimos 5 minutos)
rate(http_requests_total[5m])

# Taxa de requisições por endpoint
sum(rate(http_requests_total[5m])) by (handler)

# Total de requisições nas últimas 24h
increase(http_requests_total[24h])
```

### Latência

```promql
# Latência média
avg(rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m]))

# Percentil 50 (mediana)
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))

# Percentil 95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Percentil 99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Latência máxima
max(http_request_duration_seconds)
```

### Erros

```promql
# Taxa de erro total
rate(http_requests_total{status=~"5.."}[5m])

# Taxa de erro percentual
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100

# Erros por status code
sum(rate(http_requests_total{status=~"5.."}[5m])) by (status)

# Erros 404 (não encontrado)
rate(http_requests_total{status="404"}[5m])
```

### Requisições Ativas

```promql
# Requisições em andamento agora
http_requests_inprogress

# Requisições ativas (nossa métrica customizada)
api_active_requests

# Máximo de requisições simultâneas (última hora)
max_over_time(api_active_requests[1h])
```

---

## 🤖 Métricas de Machine Learning

### Qualidade do Modelo

```promql
# F2-Score atual
model_f2_score

# AUC-ROC atual
model_auc_score

# Precisão
model_precision

# Recall
model_recall

# Evolução do F2-Score (comparar com 1 dia atrás)
model_f2_score - model_f2_score offset 1d

# Evolução do AUC (comparar com 1 hora atrás)
model_auc_score - model_auc_score offset 1h
```

### Treinamento

```promql
# Duração do último treinamento (em minutos)
model_training_duration_seconds / 60

# Número de amostras de treino
model_training_samples

# Taxa de crescimento do dataset (comparar com versão anterior)
(model_training_samples - model_training_samples offset 7d) / model_training_samples offset 7d * 100
```

### Predições

```promql
# Total de predições servidas
model_predictions_total

# Taxa de predições por minuto
rate(model_predictions_total[1m]) * 60

# Taxa de predições por hora
rate(model_predictions_total[1h]) * 3600

# Predições por endpoint
sum(model_predictions_total) by (endpoint)

# Predições carregadas em memória
api_predictions_loaded
```

---

## 💼 Métricas de Negócio (Churn)

### Distribuição de Risco

```promql
# Clientes em alto risco (>0.7)
churn_predictions_high_risk

# Clientes por nível de risco
churn_predictions_by_level

# Total de clientes
sum(churn_predictions_by_level)

# Percentual de clientes em alto risco
(churn_predictions_by_level{level="alto"} / sum(churn_predictions_by_level)) * 100

# Percentual de clientes em baixo risco
(churn_predictions_by_level{level="baixo"} / sum(churn_predictions_by_level)) * 100
```

### Score de Churn

```promql
# Score médio de churn
churn_prediction_score_avg

# Variação do score médio (última hora)
churn_prediction_score_avg - churn_prediction_score_avg offset 1h

# Variação percentual do score médio
((churn_prediction_score_avg - churn_prediction_score_avg offset 1h) / churn_prediction_score_avg offset 1h) * 100

# Score médio está acima de threshold (0.6)?
churn_prediction_score_avg > 0.6
```

### Distribuição de Scores

```promql
# Histograma de distribuição de scores
churn_prediction_score_distribution_bucket

# Percentil 90 dos scores
histogram_quantile(0.90, churn_prediction_score_distribution_bucket)
```

---

## 🔍 Queries Avançadas

### Correlação entre Métricas

```promql
# Correlação entre taxa de predições e latência
rate(model_predictions_total[5m]) and histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Verificar se alto volume causa alta latência
(rate(http_requests_total[5m]) > 10) and (histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1)
```

### Detecção de Anomalias

```promql
# Spike no score médio (aumento > 20%)
((churn_prediction_score_avg - churn_prediction_score_avg offset 1h) / churn_prediction_score_avg offset 1h) > 0.2

# Queda abrupta no F2-Score
(model_f2_score offset 1h - model_f2_score) > 0.1

# Aumento repentino de clientes em alto risco
churn_predictions_high_risk > (avg_over_time(churn_predictions_high_risk[24h]) * 1.5)
```

### Agregações Temporais

```promql
# Média de F2-Score nas últimas 24h
avg_over_time(model_f2_score[24h])

# Máximo de clientes em alto risco (última semana)
max_over_time(churn_predictions_high_risk[7d])

# Mínimo do AUC (últimas 48h)
min_over_time(model_auc_score[48h])

# Taxa média de requisições (última hora)
avg_over_time(rate(http_requests_total[5m])[1h:])
```

### Health Check e Disponibilidade

```promql
# API está up?
up{job="api-churn"}

# Uptime (% de tempo que API estava up nas últimas 24h)
avg_over_time(up{job="api-churn"}[24h]) * 100

# Quantos dados estão carregados?
api_predictions_loaded > 0
```

---

## 📈 Queries para Dashboards

### Dashboard de Overview

```promql
# Painel 1: Status da API
up{job="api-churn"}

# Painel 2: Taxa de requisições
sum(rate(http_requests_total[5m]))

# Painel 3: Taxa de erro
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100

# Painel 4: F2-Score
model_f2_score

# Painel 5: Clientes em alto risco
churn_predictions_high_risk
```

### Dashboard de Performance

```promql
# Latência P50, P95, P99
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Requests por segundo
rate(http_requests_total[1m])

# Requisições ativas
api_active_requests

# Taxa de sucesso
(sum(rate(http_requests_total{status=~"2.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100
```

### Dashboard de ML

```promql
# Métricas do modelo
model_f2_score
model_auc_score
model_precision
model_recall

# Evolução temporal
model_f2_score[1h]
model_auc_score[1h]

# Tempo de treinamento (em minutos)
model_training_duration_seconds / 60

# Amostras de treino
model_training_samples
```

### Dashboard de Negócio

```promql
# Distribuição por nível
churn_predictions_by_level{level="baixo"}
churn_predictions_by_level{level="medio"}
churn_predictions_by_level{level="alto"}

# Score médio
churn_prediction_score_avg

# Total de clientes
sum(churn_predictions_by_level)

# % Alto risco
(churn_predictions_by_level{level="alto"} / sum(churn_predictions_by_level)) * 100
```

---

## 🎯 Queries para Alertas

### Alertas Críticos

```promql
# API Down
up{job="api-churn"} == 0

# Taxa de erro > 10%
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) > 0.10

# F2-Score < 0.6
model_f2_score < 0.6
```

### Alertas de Warning

```promql
# Latência P95 > 2s
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2

# Score médio aumentou > 10%
((churn_prediction_score_avg - churn_prediction_score_avg offset 1h) / churn_prediction_score_avg offset 1h) > 0.10

# Mais de 1000 clientes em alto risco
churn_predictions_high_risk > 1000
```

---

## 💡 Dicas de Uso

### Intervalos de Tempo

- `[5m]` - últimos 5 minutos
- `[1h]` - última hora
- `[24h]` - últimas 24 horas
- `[7d]` - últimos 7 dias

### Funções Úteis

- `rate()` - Taxa de crescimento por segundo
- `increase()` - Incremento total no período
- `avg_over_time()` - Média no período
- `max_over_time()` - Máximo no período
- `min_over_time()` - Mínimo no período
- `histogram_quantile()` - Percentil de um histograma
- `sum()` - Soma de valores
- `avg()` - Média de valores
- `max()` - Máximo de valores
- `min()` - Mínimo de valores

### Operadores

- `+` - Adição
- `-` - Subtração
- `*` - Multiplicação
- `/` - Divisão
- `==` - Igual
- `!=` - Diferente
- `>` - Maior que
- `<` - Menor que
- `>=` - Maior ou igual
- `<=` - Menor ou igual

### Filtros (Labels)

```promql
# Filtrar por job
metric_name{job="api-churn"}

# Filtrar por múltiplos valores
metric_name{status=~"2..|3.."}

# Filtrar excluindo valores
metric_name{handler!="/metrics"}

# Combinar filtros
metric_name{job="api-churn",status="200"}
```

---

## 📚 Recursos Adicionais

- **PromQL Tutorial**: https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Functions Reference**: https://prometheus.io/docs/prometheus/latest/querying/functions/
- **Query Examples**: https://prometheus.io/docs/prometheus/latest/querying/examples/
