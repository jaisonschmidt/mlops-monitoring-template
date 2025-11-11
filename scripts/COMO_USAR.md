# 🚀 Como Usar os Scripts de Monitoramento

## Script Principal: start_monitoring.sh

### O que o script faz automaticamente:

1. **✅ Verifica e instala dependências Python**
   - Detecta se `loguru`, `prometheus-client`, etc. estão instalados
   - Instala automaticamente se necessário

2. **🤖 Treina o modelo (se não existir)**
   - Verifica se `models/pipeline_modelo_treinado.joblib` existe
   - Se não, executa `src/treinamento.py` automaticamente
   - Gera métricas de performance

3. **🔮 Gera predições (se não existirem)**
   - Verifica se `outputs/predicoes.csv` existe
   - Se não, executa `src/predicao.py` automaticamente
   - Prepara dados para a API

4. **🐳 Inicia containers Docker**
   - Prometheus (porta 9090)
   - Grafana (porta 3000)
   - API de Churn (porta 8000)

5. **🔍 Valida a saúde de tudo**
   - Health checks dos 3 containers
   - Verifica coleta de métricas

## Uso Básico

### Iniciar tudo (1 comando!)

```bash
./scripts/start_monitoring.sh
```

**OU** se não tiver permissão de execução:

```bash
bash scripts/start_monitoring.sh
```

### Primeira execução (sem dependências instaladas)

O script detecta automaticamente e:
1. Instala dependências (`pip install -r requirements.txt`)
2. Treina o modelo (~2-3 minutos)
3. Gera predições (~30 segundos)
4. Sobe os containers (~1 minuto)

**Tempo total**: ~5 minutos

### Execuções subsequentes

Se modelo e predições já existem:
1. Valida que estão prontos
2. Sobe os containers

**Tempo total**: ~1 minuto

## Parar a Stack

```bash
./scripts/stop_monitoring.sh
```

### Parar e limpar tudo (imagens também)

```bash
./scripts/stop_monitoring.sh --clean
```

## Acessar os Serviços

Após o script finalizar, acesse:

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **API** | http://localhost:8000/docs | - |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin / admin |

## Testar o Sistema

### Gerar tráfego na API

```bash
python scripts/test_api_load.py
```

Isso vai:
- Fazer 100 requisições de predição
- Gerar métricas no Prometheus
- Atualizar dashboards no Grafana

### Ver logs em tempo real

```bash
# Logs da API
docker logs -f api-churn

# Logs do Prometheus
docker logs -f prometheus

# Logs do Grafana
docker logs -f grafana
```

## Troubleshooting

### ❌ Erro: "Dependências não instaladas"

**Solução**: O script instala automaticamente. Se falhar:

```bash
pip install -r requirements.txt
bash scripts/start_monitoring.sh
```

### ❌ Erro: "Modelo não encontrado"

**Solução**: O script treina automaticamente. Se falhar:

```bash
python src/treinamento.py
bash scripts/start_monitoring.sh
```

### ❌ Erro: "Predições não encontradas"

**Solução**: O script gera automaticamente. Se falhar:

```bash
python src/predicao.py
bash scripts/start_monitoring.sh
```

### ❌ Erro: "Port already in use"

**Solução**: Parar containers existentes:

```bash
docker stop prometheus grafana api-churn
docker rm prometheus grafana api-churn
bash scripts/start_monitoring.sh
```

### ❌ Grafana não carrega dashboards

**Solução**: Aguardar ~30 segundos após iniciar:

```bash
# Verificar logs
docker logs grafana

# Reiniciar se necessário
docker restart grafana
```

## Workflow Completo de Desenvolvimento

### 1. Clone e Setup Inicial

```bash
git clone <repo>
cd mlops-monitoring-prep
bash scripts/start_monitoring.sh
```

### 2. Fazer Mudanças no Modelo

```bash
# Editar src/treinamento.py
# ...

# Retreinar
python src/treinamento.py

# Gerar novas predições
python src/predicao.py

# Reiniciar API para carregar novas predições
docker restart api-churn
```

### 3. Validar no Grafana

1. Acesse http://localhost:3000
2. Vá em **ML Model Metrics**
3. Verifique se F2-Score e AUC mudaram

### 4. Testar com Carga

```bash
python scripts/test_api_load.py
```

### 5. Parar quando terminar

```bash
bash scripts/stop_monitoring.sh
```

## Fluxo Automático vs Manual

### ✅ Automático (Recomendado)

```bash
bash scripts/start_monitoring.sh
# Faz tudo automaticamente!
```

### 🔧 Manual (Para debug)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Treinar modelo
python src/treinamento.py

# 3. Gerar predições
python src/predicao.py

# 4. Build Prometheus
cd monitoring/prometheus
docker build -t prometheus-mlops -f Dockerfile.prometheus .
docker run -d --name prometheus -p 9090:9090 --network host prometheus-mlops

# 5. Build Grafana
cd ../grafana
docker build -t grafana-mlops -f Dockerfile.grafana .
docker run -d --name grafana -p 3000:3000 --network host grafana-mlops

# 6. Build API
cd ../..
docker build -t api-churn -f Dockerfile.api .
docker run -d --name api-churn -p 8000:8000 api-churn

# 7. Testar
python scripts/test_api_load.py
```

## Dicas para Alunos

### 🎓 Primeira vez usando?

1. Execute `bash scripts/start_monitoring.sh`
2. Aguarde ~5 minutos (primeira vez é mais lento)
3. Acesse Grafana: http://localhost:3000
4. Login: admin / admin
5. Explore os 4 dashboards
6. Execute teste: `python scripts/test_api_load.py`
7. Volte no Grafana e veja métricas atualizarem!

### 🧪 Experimentando?

```bash
# Modificar dados de treino
# vim data/raw/dados_treino.csv

# Retreinar
python src/retreinamento.py
python src/treinamento.py

# Reiniciar API
docker restart api-churn

# Ver mudanças no Grafana
```

### 📊 Apresentando projeto?

1. Inicie tudo: `bash scripts/start_monitoring.sh`
2. Abra Grafana no navegador
3. Selecione dashboard **System Overview**
4. Execute em outro terminal: `python scripts/test_api_load.py`
5. Mostre métricas atualizando em tempo real! 🎉

## Variáveis de Ambiente (Opcional)

```bash
# Mudar portas (se necessário)
export API_PORT=8001
export PROMETHEUS_PORT=9091
export GRAFANA_PORT=3001

bash scripts/start_monitoring.sh
```

## Recursos Adicionais

- 📖 [Tutorial Prometheus](../tutorial/PROMETHEUS.md)
- 📈 [Tutorial Grafana](../tutorial/GRAFANA.md)
- 🎯 [Planejamento](../monitoring/PLANEJAMENTO_MONITORAMENTO.md)
- 📋 [Resumo Implementação](../RESUMO_IMPLEMENTACAO.md)

---

**💡 Dica**: Na dúvida, sempre use `bash scripts/start_monitoring.sh` - ele faz tudo pra você!
