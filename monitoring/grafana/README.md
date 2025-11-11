# Grafana - Visualização de Métricas MLOps

Este diretório contém a configuração completa do Grafana para visualização das métricas do sistema MLOps de predição de churn.

## 📊 Dashboards Disponíveis

### 1. **System Overview** (Visão Geral)
- **Público-alvo**: Gerentes, visão executiva
- **Refresh**: 10s
- **Conteúdo**:
  - Status geral do sistema
  - KPIs principais (F2-Score, Taxa de Erro, Uptime)
  - Atividade de requisições e predições
  - Distribuição de risco de churn
  - Tabela resumo de métricas

### 2. **API Health & Performance**
- **Público-alvo**: DevOps, SRE
- **Refresh**: 10s
- **Conteúdo**:
  - Status da API (UP/DOWN)
  - Taxa de requisições/segundo
  - Latência (P50, P95, P99)
  - Taxa de erro
  - Requisições ativas
  - Erros por status code

### 3. **ML Model Metrics**
- **Público-alvo**: Data Scientists, ML Engineers
- **Refresh**: 30s
- **Conteúdo**:
  - F2-Score (gauge)
  - AUC-ROC (gauge)
  - Precisão e Recall
  - Tempo de treinamento
  - Amostras de treino
  - Evolução das métricas
  - Taxa de predições

### 4. **Business Intelligence - Churn**
- **Público-alvo**: Product Managers, Business Analysts
- **Refresh**: 30s
- **Conteúdo**:
  - Clientes em alto risco (alerta)
  - Score médio de churn
  - Distribuição de risco (pie chart)
  - Evolução temporal por nível
  - Variações e tendências
  - Taxa de consultas

## 🚀 Como Usar

### Build da Imagem

```bash
cd monitoring/grafana
docker build -f Dockerfile.grafana -t grafana-mlops:latest .
```

### Executar Container

```bash
docker run -d \
  --name grafana-mlops \
  -p 3000:3000 \
  -v grafana_data:/var/lib/grafana \
  grafana-mlops:latest
```

### Acessar Grafana

1. Abrir navegador em: `http://localhost:3000`
2. **Login padrão**:
   - Usuário: `admin`
   - Senha: `admin`
3. Trocar senha no primeiro acesso (recomendado)

## 📁 Estrutura de Arquivos

```
grafana/
├── Dockerfile.grafana              # Imagem Docker
├── grafana.ini                     # Configuração principal
├── provisioning/
│   ├── datasources/
│   │   └── prometheus.yml          # Auto-config Prometheus
│   └── dashboards/
│       ├── dashboards.yml          # Provider de dashboards
│       ├── api-health.json         # Dashboard API
│       ├── ml-metrics.json         # Dashboard ML
│       ├── business-churn.json     # Dashboard Negócio
│       └── overview.json           # Dashboard Overview
└── screenshots/                    # Screenshots dos dashboards
```

## ⚙️ Configuração

### Datasource Prometheus

O datasource é configurado automaticamente via provisioning:
- **Nome**: Prometheus
- **URL**: `http://host.docker.internal:9090`
- **Acesso**: Proxy
- **Intervalo**: 15s

### Dashboards

Os dashboards são provisionados automaticamente na pasta **"MLOps Monitoring"**.

## 🔔 Alertas Configurados

### Dashboard: API Health & Performance
- **Latência P95 Alta**: P95 > 2s por 5 minutos

### Dashboard: Business - Churn
- **Score Médio Alto**: Score > 0.6

## 🎨 Personalização

### Editar Dashboards

1. Acesse o dashboard no Grafana
2. Clique em "Dashboard settings" (⚙️)
3. Faça suas modificações
4. Salve

### Exportar Dashboard

1. Dashboard settings → JSON Model
2. Copiar JSON
3. Salvar em `provisioning/dashboards/<nome>.json`

### Importar Dashboard

1. Criar arquivo JSON em `provisioning/dashboards/`
2. Adicionar ao `dashboards.yml` se necessário
3. Reiniciar container

## 📊 Variáveis de Dashboard

Os dashboards suportam variáveis para filtragem:
- **Intervalo de tempo**: Ajustável no canto superior direito
- **Refresh**: Configurável por dashboard

## 🔧 Troubleshooting

### Grafana não inicia

```bash
# Ver logs
docker logs grafana-mlops

# Verificar permissões
docker exec -it grafana-mlops ls -la /var/lib/grafana
```

### Datasource não conecta

```bash
# Verificar se Prometheus está rodando
curl http://localhost:9090/-/healthy

# Testar conectividade do container
docker exec -it grafana-mlops wget -O- http://host.docker.internal:9090/api/v1/status/config
```

### Dashboards não aparecem

```bash
# Verificar provisioning
docker exec -it grafana-mlops ls -la /etc/grafana/provisioning/dashboards/

# Recarregar provisioning
# Reiniciar o container
docker restart grafana-mlops
```

### Sem dados nos painéis

1. Verificar se a API está rodando e gerando métricas
2. Verificar se Prometheus está coletando: `http://localhost:9090/targets`
3. Testar query direto no Prometheus
4. Verificar intervalo de tempo no dashboard

## 📖 Recursos Adicionais

- **Grafana Docs**: https://grafana.com/docs/grafana/latest/
- **Dashboard Best Practices**: https://grafana.com/docs/grafana/latest/best-practices/
- **PromQL Queries**: Ver `monitoring/queries_exemplos.md`

## 🔐 Segurança

### Produção

Para ambiente de produção, alterar:

```ini
[security]
admin_user = seu_usuario
admin_password = senha_forte

[users]
allow_sign_up = false
```

### Variáveis de Ambiente

```bash
docker run -d \
  --name grafana-mlops \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_USER=admin" \
  -e "GF_SECURITY_ADMIN_PASSWORD=sua_senha" \
  grafana-mlops:latest
```

## 💡 Dicas

1. **Favoritar dashboards importantes**: ⭐ no menu
2. **Criar playlists**: Para exibir múltiplos dashboards
3. **Usar anotações**: Marcar eventos importantes (deploys, incidentes)
4. **Compartilhar**: Link direto ou snapshot
5. **Alertas**: Configurar notification channels (email, Slack)

## 📸 Screenshots

Screenshots dos dashboards estão disponíveis em `screenshots/`:
- `overview.png`
- `api-health.png`
- `ml-metrics.png`
- `business-churn.png`
