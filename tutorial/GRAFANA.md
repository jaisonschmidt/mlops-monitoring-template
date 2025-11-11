# 📊 Tutorial: Grafana - Visualização de Dados

## 🎯 Objetivos de Aprendizagem

Ao final deste tutorial, você será capaz de:
- ✅ Entender o que é Grafana e suas funcionalidades
- ✅ Navegar pelos dashboards pré-configurados
- ✅ Criar painéis (panels) personalizados
- ✅ Escrever queries PromQL no Grafana
- ✅ Configurar alertas visuais
- ✅ Exportar e compartilhar dashboards

## 📚 O que é Grafana?

**Grafana** é uma plataforma de observabilidade e visualização que:
- Conecta-se a múltiplas fontes de dados (Prometheus, MySQL, etc.)
- Cria dashboards interativos com gráficos
- Suporta alertas visuais e notificações
- Permite compartilhamento de dashboards

### Por que usar Grafana?

| Prometheus | Grafana |
|------------|---------|
| ✅ Coleta e armazena métricas | ✅ Visualiza métricas |
| ✅ Queries PromQL | ✅ Interface gráfica para PromQL |
| ❌ Gráficos básicos | ✅ Dashboards profissionais |
| ❌ Difícil compartilhar | ✅ Fácil export/import |

## 🚀 Passo a Passo

### 1️⃣ Acessando o Grafana

```bash
# Se ainda não iniciou:
./scripts/start_monitoring.sh
```

Abra o navegador em: **http://localhost:3000**

**Credenciais padrão:**
- 👤 Usuário: `admin`
- 🔑 Senha: `admin`

> ⚠️ **Primeira vez**: Você será solicitado a alterar a senha. Pode clicar em "Skip" para pular.

### 2️⃣ Explorando a Interface

Após login, você verá:

```
┌─────────────────────────────────────────┐
│  🏠 Home  📊 Dashboards  ⚙️ Config      │
├─────────────────────────────────────────┤
│                                         │
│  🔍 Search dashboards...                │
│                                         │
│  📂 Dashboards Disponíveis:             │
│    • System Overview                    │
│    • API Health & Performance           │
│    • ML Model Metrics                   │
│    • Business Intelligence - Churn      │
│                                         │
└─────────────────────────────────────────┘
```

### 3️⃣ Dashboard 1: System Overview

**Objetivo**: Visão executiva de alto nível

1. Clique em **Dashboards** (ícone de quatro quadrados)
2. Selecione **System Overview**

**O que você verá:**

| Painel | Descrição | Interpretação |
|--------|-----------|---------------|
| 🟢 **API Status** | UP/DOWN | Verde = OK, Vermelho = Problema |
| 🎯 **F2-Score** | Qualidade do modelo | >0.8 = Bom (verde) |
| 📊 **AUC** | Discriminação | >0.85 = Excelente |
| ❌ **Taxa Erro** | % de erros HTTP | <3% = OK (verde) |
| ⏰ **Uptime 24h** | Disponibilidade | >99% = Excelente |
| 🚨 **Alto Risco** | Clientes críticos | Alerta se >1000 |

**Dica**: Este dashboard é ideal para mostrar em TVs ou reuniões executivas!

### 4️⃣ Dashboard 2: API Health & Performance

**Objetivo**: Monitoramento de infraestrutura

1. Acesse **Dashboards → API Health & Performance**

**Painéis importantes:**

#### Taxa de Requisições
```
Mostra: Requisições por segundo (RPS)
Uso: Identificar picos de tráfego
Alerta: Queda súbita pode indicar problema
```

#### Latência (P50, P95, P99)
```
P50 = Mediana (50% das requisições)
P95 = 95% das requisições
P99 = 99% das requisições (pior caso)

Ideal:
  P50 < 100ms
  P95 < 300ms  
  P99 < 500ms
```

#### Taxa de Erros
```
Mostra: % de erros 5xx
Meta: < 1%
Crítico: > 5%
```

**Experimente:**
1. Execute teste de carga: `python scripts/test_api_load.py`
2. Observe os gráficos atualizarem em tempo real
3. Note como latência aumenta com carga

### 5️⃣ Dashboard 3: ML Model Metrics

**Objetivo**: Monitorar qualidade do modelo

1. Acesse **Dashboards → ML Model Metrics**

**Métricas-chave:**

#### F2-Score (Gauge)
```
0.0 - 0.6: 🔴 Ruim
0.6 - 0.8: 🟡 Aceitável
0.8 - 1.0: 🟢 Excelente

Por que F2? Prioriza recall (não perder churners)
```

#### AUC-ROC (Gauge)
```
0.5: 🔴 Aleatório (sem poder de discriminação)
0.7 - 0.8: 🟡 Aceitável
0.85+: 🟢 Excelente
```

#### Evolução de Métricas
```
Gráfico de linha mostrando F2 e AUC ao longo do tempo
Use para: Detectar degradação de performance
```

**Workflow de Monitoramento:**

