# Scripts Auxiliares

Este diretório contém scripts para auxiliar no desenvolvimento, testes e operação do sistema de monitoramento.

## 📁 Scripts Disponíveis

### 📊 Exportação de Métricas

#### `export_metrics.py`
Exporta métricas Prometheus para arquivo de texto no formato Prometheus.

**Quando usar:**
- Após executar scripts batch (treinamento, predição, retreinamento)
- Para debugging de métricas
- Para análise offline de métricas

**Como usar:**
```bash
# Exportar para caminho padrão (outputs/prometheus_metrics.txt)
python scripts/export_metrics.py

# Exportar para caminho customizado
python scripts/export_metrics.py outputs/my_metrics.txt
```

**Saída:**
```
✅ Métricas exportadas para: outputs/prometheus_metrics.txt
📊 Total de métricas: 15
📈 Resumo das métricas exportadas:
  - model_f2_score: gauge
  - model_auc_score: gauge
  - model_predictions_total: counter
  ...
```

### 🔄 Workflow Completo de MLOps

Para executar um workflow completo com monitoramento:

```bash
# 1. Treinar modelo
python src/treinamento.py

# 2. Exportar métricas de treinamento
python scripts/export_metrics.py

# 3. Fazer predições
python src/predicao.py

# 4. Exportar métricas de predição
python scripts/export_metrics.py

# 5. (Opcional) Retreinar com novos dados
python src/retreinamento.py data/raw/dados_novos_2.csv
python src/treinamento.py
python scripts/export_metrics.py
```

### 🚀 Monitoramento em Produção

Para ambiente de produção com API:

```bash
# 1. Iniciar Prometheus
cd monitoring/prometheus
docker build -t prometheus-mlops -f Dockerfile.prometheus .
docker run -d --name prometheus -p 9090:9090 --network host prometheus-mlops

# 2. Iniciar Grafana
cd ../grafana
docker build -t grafana-mlops -f Dockerfile.grafana .
docker run -d --name grafana -p 3000:3000 --network host grafana-mlops

# 3. Iniciar API
cd ../..
docker build -t api-churn -f Dockerfile.api .
docker run -d --name api-churn -p 8000:8000 api-churn

# 4. Acessar dashboards
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
# - API Docs: http://localhost:8000/docs
```

## 🔍 Troubleshooting

### Métricas não aparecem no arquivo

**Problema:** `prometheus_metrics.txt` está vazio ou faltando métricas

**Solução:**
```bash
# Verificar se as métricas foram atualizadas nos scripts
grep "update_model_metrics" src/treinamento.py
grep "MODEL_PREDICTIONS_TOTAL" src/predicao.py

# Executar o script que gera as métricas primeiro
python src/treinamento.py  # ou src/predicao.py
python scripts/export_metrics.py
```

### Erro de import

**Problema:** `ModuleNotFoundError: No module named 'utils'`

**Solução:**
```bash
# Executar a partir da raiz do projeto
cd /workspaces/mlops-monitoring-prep
python scripts/export_metrics.py
```

## 📚 Próximos Passos

1. Consultar `tutorial/` para tutoriais completos
2. Ver `monitoring/PLANEJAMENTO_MONITORAMENTO.md` para visão geral
3. Acessar `monitoring/prometheus/README.md` para detalhes do Prometheus
4. Acessar `monitoring/grafana/README.md` para detalhes do Grafana

