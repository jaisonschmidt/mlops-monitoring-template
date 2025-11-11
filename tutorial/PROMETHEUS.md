# 📊 Tutorial: Prometheus - Monitoramento de Métricas

## 🎯 Objetivos de Aprendizagem

Ao final deste tutorial, você será capaz de:
- ✅ Entender o que é Prometheus e como funciona
- ✅ Executar Prometheus em container Docker
- ✅ Coletar métricas de uma aplicação Python/FastAPI
- ✅ Escrever queries PromQL para análise de dados
- ✅ Configurar alertas básicos

## 📚 O que é Prometheus?

**Prometheus** é um sistema de monitoramento e alerta open-source que:
- Coleta métricas de aplicações via HTTP (scraping)
- Armazena dados em séries temporais (time series)
- Permite consultas através da linguagem PromQL
- Suporta alertas baseados em regras

### Arquitetura

```
┌──────────────┐
│  Aplicação   │ Expõe /metrics
│  (FastAPI)   │ no formato Prometheus
└──────┬───────┘
       │
       │ HTTP GET a cada 15s
       ▼
┌──────────────┐
│  Prometheus  │ Coleta (scrape)
│   Server     │ e armazena métricas
└──────┬───────┘
       │
       │ PromQL
       ▼
┌──────────────┐
│   Grafana    │ Visualiza
│  Dashboards  │ métricas
└──────────────┘
```

## 🚀 Passo a Passo

### 1️⃣ Iniciando o Prometheus

```bash
# Método 1: Script automatizado (recomendado)
./scripts/start_monitoring.sh

# Método 2: Docker manual
cd monitoring/prometheus
docker build -t prometheus-mlops -f Dockerfile.prometheus .
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  --network host \
  prometheus-mlops
```

### 2️⃣ Acessando a Interface

Abra seu navegador em: **http://localhost:9090**

Você verá:
- 🔍 **Graph**: Consultar e visualizar métricas
- 🎯 **Targets**: Status dos endpoints monitorados
- 🚨 **Alerts**: Alertas configurados
- ⚙️ **Configuration**: Configuração do Prometheus

### 3️⃣ Verificando Targets

1. Clique em **Status → Targets**
2. Verifique se `api-churn` está **UP** (verde)
3. Se estiver **DOWN** (vermelho):
   - Verifique se a API está rodando: `curl http://localhost:8000/health`
   - Verifique logs: `docker logs prometheus`

### 4️⃣ Explorando Métricas

Clique em **Graph** e experimente estas queries:

#### Métricas de Infraestrutura

```promql
# API está UP? (1 = sim, 0 = não)
up{job="api-churn"}

# Requisições por segundo
rate(http_requests_total[5m])

# Latência média (P50)
histogram_quantile(0.5, rate(http_request_duration_seconds_bucket[5m]))

# Taxa de erros (%)
(sum(rate(http_requests_total{status=~"5.."}[5m])) / 
 sum(rate(http_requests_total[5m]))) * 100
```

#### Métricas de ML

```promql
# F2-Score do modelo
model_f2_score

# AUC-ROC
model_auc_score

# Total de predições
model_predictions_total

# Predições por minuto
rate(model_predictions_total[1m]) * 60
```

#### Métricas de Negócio

```promql
# Clientes em alto risco
churn_predictions_high_risk

# Score médio de churn
churn_score_average

# Distribuição por nível de risco
churn_predictions_by_level{level="alto"}
churn_predictions_by_level{level="medio"}
churn_predictions_by_level{level="baixo"}
```

### 5️⃣ Criando Gráficos

1. Digite uma query (ex: `rate(http_requests_total[5m])`)
2. Clique em **Execute**
3. Escolha entre:
   - **Table**: Tabela com valores
   - **Graph**: Gráfico de linha temporal

**Dica**: Use `[5m]` para janela de 5 minutos, `[1h]` para 1 hora, etc.

## 📊 PromQL - Guia Rápido

### Tipos de Métricas

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| **Counter** | Valor que só aumenta | `http_requests_total` |
| **Gauge** | Valor que sobe/desce | `model_f2_score` |
| **Histogram** | Distribuição de valores | `http_request_duration_seconds` |
| **Summary** | Similar ao Histogram | `request_size_bytes` |

### Funções Essenciais

```promql
# rate() - Taxa de crescimento por segundo
rate(http_requests_total[5m])

# increase() - Aumento total no período
increase(http_requests_total[1h])

# sum() - Soma valores
sum(http_requests_total) by (method)

# avg() - Média
avg(model_f2_score)

# max() / min() - Máximo / Mínimo
max(churn_score_average)

# histogram_quantile() - Percentil
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Filtros

```promql
# Por label exato
http_requests_total{method="POST"}

# Por regex
http_requests_total{status=~"2.."}  # 2xx

# Negação
http_requests_total{status!="200"}