```bash
# 1. Treinar modelo
python src/treinamento.py

# 2. Verificar métricas no dashboard
# Aguardar 30s e recarregar página

# 3. Se métricas baixas, retreinar
python src/retreinamento.py
python src/treinamento.py
```

### 6️⃣ Dashboard 4: Business Intelligence - Churn

**Objetivo**: KPIs de negócio

1. Acesse **Dashboards → Business Intelligence - Churn**

**Painéis de negócio:**

#### Clientes em Alto Risco
```
Mostra: Total de clientes com P(churn) >= 70%
Ação: Se > 1000, iniciar campanha de retenção
```

#### Distribuição de Risco (Pie Chart)
```
🟢 Baixo: P(churn) < 30%
🟡 Médio: 30% <= P(churn) < 70%
🔴 Alto: P(churn) >= 70%

Ideal: Maioria em verde/amarelo
```

#### Score Médio de Churn
```
0.0 - 0.3: 🟢 Base saudável
0.3 - 0.5: 🟡 Atenção
0.5+: 🔴 Crítico - muitos em risco
```

**Exemplo de Análise:**

```
Cenário: Dashboard mostra 850 clientes em alto risco

Ações:
1. Filtrar clientes de alto valor
2. Criar campanha de retenção
3. Monitorar evolução no dashboard
4. Medir impacto após 1 semana
```

## 🎨 Criando Painéis Personalizados

### Criar Novo Painel

1. Abra qualquer dashboard
2. Clique em **Add → Visualization**
3. Escolha o tipo de painel:

| Tipo | Quando usar |
|------|-------------|
| **Time series** | Evolução temporal de métricas |
| **Stat** | Valores atuais (ex: uptime) |
| **Gauge** | Métricas com limites (ex: score) |
| **Bar chart** | Comparação entre categorias |
| **Pie chart** | Distribuições percentuais |
| **Table** | Dados tabulares |

### Exemplo: Criar Painel de "Predições por Endpoint"

**Passo a passo:**

1. Click **Add → Visualization**
2. Selecione **Time series**
3. No campo **Query**, digite:
   ```promql
   sum(rate(http_requests_total{endpoint="/predict"}[5m])) by (method)
   ```
4. Em **Panel options**:
   - Title: `Predições por Endpoint`
   - Description: `Taxa de requisições no endpoint /predict`
5. Em **Axes**:
   - Left Y: `requests/s`
6. Click **Apply**

### Exemplo: Gauge de Clientes Ativos

```promql
# Query
sum(churn_predictions_by_level)

# Configuração:
- Type: Gauge
- Min: 0
- Max: 10000
- Thresholds:
  * 0-3000: Verde
  * 3000-7000: Amarelo
  * 7000-10000: Vermelho
```

## 🔔 Configurando Alertas

Grafana permite alertas visuais nos painéis.

### Criar Alerta de F2-Score Baixo

1. Edite o painel "F2-Score"
2. Vá para aba **Alert**
3. Click **Create alert**
4. Configure:
   ```
   Condition: WHEN last() OF query(model_f2_score)
              IS BELOW 0.7
   
   Evaluate every: 1m
   For: 5m
   
   Notification: Email / Slack
   Message: "⚠️ F2-Score abaixo do limite aceitável!"
   ```

5. Salve o painel

> ⚠️ **Nota**: Para notificações funcionarem, é preciso configurar um canal (Email, Slack, etc.) em **Alerting → Notification channels**

## 📥 Exportando e Importando Dashboards

### Exportar Dashboard

1. Abra o dashboard
2. Click no ícone ⚙️ (Settings)
3. Click **JSON Model**
4. Click **Copy to Clipboard** ou **Save to file**

### Importar Dashboard

1. Click **Dashboards → Import**
2. Cole o JSON ou faça upload do arquivo
3. Selecione o datasource (Prometheus)
4. Click **Import**

### Compartilhar Dashboard

```bash
# Os dashboards estão em:
monitoring/grafana/provisioning/dashboards/

# Para compartilhar com colegas:
1. Copie o arquivo JSON
2. Envie via email/git
3. Colega importa no Grafana dele
```

## 🎓 Exercícios Práticos

### Exercício 1: Criar Painel de Uptime Semanal

**Objetivo**: Mostrar uptime dos últimos 7 dias

<details>
<summary>💡 Ver solução</summary>

```promql
# Query
avg_over_time(up{job="api-churn"}[7d]) * 100

# Configuração:
- Type: Stat
- Unit: Percent (0-100)
- Decimals: 2
- Color: Green
- Title: "Uptime 7 dias"
```
</details>

### Exercício 2: Tabela de Métricas por Método HTTP

**Objetivo**: Mostrar requisições agrupadas por método (GET, POST)

<details>
<summary>💡 Ver solução</summary>

```promql
# Query
sum(rate(http_requests_total[5m])) by (method)

# Configuração:
- Type: Table
- Transform: "Organize fields"
  * Renomear "Value" → "Requests/s"
  * Renomear "method" → "HTTP Method"
```
</details>

### Exercício 3: Alerta Visual de Alta Latência

