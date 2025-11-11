# Tutorial Docker – MLOps Churn

Este guia mostra, passo a passo, como conteinerizar e executar este projeto de Churn com Docker, cobrindo desde a criação da imagem até o uso em desenvolvimento e produção.

## Por que usar Docker neste projeto?

- **Reprodutibilidade**: mesma versão de Python, libs e SO para todos.
- **Portabilidade**: funciona em qualquer ambiente com Docker (Linux, macOS, Windows, CI/CD).
- **Isolamento**: dependências do projeto não conflitam com as do sistema/venv locais.
- **Simplicidade**: um único comando para construir e executar.
- **Escalabilidade e CI/CD**: imagens publicáveis em registries e orquestráveis (K8s, ECS).

## Pré‑requisitos

- Docker 20+ instalado
- Acesso à internet para baixar a imagem base Python e instalar pacotes

Verifique rapidamente:

```bash
docker --version
```

## Dockerfile proposto

Crie um arquivo `Dockerfile` na raiz do projeto com o seguinte conteúdo simplificado:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/treinamento.py"]
```

**Explicação linha a linha:**
- `FROM python:3.11-slim` – usa imagem Python otimizada e leve
- `WORKDIR /app` – define diretório de trabalho dentro do container
- `COPY requirements.txt .` – copia apenas as dependências primeiro (melhor cache)
- `RUN pip install` – instala as bibliotecas Python necessárias
- `COPY . .` – copia todo o código fonte do projeto
- `CMD` – comando padrão ao executar o container (treinamento)

## Passo a passo de uso

### 1) Criar o Dockerfile

Crie o arquivo `Dockerfile` na raiz do projeto com o conteúdo acima.

### 2) Construir a imagem

```bash
docker build -f Dockerfile.train -t mlops-churn .
```

Este comando cria uma imagem chamada `mlops-churn` com todo o ambiente configurado.

### 3) Executar treinamento

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn python src/treinamento.py
```

Explicação:
- `--rm` – remove o container após a execução
- `-v $(pwd)/models:/app/models` – monta a pasta local `models/` no container para salvar o modelo
- `-v $(pwd)/outputs:/app/outputs` – monta a pasta local `outputs/` para salvar as métricas

### 4) Executar predição

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn python src/predicao.py
```

### 5) Executar retreinamento

```bash
# Primeiro, atualizar dados de treino
docker run --rm \
  -v $(pwd)/data:/app/data \
  mlops-churn python src/retreinamento.py data/raw/dados_novos_1.csv

# Depois, retreinar o modelo
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn python src/treinamento.py
```

### 6) Acessar shell do container (debug)

```bash
docker run --rm -it -v $(pwd):/app mlops-churn bash
```

## O que é Docker Compose?

**Docker Compose** é uma ferramenta que permite definir e executar aplicações Docker multi-container através de um arquivo YAML (`docker-compose.yml`). Ele simplifica a orquestração de serviços, volumes e redes, sendo útil para ambientes com vários containers interdependentes (ex.: aplicação + banco de dados + redis). Para este projeto simples de MLOps, o uso de Docker Compose não é necessário no momento, mas pode ser útil no futuro se você quiser adicionar serviços complementares (API, dashboard, banco de dados, etc.).

## Boas práticas e dicas

- **Fixe versões** de dependências no `requirements.txt` para builds reprodutíveis.
- **Use volumes** para dados/modelos e não empacote dados sensíveis na imagem.
- **Publique imagens** em registries (Docker Hub, GHCR) com tags versionadas (`:v1.0.0`).
- **Integre com CI/CD** (GitHub Actions) para build/test/push automático.
- **Otimize tamanho**: use imagens `slim`, multi-stage builds e `.dockerignore`.

## Ganhos esperados

- ✅ Menos "funciona na minha máquina": ambientes consistentes.
- ✅ Onboarding rápido: um `docker build` + `docker run` e tudo funciona.
- ✅ Entrega contínua: publicar imagens versionadas facilita releases.
- ✅ Escalonamento: a mesma imagem roda em Kubernetes/ECS sem ajustes no código.

## Próximos passos (opcionais)

- Adicionar um workflow do GitHub Actions para build/push da imagem.
- Criar um `.dockerignore` para otimizar o build context.
- Expor os scripts como API REST usando FastAPI ou Flask.
- Adicionar health checks e monitoramento.

---

Com isso, o projeto está pronto para ser conteinerizado e executado de forma consistente via Docker!