# Múltiplos filtros
http_requests_total{method="POST",status="200"}
```

### Operações Matemáticas

```promql
# Taxa de erro (%)
(sum(rate(http_requests_total{status=~"5.."}[5m])) / 
 sum(rate(http_requests_total[5m]))) * 100

# Throughput total
sum(rate(http_requests_total[5m])) * 60  # req/min

# Diferença entre métricas
model_f2_score - 0.8  # Quanto acima de 0.8?
```

## 🚨 Configurando Alertas

Os alertas já estão configurados em `monitoring/prometheus/alert_rules.yml`:

### Ver Alertas Ativos

1. Acesse **Alerts** no Prometheus
2. Veja alertas **Pending** (aviso) e **Firing** (disparado)

### Exemplo de Regra de Alerta

```yaml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      - alert: APIDown
        expr: up{job="api-churn"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "API Churn está DOWN"
          description: "A API não respondeu por mais de 1 minuto"
```

### Alertas Disponíveis

| Alerta | Condição | Severidade |
|--------|----------|------------|
| `APIDown` | API offline > 1min | 🔴 Critical |
| `HighErrorRate` | Erros > 5% | 🟠 Warning |
| `HighLatency` | P95 > 500ms | 🟡 Warning |
| `ModelPerformanceDegraded` | F2-Score < 0.7 | 🟠 Warning |
| `HighChurnRisk` | Clientes alto risco > 1000 | 🟡 Info |

## 🧪 Exercícios Práticos

### Exercício 1: Monitorar Taxa de Sucesso

**Objetivo**: Criar query que mostra % de requisições bem-sucedidas

<details>
<summary>💡 Ver solução</summary>

```promql
(sum(rate(http_requests_total{status=~"2.."}[5m])) / 
 sum(rate(http_requests_total[5m]))) * 100
```
</details>

### Exercício 2: Predições por Hora

**Objetivo**: Calcular quantas predições são feitas por hora

<details>
<summary>💡 Ver solução</summary>

```promql
rate(model_predictions_total[5m]) * 3600
```
</details>

### Exercício 3: Tempo Médio de Resposta

**Objetivo**: Calcular latência média da API

<details>
<summary>💡 Ver solução</summary>

```promql
# Mediana (P50)
histogram_quantile(0.5, rate(http_request_duration_seconds_bucket[5m]))

# Média usando sum/count
sum(rate(http_request_duration_seconds_sum[5m])) / 
sum(rate(http_request_duration_seconds_count[5m]))
```
</details>

### Exercício 4: Criar Novo Alerta

**Objetivo**: Criar alerta quando predições/minuto < 1

<details>
<summary>💡 Ver solução</summary>

Adicione em `alert_rules.yml`:

```yaml
- alert: LowPredictionRate
  expr: rate(model_predictions_total[5m]) * 60 < 1
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Taxa de predições baixa"
    description: "Menos de 1 predição por minuto nos últimos 5 minutos"
```

Recarregue configuração:
```bash
curl -X POST http://localhost:9090/-/reload
```
</details>

## 🔧 Troubleshooting

### Problema: Target "api-churn" está DOWN

**Soluções**:
```bash
# 1. Verificar se API está rodando
curl http://localhost:8000/health

# 2. Verificar se /metrics está acessível
curl http://localhost:8000/metrics

# 3. Ver logs do Prometheus
docker logs prometheus

# 4. Reiniciar Prometheus
docker restart prometheus
```

### Problema: Métricas não aparecem

**Possíveis causas**:
1. API ainda não foi acessada (gerar tráfego com `test_api_load.py`)
2. Aguardar intervalo de scraping (15s)
3. Métrica não foi registrada no código

**Solução**:
```bash
# Gerar tráfego
python scripts/test_api_load.py

# Aguardar 30 segundos
sleep 30

# Verificar novamente
```

### Problema: Alertas não disparam

**Checklist**:
- ✅ Arquivo `alert_rules.yml` está correto?
- ✅ Prometheus carregou as regras? (ver **Alerts**)
- ✅ Condição do alerta está satisfeita?
- ✅ Aguardou o tempo de `for:`?

## 📚 Recursos Adicionais

### Documentação Oficial
- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Best Practices](https://prometheus.io/docs/practices/naming/)

### Tutoriais
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [Prometheus Up & Running (Livro)](https://www.oreilly.com/library/view/prometheus-up/9781492034131/)

### Ferramentas
- [PromLens](https://promlens.com/) - Editor visual de PromQL
- [Prometheus Playground](https://demo.promlabs.com/) - Ambiente de teste

## 🎯 Próximos Passos

1. ✅ Explore diferentes queries PromQL
2. ✅ Configure alertas personalizados
3. ✅ Prossiga para o tutorial do Grafana: `tutorial/GRAFANA.md`
4. ✅ Integre com Alertmanager para notificações (avançado)

---

**Dúvidas?** Consulte `monitoring/queries_exemplos.md` para mais queries prontas!