**Objetivo**: Painel fica vermelho se P95 > 500ms

<details>
<summary>💡 Ver solução</summary>

```promql
# Query
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) * 1000

# Configuração:
- Type: Stat
- Unit: milliseconds (ms)
- Thresholds:
  * 0-300: Verde
  * 300-500: Amarelo
  * 500+: Vermelho
- Color scheme: "From thresholds (by value)"
```
</details>

## 🔧 Troubleshooting

### Problema: "No data" nos gráficos

**Possíveis causas:**
1. Prometheus não está coletando métricas
2. Range de tempo inadequado
3. Query incorreta

**Soluções:**
```bash
# 1. Verificar se Prometheus está coletando
curl http://localhost:9090/api/v1/targets

# 2. Ajustar range de tempo no Grafana (canto superior direito)
#    Clique em "Last 6 hours" → "Last 5 minutes"

# 3. Testar query diretamente no Prometheus
#    http://localhost:9090/graph
```

### Problema: Dashboard não carrega

**Soluções:**
```bash
# 1. Verificar se Grafana está rodando
docker ps | grep grafana

# 2. Ver logs
docker logs grafana

# 3. Reiniciar Grafana
docker restart grafana

# 4. Aguardar 30 segundos e recarregar página
```

### Problema: Gráficos lentos

**Otimizações:**
- Reduza o range de tempo (ex: 1h em vez de 7d)
- Use queries mais eficientes (agregações)
- Aumente o intervalo de refresh (ex: 1m em vez de 5s)

## 📊 Melhores Práticas

### 1. Organização de Dashboards

```
✅ BOM:
  - 1 dashboard por objetivo
  - Máximo 10-12 painéis por dashboard
  - Fluxo lógico (cima→baixo, esquerda→direita)

❌ RUIM:
  - Dashboard com 30+ painéis
  - Painéis sem contexto
  - Cores e escalas inconsistentes
```

### 2. Uso de Cores

```
🟢 Verde: Tudo OK, valores bons
🟡 Amarelo: Atenção, valores aceitáveis
🔴 Vermelho: Problema, ação necessária
🔵 Azul: Neutro, informativo
```

### 3. Nomenclatura

```
✅ BOM:
  "Taxa de Requisições (req/s)"
  "F2-Score do Modelo"
  "Clientes em Alto Risco"

❌ RUIM:
  "Metric 1"
  "rate_http"
  "churn_high"
```

### 4. Performance

```promql
# ✅ EFICIENTE - Agregação primeiro
sum(rate(http_requests_total[5m])) by (method)

# ❌ LENTO - Muitas séries temporais
rate(http_requests_total[5m])  # Sem agregação
```

## 🎯 Casos de Uso Reais

### Monitoramento em Produção

**Cenário**: Você deployou o modelo em produção

**Dashboards necessários:**
1. **System Overview**: TV na sala da equipe
2. **API Health**: NOC (Centro de Operações)
3. **ML Metrics**: Cientistas de dados
4. **Business Churn**: Time de negócio

**Workflow diário:**
```
08:00 - Verificar System Overview
10:00 - Analisar Business Churn (reunião diária)
14:00 - Revisar ML Metrics (semanalmente)
18:00 - Validar API Health antes de sair
```

### Debugging de Incidentes

**Cenário**: Usuários reportam API lenta

**Passo a passo:**
1. Abrir **API Health & Performance**
2. Verificar painel "Latência P95"
3. Ver se há pico em "Taxa de Requisições"
4. Correlacionar com "Taxa de Erros"
5. Usar Time Range Picker para ver histórico

### A/B Testing de Modelo

**Cenário**: Testar novo modelo vs. modelo atual

**Setup:**
1. Deployar modelos com labels diferentes
2. Modificar queries para filtrar por modelo:
   ```promql
   model_f2_score{model="v1"}
   model_f2_score{model="v2"}
   ```
3. Criar painel comparativo side-by-side
4. Analisar por 1 semana
5. Escolher modelo vencedor

## 📚 Recursos Adicionais

### Documentação
- [Grafana Official Docs](https://grafana.com/docs/)
- [Panel Plugins](https://grafana.com/grafana/plugins/)
- [Dashboard Examples](https://grafana.com/grafana/dashboards/)

### Comunidade
- [Grafana Community Forums](https://community.grafana.com/)
- [GitHub Examples](https://github.com/grafana/grafana/tree/main/public/app/plugins/panel)

### Vídeos
- [Getting Started with Grafana](https://grafana.com/tutorials/)
- [Advanced Dashboard Design](https://www.youtube.com/grafana)

## 🎯 Próximos Passos

1. ✅ Explore todos os 4 dashboards
2. ✅ Execute `test_api_load.py` e observe métricas
3. ✅ Crie um painel personalizado
4. ✅ Configure um alerta
5. ✅ Exporte um dashboard e compartilhe

---

**Dúvidas?** Consulte `monitoring/grafana/README.md` ou abra um issue!

**Próximo tutorial:** Integração completa MLOps (treino → deploy → monitor)
