# 📋 Planejamento de Implementação: Monitoramento MLOps

**Projeto:** mlops-monitoring-prep  
**Data:** Novembro 2025  
**Objetivo:** Adicionar recursos de monitoramento (Loguru, Prometheus, Grafana) ao projeto acadêmico de MLOps

---

## 📑 ÍNDICE - PASSOS DE EXECUÇÃO

### **PASSO 1: Preparação do Ambiente** ⚙️
- [1.1 Atualizar Dependências](#passo-1-preparação-do-ambiente)
- [1.2 Criar Estrutura de Diretórios](#12-criar-estrutura-de-diretórios)
- [1.3 Arquivos de Configuração](#13-arquivos-de-configuração)

### **PASSO 2: Implementação do Loguru** 📝
- [2.1 Criar Módulo de Logging](#passo-2-implementação-do-loguru)
- [2.2 Integrar nos Scripts Existentes](#22-integrar-nos-scripts-existentes)
- [2.3 Definir Padrões de Logging](#23-definir-padrões-de-logging)

### **PASSO 3: Implementação do Prometheus** 📊
- [3.1 Criar Módulo de Métricas](#passo-3-implementação-do-prometheus)
- [3.2 Instrumentar API FastAPI](#32-instrumentar-api-fastapi)
- [3.3 Métricas Customizadas](#33-métricas-customizadas)
- [3.4 Container do Prometheus](#34-container-do-prometheus)

### **PASSO 4: Implementação do Grafana** 📈
- [4.1 Criar Container do Grafana](#passo-4-implementação-do-grafana)
- [4.2 Configurar Datasource Prometheus](#42-configurar-datasource-prometheus)
- [4.3 Criar Dashboards](#43-criar-dashboards)
- [4.4 Configurar Alertas](#44-configurar-alertas)

### **PASSO 5: Métricas de Machine Learning** 🤖
- [5.1 Instrumentar Treinamento](#passo-5-métricas-de-machine-learning)
- [5.2 Instrumentar Predição](#52-instrumentar-predição)
- [5.3 Métricas de Negócio](#53-métricas-de-negócio)

### **PASSO 6: Integração e Testes** ✅
- [6.1 Scripts de Inicialização](#passo-6-integração-e-testes)
- [6.2 Testes de Carga](#62-testes-de-carga)
- [6.3 Documentação](#63-documentação)
- [6.4 Exemplos Práticos](#64-exemplos-práticos)

---

## 🎯 VISÃO GERAL

### Stack de Monitoramento

| Ferramenta | Função | Porta | Container |
|------------|--------|-------|-----------|
| **Loguru** | Logging estruturado | N/A | Biblioteca Python |
| **Prometheus** | Coleta de métricas | 9090 | prometheus-server |
| **Grafana** | Visualização | 3000 | grafana-server |
| **API FastAPI** | Aplicação | 8000 | api-churn |

### Componentes do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    APLICAÇÕES PYTHON                         │
│  [Treinamento] [Predição] [Retreinamento] [API FastAPI]    │
│         ↓            ↓            ↓            ↓             │
│    [Loguru] + [Prometheus Client] + [Custom Metrics]       │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
  [Logs/*.log]    [/metrics endpoint]  [Métricas Custom]
        │                 │                 │
        │                 │                 │
        │                 ▼                 │
        │         [Prometheus Server]       │
        │                 │                 │
        │                 ▼                 │
        │           [Grafana Server]        │
        │                 │                 │
        │                 ▼                 │
        │         [Dashboards Visuais]      │
        │                                   │
        └───────────────────────────────────┘
                Observabilidade Completa
```

---

## 📊 MÉTRICAS DEFINIDAS

### Métricas de Infraestrutura da API

| Métrica | Tipo | Descrição | Dashboard |
|---------|------|-----------|-----------|
| `api_requests_total` | Counter | Total de requisições HTTP | API Health |
| `api_request_duration_seconds` | Histogram | Tempo de resposta | API Health |
| `api_errors_total` | Counter | Total de erros por código | API Health |
| `api_active_requests` | Gauge | Requisições em andamento | API Health |
| `api_predictions_loaded` | Gauge | Predições em memória | API Health |

### Métricas de Negócio (ML)

| Métrica | Tipo | Descrição | Dashboard |
|---------|------|-----------|-----------|
| `churn_predictions_high_risk` | Gauge | Clientes alto risco | Business |
| `churn_predictions_by_level` | Gauge | Por nível (baixo/médio/alto) | Business |
| `churn_prediction_score_avg` | Gauge | Score médio de churn | Business |
| `model_predictions_total` | Counter | Total de predições servidas | ML Metrics |
| `model_cache_hits` | Counter | Consultas em cache | ML Metrics |

### Métricas de Treinamento

| Métrica | Tipo | Descrição | Dashboard |
|---------|------|-----------|-----------|
| `model_training_duration_seconds` | Gauge | Tempo de treinamento | ML Metrics |
| `model_f2_score` | Gauge | F2-Score do modelo | ML Metrics |
| `model_auc_score` | Gauge | AUC-ROC | ML Metrics |
| `model_training_samples` | Gauge | Amostras de treino | ML Metrics |
| `model_version` | Info | Versão/timestamp | ML Metrics |

---

## PASSO 1: Preparação do Ambiente

### 1.1 Atualizar Dependências

**Arquivo:** `requirements.txt`

**Adicionar:**
```txt
# Logging
loguru>=0.7.0

# Métricas e Monitoramento
prometheus-client>=0.19.0
prometheus-fastapi-instrumentator>=6.1.0
```

**Instalar:**
```bash
pip install -r requirements.txt
```

---

### 1.2 Criar Estrutura de Diretórios

**Comandos:**
```bash
# Diretório de logs
mkdir -p logs

# Estrutura de monitoramento
mkdir -p monitoring/prometheus
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/provisioning/dashboards
mkdir -p monitoring/grafana/screenshots

# Utilitários
mkdir -p src/utils

# Scripts auxiliares
mkdir -p scripts

# Configurações
mkdir -p config
```

**Estrutura Final:**
```
mlops-monitoring-prep/
├── logs/                              # ⭐ NOVO
│   └── .gitkeep
├── monitoring/                        # ⭐ NOVO
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   ├── Dockerfile.prometheus
│   │   └── alert_rules.yml
│   ├── grafana/
│   │   ├── Dockerfile.grafana
│   │   ├── grafana.ini
│   │   └── provisioning/
│   │       ├── datasources/
│   │       │   └── prometheus.yml
│   │       └── dashboards/
│   │           ├── dashboards.yml
│   │           ├── api-health.json
│   │           ├── ml-metrics.json
│   │           ├── business-churn.json
│   │           └── overview.json
│   └── queries_exemplos.md
├── src/
│   └── utils/                         # ⭐ NOVO
│       ├── __init__.py
│       ├── logger.py
│       └── metrics.py
├── config/                            # ⭐ NOVO
│   └── monitoring_config.py
└── scripts/                           # ⭐ NOVO
    ├── start_monitoring.sh
    ├── test_api_load.py
    └── export_metrics.py
```

---

### 1.3 Arquivos de Configuração

**1.3.1 Criar `.gitkeep` para logs**
```bash
touch logs/.gitkeep
```

**1.3.2 Atualizar `.gitignore`**
```gitignore
# Logs
logs/*.log
logs/*.json

# Dados do Prometheus
monitoring/prometheus/data/

# Dados do Grafana
monitoring/grafana/data/

# Python
__pycache__/
*.pyc
.env
```

---

## PASSO 2: Implementação do Loguru

### 2.1 Criar Módulo de Logging

**Arquivo:** `src/utils/logger.py`

**Funcionalidades:**
- Configuração centralizada do Loguru
- Rotação automática de arquivos (10 MB)
- Retenção de 7 dias
- Formatação customizada
- Logs estruturados (JSON opcional)
- Níveis por componente

**Configurações:**
```python
# Exemplo de configuração
logger.add(
    "logs/{time:YYYY-MM-DD}_api.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    serialize=False  # True para JSON
)
```

**Níveis de Log:**
- `TRACE`: Debug detalhado
- `DEBUG`: Informações de desenvolvimento
- `INFO`: Eventos normais
- `SUCCESS`: Operações bem-sucedidas
- `WARNING`: Alertas
- `ERROR`: Erros tratáveis
- `CRITICAL`: Erros críticos

---

### 2.2 Integrar nos Scripts Existentes

**Scripts a modificar:**
1. `src/treinamento.py`
2. `src/predicao.py`
3. `src/retreinamento.py`
4. `src/api_churn.py`

**Padrão de integração:**
```python
from utils.logger import logger

# Substituir print() por:
logger.info("Mensagem informativa")
logger.success("Operação concluída")
logger.warning("Alerta")
logger.error("Erro")
```

**Contexto adicional:**
```python
logger.info("Predição realizada", extra={
    "id_cliente": cliente_id,
    "risco": risco_score,
    "nivel": nivel_risco
})
```

---

### 2.3 Definir Padrões de Logging

**Por Componente:**

| Componente | Arquivo de Log | Eventos Principais |
|------------|----------------|-------------------|
| API | `api.log` | Requests, erros, latência |
| Treinamento | `training.log` | Etapas, métricas, duração |
| Predição | `prediction.log` | Carregamento, predições |
| Retreinamento | `retraining.log` | Combinação de dados |

**Estrutura de Log (JSON):**
```json
{
  "timestamp": "2025-11-11T10:30:45.123Z",
  "level": "INFO",
  "module": "api_churn",
  "function": "obter_churn_cliente",
  "line": 85,
  "message": "Consulta de risco realizada",
  "extra": {
    "id_cliente": 12345,
    "risco": 0.75,
    "request_id": "abc-123-def"
  }
}
```

---

## PASSO 3: Implementação do Prometheus

### 3.1 Criar Módulo de Métricas

**Arquivo:** `src/utils/metrics.py`

**Conteúdo:**
- Definição de todas as métricas
- Funções helpers
- Decorators para timing
- Inicialização das métricas

**Tipos de Métricas:**
- **Counter**: Valores que só aumentam (ex: total de requests)
- **Gauge**: Valores que sobem/descem (ex: requests ativas)
- **Histogram**: Distribuição de valores (ex: latência)
- **Summary**: Estatísticas (ex: percentis)
- **Info**: Metadata (ex: versão do modelo)

---

### 3.2 Instrumentar API FastAPI

**Arquivo:** `src/api_churn.py`

**Adicionar:**
```python
from prometheus_fastapi_instrumentator import Instrumentator

# Após criar app
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)
```

**Métricas Automáticas:**
- `http_requests_total`
- `http_request_duration_seconds`
- `http_requests_in_progress`

**Endpoint de Métricas:**
- URL: `http://localhost:8000/metrics`
- Formato: Prometheus text format

---

### 3.3 Métricas Customizadas

**Adicionar ao código:**

```python
from utils.metrics import (
    churn_predictions_high_risk,
    churn_predictions_by_level,
    model_predictions_total
)

# Exemplo de uso
@app.get("/churn/{id_cliente}")
async def obter_churn_cliente(id_cliente: int):
    # ... código existente ...
    
    # Incrementar métricas
    model_predictions_total.inc()
    
    if risco > 0.7:
        churn_predictions_high_risk.inc()
    
    churn_predictions_by_level.labels(level=nivel_risco).set(valor)
    
    return resultado
```

---

### 3.4 Container do Prometheus

**Arquivo:** `monitoring/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: 'mlops-churn-monitor'

scrape_configs:
  - job_name: 'api-churn'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s
```

**Arquivo:** `monitoring/prometheus/Dockerfile.prometheus`

```dockerfile
FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY alert_rules.yml /etc/prometheus/alert_rules.yml

EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.console.libraries=/usr/share/prometheus/console_libraries", \
     "--web.console.templates=/usr/share/prometheus/consoles"]
```

**Build e Run:**
```bash
# Build
docker build -f monitoring/prometheus/Dockerfile.prometheus \
  -t prometheus-mlops:latest \
  monitoring/prometheus/

# Run
docker run -d \
  --name prometheus-mlops \
  -p 9090:9090 \
  -v prometheus_data:/prometheus \
  prometheus-mlops:latest
```

**Acessar:** `http://localhost:9090`

---

## PASSO 4: Implementação do Grafana

### 4.1 Criar Container do Grafana

**Arquivo:** `monitoring/grafana/Dockerfile.grafana`

```dockerfile
FROM grafana/grafana:10.2.0

# Copiar configurações
COPY grafana.ini /etc/grafana/grafana.ini

# Copiar provisioning
COPY provisioning/ /etc/grafana/provisioning/

# Configurar permissões
USER root
RUN mkdir -p /var/lib/grafana && \
    chown -R grafana:grafana /var/lib/grafana

USER grafana

EXPOSE 3000
```

**Arquivo:** `monitoring/grafana/grafana.ini`

```ini
[server]
http_port = 3000

[security]
admin_user = admin
admin_password = admin

[users]
allow_sign_up = false

[analytics]
reporting_enabled = false
check_for_updates = false

[log]
mode = console
level = info
```

**Build e Run:**
```bash
# Build
docker build -f monitoring/grafana/Dockerfile.grafana \
  -t grafana-mlops:latest \
  monitoring/grafana/

# Run
docker run -d \
  --name grafana-mlops \
  -p 3000:3000 \
  -v grafana_data:/var/lib/grafana \
  grafana-mlops:latest
```

**Acessar:** `http://localhost:3000`  
**Login:** admin / admin

---

### 4.2 Configurar Datasource Prometheus

**Arquivo:** `monitoring/grafana/provisioning/datasources/prometheus.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://host.docker.internal:9090
    isDefault: true
    editable: false
    jsonData:
      timeInterval: 15s
      queryTimeout: 60s
```

**Provisioning Automático:**
- Datasource criado automaticamente ao iniciar Grafana
- Não precisa configuração manual

---

### 4.3 Criar Dashboards

**Arquivo:** `monitoring/grafana/provisioning/dashboards/dashboards.yml`

```yaml
apiVersion: 1

providers:
  - name: 'MLOps Dashboards'
    orgId: 1
    folder: 'MLOps Monitoring'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

#### **4.3.1 Dashboard: API Health & Performance**

**Arquivo:** `monitoring/grafana/provisioning/dashboards/api-health.json`

**Painéis:**
1. **Status da API** (Stat)
   - Query: `up{job="api-churn"}`
   - Cores: Verde (1) / Vermelho (0)

2. **Requisições/segundo** (Graph)
   - Query: `rate(api_requests_total[5m])`

3. **Latência P95** (Gauge)
   - Query: `histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))`
   - Threshold: Verde (<1s), Amarelo (1-2s), Vermelho (>2s)

4. **Taxa de Erro** (Stat + Graph)
   - Query: `(sum(rate(api_errors_total[5m])) / sum(rate(api_requests_total[5m]))) * 100`

5. **Requisições Ativas** (Gauge)
   - Query: `api_active_requests`

6. **Erros por Código HTTP** (Pie Chart)
   - Query: `sum(api_errors_total) by (status_code)`

#### **4.3.2 Dashboard: ML Model Metrics**

**Arquivo:** `monitoring/grafana/provisioning/dashboards/ml-metrics.json`

**Painéis:**
1. **F2-Score** (Gauge)
   - Query: `model_f2_score`
   - Zonas: Vermelho (<0.6), Amarelo (0.6-0.7), Verde (>0.8)

2. **AUC-ROC** (Gauge)
   - Query: `model_auc_score`

3. **Tempo de Treinamento** (Bar Chart)
   - Query: `model_training_duration_seconds`

4. **Predições Totais** (Stat)
   - Query: `model_predictions_total`

5. **Taxa de Predições/min** (Graph)
   - Query: `rate(model_predictions_total[1m])`

6. **Histórico de Versões** (Table)
   - Queries: `model_f2_score`, `model_auc_score`, `model_version`

#### **4.3.3 Dashboard: Business Intelligence - Churn**

**Arquivo:** `monitoring/grafana/provisioning/dashboards/business-churn.json`

**Painéis:**
1. **Clientes Alto Risco** (Stat - Alerta)
   - Query: `churn_predictions_high_risk`
   - Cor: Vermelho se > 1000

2. **Distribuição de Risco** (Pie Chart)
   - Queries:
     - `churn_predictions_by_level{level="baixo"}`
     - `churn_predictions_by_level{level="medio"}`
     - `churn_predictions_by_level{level="alto"}`

3. **Score Médio de Churn** (Gauge)
   - Query: `churn_prediction_score_avg`

4. **Evolução por Nível** (Stacked Area)
   - Query: `churn_predictions_by_level`

5. **Taxa de Consultas** (Graph)
   - Query: `rate(api_requests_total{endpoint="/churn"}[5m])`

#### **4.3.4 Dashboard: System Overview**

**Arquivo:** `monitoring/grafana/provisioning/dashboards/overview.json`

**Painéis:**
1. **Resumo de Status** (Stat Grid)
   - API Status, F2-Score, Taxa Erro, Uptime

2. **Atividade Geral** (Graph)
   - Requests, Predições, Erros

3. **Métricas Principais** (Table)
   - Todas as métricas importantes

---

### 4.4 Configurar Alertas

**Alertas no Grafana:**

| Nome | Condição | Severidade | Notificação |
|------|----------|------------|-------------|
| API Down | `up{job="api"} == 0` por 1min | Critical | Email/Slack |
| Alta Latência | P95 > 2s por 5min | Warning | Email |
| Taxa de Erro Alta | Erro > 5% por 5min | Warning | Email |
| F2-Score Baixo | F2 < 0.7 | Warning | Email |
| Sem Predições | Nenhuma em 1h | Warning | Email |
| Spike de Churn | Alto risco aumentou 20% | Critical | Email/Slack |

**Configuração de Notification Channel (exemplo):**
```json
{
  "name": "Email MLOps Team",
  "type": "email",
  "isDefault": true,
  "settings": {
    "addresses": "mlops-team@example.com"
  }
}
```

---

## PASSO 5: Métricas de Machine Learning

### 5.1 Instrumentar Treinamento

**Arquivo:** `src/treinamento.py`

**Adicionar:**
```python
from utils.logger import logger
from utils.metrics import (
    model_training_duration_seconds,
    model_f2_score,
    model_auc_score,
    model_training_samples
)
import time

# Início do treino
logger.info("Iniciando treinamento do modelo")
start_time = time.time()

# ... código de treinamento existente ...

# Ao final
duration = time.time() - start_time
model_training_duration_seconds.set(duration)
model_f2_score.set(metricas['f2_score'])
model_auc_score.set(metricas['auc'])
model_training_samples.set(len(X_train) + len(X_test))

logger.success(f"Modelo treinado em {duration:.2f}s", extra={
    "f2_score": metricas['f2_score'],
    "auc": metricas['auc'],
    "samples": len(X_train) + len(X_test)
})
```

**Logs por Etapa:**
```python
logger.info("Etapa 1: Carregamento de dados")
logger.info("Etapa 2: Separação treino/teste")
logger.debug(f"X_train shape: {X_train.shape}")
logger.info("Etapa 3: Imputação de valores ausentes")
logger.info("Etapa 4: Transformações")
logger.info("Etapa 5: SMOTE")
logger.info("Etapa 6: Treinamento do modelo")
logger.success("Treinamento concluído")
```

---

### 5.2 Instrumentar Predição

**Arquivo:** `src/predicao.py`

**Adicionar:**
```python
from utils.logger import logger
from utils.metrics import (
    churn_predictions_high_risk,
    churn_predictions_by_level,
    churn_prediction_score_avg
)

logger.info("Carregando modelo treinado")
pipeline = joblib.load("models/pipeline_modelo_treinado.joblib")

logger.info("Fazendo predições")
preds = pipeline.predict_proba(X)[:,1]

# Calcular métricas de distribuição
high_risk_count = (preds > 0.7).sum()
churn_predictions_high_risk.set(high_risk_count)

avg_score = preds.mean()
churn_prediction_score_avg.set(avg_score)

# Por nível
baixo = (preds < 0.5).sum()
medio = ((preds >= 0.5) & (preds < 0.7)).sum()
alto = (preds >= 0.7).sum()

churn_predictions_by_level.labels(level="baixo").set(baixo)
churn_predictions_by_level.labels(level="medio").set(medio)
churn_predictions_by_level.labels(level="alto").set(alto)

logger.success(f"Predições concluídas: {len(preds)} clientes", extra={
    "alto_risco": int(high_risk_count),
    "score_medio": float(avg_score)
})
```

---

### 5.3 Métricas de Negócio

**Contexto Adicional nos Logs:**

```python
# API - Log de cada requisição
logger.info("Consulta de churn realizada", extra={
    "id_cliente": id_cliente,
    "risco": risco,
    "nivel": nivel_risco,
    "endpoint": "/churn/{id}",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": tempo_resposta
})

# Análise agregada
logger.info("Análise de risco concluída", extra={
    "total_clientes": total,
    "alto_risco": alto_risco_count,
    "percentual_alto_risco": (alto_risco_count/total)*100
})
```

---

## PASSO 6: Integração e Testes

### 6.1 Scripts de Inicialização

**Arquivo:** `scripts/start_monitoring.sh`

```bash
#!/bin/bash

echo "=== Iniciando Stack de Monitoramento MLOps ==="

# Criar networks se não existirem
docker network create mlops-network 2>/dev/null || true

echo ""
echo "1. Iniciando Prometheus..."
docker run -d \
  --name prometheus-mlops \
  --network mlops-network \
  -p 9090:9090 \
  -v prometheus_data:/prometheus \
  prometheus-mlops:latest

echo "✓ Prometheus rodando em http://localhost:9090"

echo ""
echo "2. Iniciando Grafana..."
docker run -d \
  --name grafana-mlops \
  --network mlops-network \
  -p 3000:3000 \
  -v grafana_data:/var/lib/grafana \
  grafana-mlops:latest

echo "✓ Grafana rodando em http://localhost:3000"
echo "  Login: admin / admin"

echo ""
echo "3. Aguardando serviços iniciarem..."
sleep 10

echo ""
echo "=== Status dos Serviços ==="
docker ps | grep mlops

echo ""
echo "=== Monitoramento Pronto! ==="
echo "Prometheus: http://localhost:9090"
echo "Grafana:    http://localhost:3000"
echo ""
echo "Próximo passo: Iniciar a API FastAPI"
echo "  uvicorn src.api_churn:app --reload"
```

**Tornar executável:**
```bash
chmod +x scripts/start_monitoring.sh
```

---

### 6.2 Testes de Carga

**Arquivo:** `scripts/test_api_load.py`

```python
"""
Script para gerar carga na API e testar monitoramento
"""
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8000"

def fazer_requisicao_churn(id_cliente):
    """Faz uma requisição para o endpoint de churn"""
    try:
        response = requests.get(f"{API_URL}/churn/{id_cliente}")
        return response.status_code
    except Exception as e:
        return None

def teste_carga(num_requests=100, workers=10):
    """Executa teste de carga"""
    print(f"Iniciando teste de carga: {num_requests} requests com {workers} workers")
    
    # IDs aleatórios (assumindo que existem entre 1-10000)
    ids = [random.randint(1, 10000) for _ in range(num_requests)]
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(fazer_requisicao_churn, ids))
    
    duration = time.time() - start_time
    
    # Estatísticas
    success = sum(1 for r in results if r == 200)
    not_found = sum(1 for r in results if r == 404)
    errors = sum(1 for r in results if r not in [200, 404])
    
    print(f"\n=== Resultados ===")
    print(f"Duração: {duration:.2f}s")
    print(f"Requests/s: {num_requests/duration:.2f}")
    print(f"Sucesso (200): {success}")
    print(f"Não encontrado (404): {not_found}")
    print(f"Erros: {errors}")

if __name__ == "__main__":
    print("Aguardando 5s para você abrir o Grafana...")
    time.sleep(5)
    
    print("\n=== Teste 1: Carga Leve ===")
    teste_carga(num_requests=50, workers=5)
    time.sleep(2)
    
    print("\n=== Teste 2: Carga Média ===")
    teste_carga(num_requests=200, workers=10)
    time.sleep(2)
    
    print("\n=== Teste 3: Carga Pesada ===")
    teste_carga(num_requests=500, workers=20)
    
    print("\n✓ Testes concluídos! Verifique os dashboards do Grafana.")
```

**Executar:**
```bash
python scripts/test_api_load.py
```

---

### 6.3 Documentação

**Arquivo:** `tutorial/MONITORING.md`

**Conteúdo:**
- Visão geral do monitoramento
- Como executar cada componente
- Interpretação das métricas
- Troubleshooting

**Arquivo:** `tutorial/PROMETHEUS.md`

**Conteúdo:**
- Introdução ao Prometheus
- PromQL básico
- Queries úteis
- Exemplos práticos

**Arquivo:** `tutorial/GRAFANA.md`

**Conteúdo:**
- Introdução ao Grafana
- Navegação nos dashboards
- Como criar painéis customizados
- Configuração de alertas
- Exportar/Importar dashboards

**Arquivo:** `monitoring/queries_exemplos.md`

**Conteúdo:**
- Queries PromQL organizadas por categoria
- Exemplos de análises
- Queries avançadas

---

### 6.4 Exemplos Práticos

**Queries PromQL Úteis:**

```promql
# Taxa de requisições por segundo
rate(api_requests_total[5m])

# Latência P95
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))

# Taxa de erro percentual
(sum(rate(api_errors_total[5m])) / sum(rate(api_requests_total[5m]))) * 100

# Clientes em alto risco
churn_predictions_high_risk

# Distribuição de risco
sum(churn_predictions_by_level) by (level)

# Evolução do F2-Score
model_f2_score

# Comparação com versão anterior (1 dia atrás)
model_f2_score - model_f2_score offset 1d
```

**Cenários de Debugging:**

1. **Latência alta detectada**
   - Abrir dashboard API Health
   - Verificar painel de latência
   - Correlacionar com logs: `tail -f logs/api.log | grep "duration_ms"`
   - Identificar endpoint lento

2. **Taxa de erro aumentou**
   - Verificar painel de erros por código
   - Buscar em logs: `grep ERROR logs/api.log`
   - Analisar stack traces

3. **F2-Score caiu**
   - Abrir dashboard ML Metrics
   - Verificar histórico
   - Comparar com versão anterior
   - Investigar data drift

---

## 📚 RECURSOS ADICIONAIS

### Queries PromQL por Categoria

**Performance:**
```promql
# Requests por endpoint
sum(rate(api_requests_total[5m])) by (endpoint)

# Latência média
avg(rate(api_request_duration_seconds_sum[5m]) / 
    rate(api_request_duration_seconds_count[5m]))

# P99 de latência
histogram_quantile(0.99, 
  sum(rate(api_request_duration_seconds_bucket[5m])) by (le))
```

**Erros:**
```promql
# Taxa de erro
rate(api_errors_total[5m]) / rate(api_requests_total[5m])

# Erros por tipo
sum(rate(api_errors_total[5m])) by (status_code)
```

**ML Metrics:**
```promql
# Evolução do F2-Score
model_f2_score

# Drift do score médio
churn_prediction_score_avg - churn_prediction_score_avg offset 1h

# Taxa de predições de alto risco
(churn_predictions_by_level{level="alto"} / 
 sum(churn_predictions_by_level)) * 100
```

---

## 🎯 OBJETIVOS PEDAGÓGICOS

### Por Fase

| Fase | Conceitos Ensinados | Habilidades Desenvolvidas |
|------|---------------------|---------------------------|
| **Passo 1** | Gestão de dependências, estrutura de projetos | Organização, planejamento |
| **Passo 2** | Logging estruturado, debugging | Rastreabilidade, troubleshooting |
| **Passo 3** | Métricas de aplicação, observabilidade | Monitoramento, performance |
| **Passo 4** | Visualização de dados, dashboards | Análise, comunicação de dados |
| **Passo 5** | MLOps, métricas de modelo | ML monitoring, data drift |
| **Passo 6** | Integração, testes, documentação | DevOps, SRE, boas práticas |

### Competências Desenvolvidas

✅ **Técnicas:**
- Configuração de ferramentas de monitoramento
- Escrita de queries PromQL
- Criação de dashboards visuais
- Análise de métricas e logs
- Debugging de aplicações

✅ **Conceituais:**
- Observabilidade vs Monitoramento
- Cultura DevOps/SRE
- MLOps e ML Monitoring
- Data Drift Detection
- Incident Response

✅ **Soft Skills:**
- Comunicação técnica
- Documentação clara
- Trabalho em equipe
- Tomada de decisão baseada em dados

---

## ⏱️ CRONOGRAMA SUGERIDO

### Distribuição em 6 Semanas (Aulas Semanais)

| Semana | Passo | Atividades | Entregável |
|--------|-------|------------|------------|
| **1** | Passo 1 | Setup do ambiente, estrutura de pastas | Ambiente configurado |
| **2** | Passo 2 | Implementar Loguru, integrar scripts | Logs funcionando |
| **3** | Passo 3 | Prometheus client, métricas básicas | /metrics endpoint |
| **4** | Passo 4 | Grafana, datasource, dashboards | Dashboards visuais |
| **5** | Passo 5 | Métricas ML, instrumentação completa | Métricas de modelo |
| **6** | Passo 6 | Testes, documentação, apresentação | Projeto completo |

### Por Aula (Exemplo de 2h/aula)

**Aula 1 - Preparação:**
- 30min: Apresentação do projeto e ferramentas
- 30min: Instalação de dependências
- 30min: Criação da estrutura de pastas
- 30min: Configuração inicial

**Aula 2 - Loguru:**
- 30min: Teoria de logging estruturado
- 45min: Implementação do módulo logger
- 45min: Integração nos scripts existentes

**Aula 3 - Prometheus:**
- 30min: Teoria de métricas
- 30min: Implementação do módulo metrics
- 30min: Instrumentação da API
- 30min: Container do Prometheus

**Aula 4 - Grafana:**
- 30min: Introdução ao Grafana
- 45min: Configuração de datasource
- 45min: Criação de dashboards

**Aula 5 - ML Metrics:**
- 30min: MLOps e monitoramento de modelos
- 60min: Instrumentação de treinamento e predição
- 30min: Análise de métricas de negócio

**Aula 6 - Integração:**
- 30min: Testes de carga
- 30min: Debugging e troubleshooting
- 30min: Documentação
- 30min: Apresentação de resultados

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Passo 1: Preparação
- [ ] Atualizar `requirements.txt`
- [ ] Instalar dependências
- [ ] Criar estrutura de pastas
- [ ] Criar `.gitkeep` em logs/
- [ ] Atualizar `.gitignore`

### Passo 2: Loguru
- [ ] Criar `src/utils/__init__.py`
- [ ] Criar `src/utils/logger.py`
- [ ] Modificar `src/treinamento.py`
- [ ] Modificar `src/predicao.py`
- [ ] Modificar `src/retreinamento.py`
- [ ] Modificar `src/api_churn.py`
- [ ] Testar logs em todos os scripts

### Passo 3: Prometheus
- [ ] Criar `src/utils/metrics.py`
- [ ] Instrumentar API com Instrumentator
- [ ] Adicionar métricas customizadas
- [ ] Criar `monitoring/prometheus/prometheus.yml`
- [ ] Criar `monitoring/prometheus/Dockerfile.prometheus`
- [ ] Build da imagem Prometheus
- [ ] Executar container Prometheus
- [ ] Testar endpoint `/metrics`

### Passo 4: Grafana
- [ ] Criar `monitoring/grafana/grafana.ini`
- [ ] Criar `monitoring/grafana/Dockerfile.grafana`
- [ ] Criar `provisioning/datasources/prometheus.yml`
- [ ] Criar `provisioning/dashboards/dashboards.yml`
- [ ] Criar dashboard `api-health.json`
- [ ] Criar dashboard `ml-metrics.json`
- [ ] Criar dashboard `business-churn.json`
- [ ] Criar dashboard `overview.json`
- [ ] Build da imagem Grafana
- [ ] Executar container Grafana
- [ ] Testar acesso ao Grafana
- [ ] Verificar datasource conectado
- [ ] Verificar dashboards carregados
- [ ] Configurar alertas

### Passo 5: ML Metrics
- [ ] Adicionar métricas em `treinamento.py`
- [ ] Adicionar métricas em `predicao.py`
- [ ] Exportar métricas de treinamento
- [ ] Calcular métricas de distribuição
- [ ] Testar métricas no Prometheus

### Passo 6: Integração
- [ ] Criar `scripts/start_monitoring.sh`
- [ ] Criar `scripts/test_api_load.py`
- [ ] Criar `scripts/export_metrics.py`
- [ ] Criar `tutorial/MONITORING.md`
- [ ] Criar `tutorial/PROMETHEUS.md`
- [ ] Criar `tutorial/GRAFANA.md`
- [ ] Criar `monitoring/queries_exemplos.md`
- [ ] Executar testes de carga
- [ ] Validar todos os componentes
- [ ] Tirar screenshots dos dashboards
- [ ] Revisar documentação

---

## 🚀 COMANDOS RÁPIDOS

### Iniciar Stack de Monitoramento

```bash
# Executar script de inicialização
./scripts/start_monitoring.sh

# OU manualmente:

# 1. Prometheus
docker run -d --name prometheus-mlops -p 9090:9090 prometheus-mlops:latest

# 2. Grafana
docker run -d --name grafana-mlops -p 3000:3000 grafana-mlops:latest

# 3. API
uvicorn src.api_churn:app --reload --port 8000
```

### Verificar Status

```bash
# Ver containers rodando
docker ps | grep mlops

# Logs do Prometheus
docker logs prometheus-mlops

# Logs do Grafana
docker logs grafana-mlops

# Logs da API
tail -f logs/api.log
```

### Acessar Serviços

```bash
# Abrir Prometheus
"$BROWSER" http://localhost:9090

# Abrir Grafana
"$BROWSER" http://localhost:3000

# Abrir API Docs
"$BROWSER" http://localhost:8000/docs

# Endpoint de métricas
curl http://localhost:8000/metrics
```

### Parar e Limpar

```bash
# Parar containers
docker stop prometheus-mlops grafana-mlops

# Remover containers
docker rm prometheus-mlops grafana-mlops

# Limpar volumes (CUIDADO: perde dados)
docker volume rm prometheus_data grafana_data
```

---

## 📖 REFERÊNCIAS

### Documentação Oficial
- **Loguru:** https://loguru.readthedocs.io/
- **Prometheus:** https://prometheus.io/docs/
- **Grafana:** https://grafana.com/docs/grafana/latest/
- **FastAPI:** https://fastapi.tiangolo.com/

### Tutoriais Recomendados
- Prometheus Basics: https://prometheus.io/docs/introduction/first_steps/
- PromQL Guide: https://prometheus.io/docs/prometheus/latest/querying/basics/
- Grafana Fundamentals: https://grafana.com/tutorials/grafana-fundamentals/
- MLOps Best Practices: https://ml-ops.org/

### Dashboards de Exemplo
- Grafana Dashboard Library: https://grafana.com/grafana/dashboards/
- FastAPI Dashboard: ID 16110
- Node Exporter: ID 1860

---

## 💡 DICAS E BOAS PRÁTICAS

### Logging
✅ Use níveis apropriados (INFO, WARNING, ERROR)
✅ Adicione contexto relevante nos logs
✅ Evite logar informações sensíveis
✅ Use logs estruturados (JSON) para análise

### Métricas
✅ Nomeie métricas de forma consistente
✅ Use labels para dimensionalidade
✅ Evite cardinalidade alta em labels
✅ Documente o significado de cada métrica

### Dashboards
✅ Organize painéis logicamente
✅ Use cores significativas (verde=ok, vermelho=erro)
✅ Adicione descrições nos painéis
✅ Configure time ranges apropriados

### Alertas
✅ Defina thresholds realistas
✅ Evite alertas excessivos (alert fatigue)
✅ Teste alertas regularmente
✅ Documente ações de resposta

---

## 🎓 EXERCÍCIOS PROPOSTOS PARA ALUNOS

### Exercício 1: Criar Métrica Customizada
**Objetivo:** Adicionar uma métrica que conta quantos clientes de cada país foram consultados

**Tarefas:**
1. Definir métrica em `metrics.py`
2. Instrumentar endpoint da API
3. Criar painel no Grafana
4. Analisar distribuição geográfica

### Exercício 2: Dashboard Personalizado
**Objetivo:** Criar dashboard comparando performance de diferentes versões do modelo

**Tarefas:**
1. Exportar métricas de múltiplos treinamentos
2. Criar dashboard com painéis comparativos
3. Usar variáveis para filtrar por versão
4. Adicionar anotações de deploys

### Exercício 3: Alerta de Data Drift
**Objetivo:** Configurar alerta quando score médio aumentar significativamente

**Tarefas:**
1. Definir query PromQL para detectar drift
2. Configurar alerta no Grafana
3. Testar com dados simulados
4. Documentar plano de ação

### Exercício 4: Análise de Logs
**Objetivo:** Encontrar padrões em logs usando grep/awk/jq

**Tarefas:**
1. Buscar todos os erros na última hora
2. Contar requisições por endpoint
3. Calcular tempo médio de resposta
4. Identificar clientes mais consultados

---

## 📊 MÉTRICAS DE SUCESSO DO PROJETO

### Critérios de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Implementação Técnica** | 40% | Todos os componentes funcionando |
| **Dashboards** | 20% | Visualizações claras e úteis |
| **Documentação** | 20% | Tutoriais e README completos |
| **Testes** | 10% | Testes de carga executados |
| **Apresentação** | 10% | Demo e explicação do projeto |

### Indicadores de Sucesso

✅ Loguru capturando logs de todos os scripts
✅ Prometheus coletando métricas da API
✅ Grafana exibindo 4 dashboards funcionais
✅ Métricas de ML sendo registradas
✅ Alertas configurados e testados
✅ Documentação completa
✅ Testes de carga validando performance

---

## 🔄 PRÓXIMAS EVOLUÇÕES (Opcional)

### Para Alunos Avançados

**Nível 1 - Intermediário:**
- [ ] Adicionar Loki para centralização de logs
- [ ] Criar mais dashboards específicos
- [ ] Implementar notificações via Slack
- [ ] Adicionar métricas de infraestrutura (CPU, memória)

**Nível 2 - Avançado:**
- [ ] Implementar Jaeger para distributed tracing
- [ ] Adicionar Alertmanager
- [ ] Criar pipeline de CI/CD com validação de métricas
- [ ] Implementar feature store com monitoramento

**Nível 3 - Expert:**
- [ ] Data drift detection com Evidently
- [ ] Model explainability com SHAP
- [ ] A/B testing de modelos com métricas
- [ ] Anomaly detection em métricas

---

## ✨ CONCLUSÃO

Este planejamento fornece um guia completo para implementar observabilidade em um projeto MLOps acadêmico. Seguindo os 6 passos, os alunos desenvolverão competências práticas em:

- **Logging estruturado** com Loguru
- **Métricas de aplicação** com Prometheus
- **Visualização de dados** com Grafana
- **MLOps** e monitoramento de modelos
- **DevOps/SRE** e cultura de observabilidade

**Tempo estimado:** 6 semanas  
**Nível:** Intermediário  
**Pré-requisitos:** Python, Docker, FastAPI básico

---

**Última atualização:** Novembro 2025  
**Versão:** 1.0  
**Autor:** Projeto MLOps Monitoring Prep
