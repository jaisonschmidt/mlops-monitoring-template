# MLOps - Modelo de Predição de Evasão de Clientes (Churn)

## 📋 Índice

- [Descrição do Projeto](#-descrição-do-projeto)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API de Predição de Churn](#-api-de-predição-de-churn)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Usar](#-como-usar)
  - [Instalação Local](#instalação)
  - [Treinamento do Modelo](#treinamento-do-modelo)
  - [Predição em Novos Dados](#predição-em-novos-dados)
- [Usando Docker](#-usando-docker)
  - [Treinar o Modelo com Docker](#1-treinar-o-modelo-com-docker)
  - [Fazer Predições com Docker](#2-fazer-predições-com-docker)
  - [Subir a API com Docker](#3-subir-a-api-com-docker)
  - [Exemplo Completo](#exemplo-completo-fluxo-de-trabalho-com-docker)
- [Retreinamento do Modelo](#-retreinamento-do-modelo)
- [Pipeline de ML](#-pipeline-de-ml)
- [Métricas de Avaliação](#-métricas-de-avaliação)
- [Contribuindo](#-contribuindo)

## 📋 Descrição do Projeto

Este projeto implementa um pipeline completo de Machine Learning para predição de evasão de clientes bancários (churn). O sistema utiliza Random Forest com balanceamento SMOTE e otimização de limiar de decisão para classificar o risco de evasão de clientes.

## 🎯 Objetivo

Desenvolver um modelo preditivo que identifica clientes com maior probabilidade de deixar o banco, permitindo ações preventivas de retenção.

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


## 🔧 Tecnologias Utilizadas

- **Python 3.x**
- **pandas** - Manipulação de dados
- **numpy** - Operações numéricas
- **scikit-learn** - Algoritmos de ML e pré-processamento
- **imbalanced-learn** - Tratamento de classes desbalanceadas (SMOTE)
- **joblib** - Serialização de modelos

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

##  Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

## 📝 Licença

Este projeto está sob licença MIT.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para aprendizado em MLOps**