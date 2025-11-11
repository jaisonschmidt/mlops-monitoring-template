# 📊 Grafana - Visualização de Métricas

## 🎯 Objetivo

Grafana para visualizar métricas do Prometheus e criar dashboards interativos para monitoramento do sistema MLOps.

## 🏗️ Arquitetura

```
┌─────────────┐    métricas    ┌────────────┐    consulta    ┌─────────────┐
│  API Churn  │──────────────>│ Prometheus │<──────────────│   Grafana   │
│  :8000      │    /metrics    │   :9090    │   PromQL      │   :3000     │
└─────────────┘                └────────────┘                └─────────────┘
```

## 📁 Estrutura de Arquivos

```
monitoring/grafana/
├── Dockerfile.grafana              # Container Grafana
├── grafana.ini                     # Configuração principal
├── README.md                       # Esta documentação
├── provisioning/                   # Auto-provisionamento
│   ├── datasources/
│   │   └── prometheus.yml         # Datasource Prometheus
│   └── dashboards/
│       ├── dashboards.yml         # Provider de dashboards
│       ├── api-health.json        # Dashboard 1: API Health
│       ├── ml-metrics.json        # Dashboard 2: ML Metrics
│       ├── business-churn.json    # Dashboard 3: Business
│       └── overview.json          # Dashboard 4: Overview
└── screenshots/                    # Capturas de tela
    └── README.md
```

## 🚀 Como Usar

### 1️⃣ Build da Imagem

```bash
cd monitoring/grafana
docker build -t grafana-mlops -f Dockerfile.grafana .
```

### 2️⃣ Executar Container

```bash
docker run -d \
  --name grafana \
  -p 3000:3000 \
  --network host \
  grafana-mlops
```

### 3️⃣ Acessar Interface

Abra o navegador em: **http://localhost:3000**

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `admin`

> ⚠️ **Atenção**: Na primeira vez, será solicitado para alterar a senha.

## 📊 Dashboards Disponíveis

### 1. API Health & Performance
- **UID**: `api-health`
- **Tags**: `api`, `performance`, `infrastructure`
- **Painéis**:
  - 🟢 Status da API (UP/DOWN)
  - 📈 Taxa de requisições por segundo
  - ⏱️ Latência P50, P95, P99
  - ❌ Taxa de erros (%)
  - 🔄 Requisições ativas
  - ⏰ Uptime da API
  - 📊 Requisições por método HTTP
  - 🌐 Requisições por endpoint
  - 📉 Histórico de latência
  - 🔴 Erros ao longo do tempo

### 2. ML Model Metrics
- **UID**: `ml-metrics`
- **Tags**: `ml`, `model`, `metrics`
- **Painéis**:
  - 🎯 F2-Score (gauge)
  - 📊 AUC-ROC (gauge)
  - ⏱️ Tempo de treinamento
  - 📝 Total de amostras treinadas
  - 📈 Evolução de métricas (F2, AUC)
  - 🔢 Total de predições
  - 📊 Taxa de predições/s
  - 🏷️ Versão do modelo
  - 📋 Tabela de métricas

### 3. Business Intelligence - Churn
- **UID**: `business-churn`
- **Tags**: `business`, `churn`, `kpi`
- **Painéis**:
  - 🚨 Clientes em alto risco
  - 🥧 Distribuição de risco (Pie Chart)
  - 📊 Score médio de churn
  - 📈 Evolução de predições (Stacked Area)
  - 📉 Tendência de alto risco
  - 📊 Percentual alto risco
  - 📊 Percentual baixo risco
  - 👥 Total de clientes
  - 📊 Taxa de queries

### 4. System Overview (Executivo)
- **UID**: `overview`
- **Tags**: `overview`, `executive`, `summary`
- **Painéis**:
  - 🟢 Status da API
  - 🎯 F2-Score
  - 📊 AUC
  - ❌ Taxa de erro
  - ⏰ Uptime 24h
  - 🚨 Clientes alto risco
  - 📊 Total de predições
  - 📈 Atividade geral (timeseries)
  - 🥧 Distribuição de risco
  - 📋 Tabela de KPIs principais

## 🔧 Configuração

### Datasource Prometheus

O datasource é provisionado automaticamente via arquivo `provisioning/datasources/prometheus.yml`:

```yaml
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://host.docker.internal:9090
    isDefault: true
```

### Dashboards Auto-Provisionamento

Os dashboards JSON são carregados automaticamente do diretório `/etc/grafana/provisioning/dashboards/` dentro do container.

## 📝 Queries PromQL Importantes

### API
```promql
# Status da API
up{job="api-churn"}

# Taxa de requisições
rate(http_requests_total[5m])

# Latência P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### ML Metrics
```promql
# F2-Score atual
model_f2_score

# Predições por segundo
rate(model_predictions_total[5m])
```

### Business
```promql
# Clientes em alto risco
churn_predictions_high_risk

# Distribuição por nível
churn_predictions_by_level{level="alto"}
```

## 🎨 Customização

### Adicionar Novo Dashboard

1. Crie o dashboard na interface do Grafana
2. Exporte como JSON: **Share → Export → Save to file**
3. Copie o arquivo para `provisioning/dashboards/`
4. Rebuild o container

### Modificar Dashboard Existente

1. Edite o arquivo JSON correspondente
2. Rebuild o container
3. Ou: Importe manualmente via **Dashboards → Import**

## 🔍 Troubleshooting

### Datasource não conecta ao Prometheus

**Problema**: Erro "Bad Gateway" ou timeout

**Solução**:
```bash
# Verifique se Prometheus está rodando
curl http://localhost:9090/-/healthy

# Use --network host no docker run
docker run -d --name grafana -p 3000:3000 --network host grafana-mlops
```

### Dashboards não aparecem

**Problema**: Dashboards não carregam automaticamente

**Solução**:
```bash
# Verifique os logs do container
docker logs grafana

# Verifique permissões dos arquivos JSON
ls -la provisioning/dashboards/

# Force reload: Restart do container
docker restart grafana
```

### Gráficos sem dados

**Problema**: Painéis mostram "No data"

**Solução**:
1. Verifique se a API está expondo `/metrics`
2. Verifique se Prometheus está coletando:
   - Acesse http://localhost:9090/targets
   - Status deve ser "UP"
3. Execute algumas predições para gerar métricas

## 📚 Recursos

- [Documentação Oficial Grafana](https://grafana.com/docs/)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)

## 🎓 Para Alunos

### Exercícios Práticos

1. **Criar um novo painel**: Adicione um painel mostrando a média móvel de 1h de predições
2. **Configurar alerta**: Crie um alerta quando F2-Score < 0.7
3. **Dashboard personalizado**: Crie um dashboard com métricas específicas do seu modelo
4. **Variáveis de template**: Adicione filtros por período de tempo

### Conceitos-Chave

- **Datasource**: Fonte de dados (Prometheus)
- **Panel**: Painel individual de visualização
- **Query**: Consulta PromQL para buscar dados
- **Dashboard**: Conjunto de painéis organizados
- **Provisioning**: Configuração automatizada via código
