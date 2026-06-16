# MLOps - Modelo de Predição de Evasão de Clientes (Churn) �

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-2.47-orange.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-10.2-red.svg)](https://grafana.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

**Sistema completo de MLOps** com monitoramento em tempo real usando **Prometheus** e **Grafana**!

## 📋 Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Recursos de Monitoramento](#-recursos-de-monitoramento)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🚀 Quick Start](#-quick-start)
- [📊 Monitoramento](#-monitoramento)
- [🌐 API de Predição](#-api-de-predição)
- [🔧 Tecnologias](#-tecnologias)
- [📚 Tutoriais](#-tutoriais)
- [🐳 Docker](#-docker)
- [📈 Pipeline de ML](#-pipeline-de-ml)
- [🤝 Contribuindo](#-contribuindo)

## 🎯 Sobre o Projeto

Este projeto implementa um **pipeline completo de MLOps** para predição de evasão de clientes bancários (churn). O sistema utiliza:

- 🤖 **Random Forest** com balanceamento SMOTE
- 📡 **API REST** com FastAPI
- 📊 **Monitoramento** com Prometheus + Grafana
- 📝 **Logging estruturado** com Loguru
- 🐳 **Containerização** com Docker

**Ideal para aprendizado de MLOps em ambiente acadêmico!**

## ✨ Recursos de Monitoramento

### 📊 Stack de Observabilidade Completa

- **📝 Loguru**: Logging estruturado com rotação automática
- **📈 Prometheus**: Coleta e armazenamento de métricas
- **📊 Grafana**: 4 dashboards profissionais pré-configurados
- **🔔 Alertas**: 5 alertas automáticos para problemas críticos

### 📊 Dashboards Disponíveis

| Dashboard | Descrição | Usuário |
|-----------|-----------|---------|
| 🎯 **System Overview** | Visão executiva geral | CEO/Gestores |
| 🚀 **API Health** | Performance da API | DevOps/SRE |
| 🤖 **ML Metrics** | Qualidade do modelo | Data Scientists |
| 💼 **Business Churn** | KPIs de negócio | Analistas |

### 📏 Métricas Coletadas

**Infraestrutura (17 métricas)**
- Taxa de requisições, latência, erros
- Uptime, requests ativas
- Tempo de resposta P50/P95/P99

**Machine Learning (6 métricas)**
- F2-Score, AUC-ROC, Precision, Recall
- Duração de treinamento
- Total de amostras

**Negócio (5 métricas)**
- Clientes em alto/médio/baixo risco
- Score médio de churn
- Distribuição de predições

## 🚀 Quick Start

### Opção 1: Iniciar Tudo com 1 Comando 🎯

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/mlops-monitoring-prep.git
cd mlops-monitoring-prep

# Iniciar stack completa (API + Prometheus + Grafana)
./scripts/start_monitoring.sh
```

**Acessar:**
- 🌐 **API**: http://localhost:8000/docs
- 📊 **Prometheus**: http://localhost:9090
- 📈 **Grafana**: http://localhost:3000 (admin/admin)

> 📘 **Entenda o fluxo completo do comando (visão executiva + didática):**
> [FLUXO_START_MONITORING.md](tutorial/FLUXO_START_MONITORING.md)

### Opção 2: Passo a Passo Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Treinar modelo
python src/treinamento.py

# 4. Fazer predições
python src/predicao.py

# 5. Subir API
uvicorn src.api_churn:app --host 0.0.0.0 --port 8000

# 6. Testar com carga
python scripts/test_api_load.py
```

## 📊 Monitoramento

### Arquitetura de Monitoramento

```
┌─────────────┐
│ Treinamento │──┐
│  Predição   │  │ Loguru
│ Retreinamento│  │ (logs/)
└─────────────┘  │
                 ▼
┌─────────────┐  ┌──────────┐  ┌─────────┐
│  API Churn  │─→│Prometheus│←─│ Grafana │
│   :8000     │  │  :9090   │  │  :3000  │
└─────────────┘  └──────────┘  └─────────┘
    /metrics       scrape        dashboards
```

### Ver Dashboards

1. **Iniciar stack**: `./scripts/start_monitoring.sh`
2. **Acessar Grafana**: http://localhost:3000
3. **Login**: admin / admin
4. **Selecionar** dashboard desejado
5. **Gerar métricas**: `python scripts/test_api_load.py`

### Consultar Métricas

```bash
# Diretamente no Prometheus
curl http://localhost:9090/api/v1/query?query=model_f2_score

# Endpoint de métricas da API
curl http://localhost:8000/metrics

# Exportar para arquivo
python scripts/export_metrics.py
```

### Alertas Configurados

| Alerta | Condição | Severidade |
|--------|----------|------------|
| 🔴 **APIDown** | API offline > 1min | Critical |
| 🟠 **HighErrorRate** | Erros > 5% | Warning |
| 🟡 **HighLatency** | P95 > 500ms | Warning |
| 🟠 **ModelDegraded** | F2-Score < 0.7 | Warning |
| 🟡 **HighChurnRisk** | Alto risco > 1000 | Info |

### Parar Monitoramento

```bash
# Parar todos containers
./scripts/stop_monitoring.sh

# Parar e limpar tudo
./scripts/stop_monitoring.sh --clean
```

## 📁 Estrutura do Projeto

```
mlops-docker-template/
├── data/                           # Dados do projeto
│   ├── raw/                        # Dados brutos
│   │   ├── dados_treino.csv        # Dataset inicial de treinamento
│   │   ├── dados_novos_1.csv       # Novos dados para predição/retreino
│   │   └── dados_novos_2.csv       # Novos dados para predição/retreino
│   └── docs/                       # Documentação dos dados
│       └── bank_churn_dict.csv     # Dicionário de dados
│
├── src/                            # Código fonte
│   ├── treinamento.py              # Script de treinamento do modelo
│   ├── predicao.py                 # Script de predição
│   └── retreinamento.py            # Script auxiliar de retreinamento
│
├── models/                         # Modelos treinados
│   └── pipeline_modelo_treinado.joblib
│
├── outputs/                        # Resultados e métricas
│   ├── metricas_desempenho_evasao.csv
│   └── predicoes.csv
│
├── src/                            # Código fonte
│   ├── api_churn.py                # API FastAPI para consulta de predições
│   ├── treinamento.py              # Script de treinamento do modelo
│   ├── predicao.py                 # Script de predição
│   └── retreinamento.py            # Script auxiliar de retreinamento
│
├── Dockerfile.api                  # Dockerfile para a API
├── docker-compose.yml              # Configuração Docker Compose
├── docker-api.sh                   # Script auxiliar para gerenciar Docker
├── .dockerignore                   # Arquivos ignorados no build Docker
├── .gitignore                      # Arquivos ignorados pelo Git
├── requirements.txt                # Dependências do projeto
├── API_CHURN_README.md             # Documentação da API
├── DOCKER_API.md                   # Documentação Docker
├── README.md                       # Este arquivo
└── README.txt                      # Documentação original
```

## 🌐 API de Predição de Churn

Este projeto inclui uma API REST desenvolvida com FastAPI para consultar predições de risco de churn.

**Documentação completa:** [API_CHURN_README.md](API_CHURN_README.md)

### Iniciar a API localmente

```bash
uvicorn src.api_churn:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints principais

- `GET /` - Informações da API
- `GET /health` - Status e health check
- `GET /churn/{id_cliente}` - Consultar risco de churn por ID
- `GET /churn/todas/predicoes` - Listar todas as predições
- `GET /docs` - Documentação interativa (Swagger)


## � Tutoriais

### Guias Completos para Alunos

| Tutorial | Descrição | Tempo estimado |
|----------|-----------|----------------|
| 📊 [**PROMETHEUS.md**](tutorial/PROMETHEUS.md) | Como usar Prometheus, PromQL, alertas | 45 min |
| 📈 [**GRAFANA.md**](tutorial/GRAFANA.md) | Dashboards, painéis, visualizações | 60 min |
| 🐳 [**DOCKER_API.md**](tutorial/DOCKER_API.md) | Containers, builds, deploy | 30 min |
| 🌐 [**API_CHURN_README.md**](tutorial/API_CHURN_README.md) | Endpoints, FastAPI, testes | 30 min |
| 🚀 [**FLUXO_START_MONITORING.md**](tutorial/FLUXO_START_MONITORING.md) | Fluxo completo do startup da stack de monitoramento | 20 min |

### Planejamento de Implementação

📋 **[PLANEJAMENTO_MONITORAMENTO.md](monitoring/PLANEJAMENTO_MONITORAMENTO.md)**
- Visão geral de 6 passos de implementação
- Métricas definidas e categorizadas
- Arquitetura de monitoramento
- Timeline de desenvolvimento

### Exercícios Práticos

Todos os tutoriais incluem:
- ✅ Conceitos teóricos explicados
- ✅ Exemplos práticos passo a passo
- ✅ Exercícios com soluções
- ✅ Troubleshooting de problemas comuns

## 🔧 Tecnologias

### Machine Learning
- **Python 3.x**
- **pandas** - Manipulação de dados
- **numpy** - Operações numéricas
- **scikit-learn** - Algoritmos de ML e pré-processamento
- **imbalanced-learn** - Tratamento de classes desbalanceadas (SMOTE)
- **joblib** - Serialização de modelos

### API & Web
- **FastAPI** - Framework REST moderno e rápido
- **uvicorn** - Servidor ASGI de alta performance
- **pydantic** - Validação de dados com type hints

### Monitoramento & Observabilidade
- **Loguru 0.7.0+** - Logging estruturado com cores e rotação
- **Prometheus 2.47+** - Coleta e armazenamento de métricas
  - `prometheus-client` - Cliente Python
  - `prometheus-fastapi-instrumentator` - Instrumentação automática
- **Grafana 10.2+** - Visualização e dashboards
  - Auto-provisioning de datasources
  - 4 dashboards pré-configurados

### Infrastructure
- **Docker** - Containerização
- **Docker Compose** - Orquestração (opcional)
- **Git** - Controle de versão

## 📊 Variáveis do Dataset

Consulte o arquivo `data/docs/bank_churn_dict.csv` para descrição detalhada das variáveis.

**Principais features:**
- Variáveis numéricas: `idade`, `saldo_conta`, `salario_estimado`, `escore_credito`
- Variáveis categóricas: `pais`, `genero`, `cartao_credito`
- Variáveis ordinais: `anos_cliente`, `numero_produtos`
- Target: `saiu` (0 = não saiu, 1 = saiu)

## 🚀 Como Usar

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/jaisonschmidt/mlops-docker-template.git
cd mlops-docker-template
```

2. Crie e ative um ambiente virtual Python:

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

> **Nota:** Para desativar o ambiente virtual, use o comando `deactivate`

### Treinamento do Modelo

Execute o script de treinamento para criar o modelo inicial:

```bash
python src/treinamento.py
```

**Entradas:**
- `data/raw/dados_treino.csv`

**Saídas:**
- `models/pipeline_modelo_treinado.joblib` - Pipeline completo do modelo
- `outputs/metricas_desempenho_evasao.csv` - Métricas de desempenho

### Predição em Novos Dados

Execute o script de predição para classificar novos clientes:

```bash
python src/predicao.py
```

**Entradas:**
- `data/raw/dados_novos_1.csv` (ou `dados_novos_2.csv`)
- `models/pipeline_modelo_treinado.joblib`

**Saídas:**
- `outputs/predicoes.csv` - Probabilidades e classificação de risco

**Classificação de Risco:**
- 🟢 **Risco muito alto**: Probabilidade > 90%
- 🟡 **Risco alto**: Probabilidade > 70%
- 🟠 **Risco moderado**: Probabilidade > 50%
- 🔴 **Risco baixo**: Probabilidade < 50%

## 🐳 Usando Docker

**Documentação Docker:** [DOCKER_API.md](DOCKER_API.md)

> **Nota para usuários Windows:**
> - No **PowerShell**, use `${PWD}` ao invés de `$(pwd)`
> - No **CMD**, use `%cd%` ao invés de `$(pwd)`
> 
> Exemplo PowerShell: `docker run --rm -v ${PWD}/data:/app/data ...`

### 1. Treinar o Modelo com Docker

Para treinar o modelo usando Docker, execute os seguintes comandos:

```bash
# Build da imagem Docker
docker build -t mlops-churn:latest .

# Executar o treinamento
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/treinamento.py
```

**Explicação dos parâmetros:**
- `--rm` - Remove o container automaticamente após a execução
- `-v $(pwd)/data:/app/data` - Monta o diretório de dados
- `-v $(pwd)/models:/app/models` - Monta o diretório de modelos (para salvar o modelo treinado)
- `-v $(pwd)/outputs:/app/outputs` - Monta o diretório de saídas (para salvar métricas)

**Arquivos gerados:**
- `models/pipeline_modelo_treinado.joblib` - Modelo treinado
- `outputs/metricas_desempenho_evasao.csv` - Métricas de desempenho

### 2. Fazer Predições com Docker

Para executar predições em novos dados usando Docker:

```bash
# Executar predições
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/predicao.py
```

**Pré-requisitos:**
- Modelo já treinado em `models/pipeline_modelo_treinado.joblib`
- Dados novos em `data/raw/dados_novos_1.csv` (ou `dados_novos_2.csv`)

**Arquivo gerado:**
- `outputs/predicoes.csv` - Predições com probabilidades e classificação de risco

### 3. Subir a API com Docker

Para executar a API de consulta de predições com Docker:

```bash
# Build da imagem da API
docker build -f Dockerfile.api -t api-churn:latest .

# Executar a API
docker run -d \
  -p 8000:8000 \
  --name api-churn-container \
  -v $(pwd)/outputs:/app/outputs:ro \
  --restart unless-stopped \
  api-churn:latest
```

**Explicação dos parâmetros:**
- `-d` - Executa em background (modo daemon)
- `-p 8000:8000` - Mapeia a porta 8000 do container para a porta 8000 do host
- `--name api-churn-container` - Define o nome do container
- `-v $(pwd)/outputs:/app/outputs:ro` - Monta o diretório de predições (read-only)
- `--restart unless-stopped` - Reinicia automaticamente o container se ele parar

**Acessar a API:**
- **Base URL**: http://localhost:8000
- **Documentação interativa (Swagger)**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

**Gerenciar o container da API:**

```bash
# Ver logs
docker logs -f api-churn-container

# Parar a API
docker stop api-churn-container

# Iniciar a API novamente
docker start api-churn-container

# Remover o container
docker rm -f api-churn-container
```

**Testar a API:**

```bash
# Health check
curl http://localhost:8000/health

# Consultar risco de churn de um cliente
curl http://localhost:8000/churn/15590146

# Listar clientes com alto risco
curl "http://localhost:8000/churn/todas/predicoes?risco_minimo=0.8&limite=10"
```

### Script Auxiliar para Docker

Para facilitar o gerenciamento da API com Docker, use o script auxiliar:

```bash
# Tornar o script executável (apenas uma vez)
chmod +x docker-api.sh

# Build da imagem
./docker-api.sh build

# Iniciar a API
./docker-api.sh run

# Ver status
./docker-api.sh status

# Ver logs
./docker-api.sh logs

# Testar a API
./docker-api.sh test

# Parar a API
./docker-api.sh stop

# Rebuild completo
./docker-api.sh rebuild
```

📖 **Documentação completa:**
- **API**: [API_CHURN_README.md](API_CHURN_README.md)
- **Docker**: [DOCKER_API.md](DOCKER_API.md)

### Exemplo Completo: Fluxo de Trabalho com Docker

Aqui está um exemplo completo do fluxo de trabalho usando Docker:

```bash
# 1. Build da imagem principal
docker build -t mlops-churn:latest .

# 2. Treinar o modelo
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/treinamento.py

# 3. Fazer predições
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/predicao.py

# 4. Build da imagem da API
docker build -f Dockerfile.api -t api-churn:latest .

# 5. Subir a API
docker run -d \
  -p 8000:8000 \
  --name api-churn-container \
  -v $(pwd)/outputs:/app/outputs:ro \
  api-churn:latest

# 6. Testar a API
curl http://localhost:8000/health
curl http://localhost:8000/churn/15590146

# 7. Ver logs da API
docker logs -f api-churn-container

# 8. Parar e remover a API quando terminar
docker stop api-churn-container
docker rm api-churn-container
```

### Resumo de Comandos Docker

| Tarefa | Comando |
|--------|---------|
| **Build imagem principal** | `docker build -t mlops-churn:latest .` |
| **Treinar modelo** | `docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models -v $(pwd)/outputs:/app/outputs mlops-churn:latest python src/treinamento.py` |
| **Fazer predições** | `docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models -v $(pwd)/outputs:/app/outputs mlops-churn:latest python src/predicao.py` |
| **Build imagem API** | `docker build -f Dockerfile.api -t api-churn:latest .` |
| **Subir API** | `docker run -d -p 8000:8000 --name api-churn-container -v $(pwd)/outputs:/app/outputs:ro api-churn:latest` |
| **Ver logs da API** | `docker logs -f api-churn-container` |
| **Parar API** | `docker stop api-churn-container` |
| **Remover API** | `docker rm -f api-churn-container` |

## 🔄 Retreinamento do Modelo

### Retreinamento com Docker

Para retreinar o modelo com novos dados usando Docker:

```bash
# 1. Executar o script de retreinamento (combina datasets)
docker run --rm \
  -v $(pwd)/data:/app/data \
  mlops-churn:latest python src/retreinamento.py

# 2. Treinar o modelo com os dados combinados
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/treinamento.py
```

### Retreinamento Local

Para retreinar o modelo com novos dados localmente:

### Opção 1: Usando o script de retreinamento (Recomendado)

```bash
# Retreinar com dados_novos_1.csv
python src/retreinamento.py

# Ou especificar outro arquivo
python src/retreinamento.py data/raw/dados_novos_2.csv

# Depois executar o treinamento
python src/treinamento.py
```

### Opção 2: Retreino manual

```bash
# No terminal Python ou script
import pandas as pd

# Combinar datasets
dados_treino = pd.read_csv("data/raw/dados_treino.csv")
dados_novos = pd.read_csv("data/raw/dados_novos_1.csv")
dados_combinados = pd.concat([dados_treino, dados_novos], ignore_index=True)
dados_combinados.to_csv("data/raw/dados_treino.csv", index=False)

# Executar treinamento
```

```bash
python src/treinamento.py
```

### Opção 3: Retreino incremental (em lotes)

É possível fazer retreino em lotes menores (ex: 32 em 32) para simular aprendizado contínuo.

## 📈 Pipeline de ML

O modelo implementa o seguinte pipeline:

1. **Imputação de valores ausentes**
   - KNN Imputer para variáveis numéricas
   - Most Frequent para categóricas

2. **Transformações**
   - Power Transform + Standard Scaler (numéricas)
   - One-Hot Encoding (categóricas)
   - Target Encoding (ordinais)
   - Polynomial Features (interações)

3. **Balanceamento**
   - SMOTE para classes desbalanceadas

4. **Modelo**
   - Random Forest Classifier (1000 árvores)
   - Tuned Threshold com otimização F2-score

## 📊 Métricas de Avaliação

O modelo é avaliado usando:
- **F1-Score** e **F2-Score** (weighted)
- **Precisão** e **Recall** (weighted)
- **AUC-ROC**

Classificação de desempenho:
- ✅ Excelente: > 0.90
- 👍 Bom: > 0.80
- ⚠️ Aceitável: > 0.70
- ⚡ Fraco: > 0.60
- ❌ Ruim: < 0.60

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

## 👨‍🏫 Para Instrutores

### Estrutura Pedagógica

Este projeto foi desenvolvido para ensino de MLOps seguindo 6 passos incrementais:

| Passo | Tópico | Duração | Objetivos |
|-------|--------|---------|-----------|
| **1** | Preparação do Ambiente | 30min | Dependencies, configs |
| **2** | Implementação do Loguru | 45min | Structured logging |
| **3** | Implementação do Prometheus | 60min | Metrics collection |
| **4** | Implementação do Grafana | 90min | Dashboards, visualization |
| **5** | Instrumentação ML | 45min | Model metrics |
| **6** | Integração e Testes | 60min | E2E testing |

**Total**: ~5.5 horas (pode ser dividido em 3 aulas de 2h)

### Commits Organizados

Cada passo possui um commit dedicado para facilitar o ensino incremental:

```bash
git log --oneline --graph
# * d0d92e3 feat: PASSO 6 - Integração, testes e documentação
# * e808d6b feat: PASSO 5 - Instrumentação de métricas ML
# * 493064b feat: PASSO 4 - Implementação do Grafana
# * d4a4655 feat: PASSO 3 - Implementação do Prometheus
# * 231314c feat: PASSO 2 - Implementação do Loguru
# * f8ba800 feat: PASSO 1 - Preparação do ambiente
```

### Sugestões de Aula

**Aula 1 - Fundamentos (2h)**
- Passos 1 e 2: Logging estruturado
- Discussão: Por que monitoramento é importante?

**Aula 2 - Métricas (2h)**  
- Passos 3 e 4: Prometheus e Grafana
- Prática: Criar queries PromQL

**Aula 3 - Integração (2h)**
- Passos 5 e 6: Instrumentação e testes
- Projeto: Adicionar nova métrica personalizada

### Exercícios Propostos

1. **Básico**: Adicionar nova métrica de "tempo de carregamento de modelo"
2. **Intermediário**: Criar dashboard personalizado com métricas específicas
3. **Avançado**: Implementar alerta customizado com notificação Slack
4. **Projeto**: Integrar com MLflow para tracking de experimentos

## 📊 Histórico de Versões

- **v1.0** - Sistema MLOps completo com monitoramento
- **v0.3** - Adicionado Grafana e dashboards
- **v0.2** - Adicionado Prometheus e métricas
- **v0.1** - API básica de churn

## 📝 Licença

Este projeto está sob licença MIT.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para ensino de MLOps**

> 💡 **Dica para alunos**: Comece pelos tutoriais em `tutorial/` antes de mexer no código!