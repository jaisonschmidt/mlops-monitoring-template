# Docker - API de Predição de Churn

Este guia explica como criar e executar a API de Predição de Churn usando Docker.

## 📦 Arquivos Docker

- **Dockerfile.api** - Dockerfile otimizado para a API
- **.dockerignore** - Arquivos a serem ignorados no build

## 🚀 Build da Imagem

### Construir a imagem

```bash
docker build -f Dockerfile.api -t api-churn:latest .
```

**Parâmetros:**
- `-f Dockerfile.api` - Especifica qual Dockerfile usar
- `-t api-churn:latest` - Nome e tag da imagem
- `.` - Contexto de build (diretório atual)

### Verificar imagem criada

```bash
docker images | grep api-churn
```

## 🏃 Executar o Container

### Modo simples

```bash
docker run -p 8000:8000 api-churn:latest
```

### Modo detached (em background)

```bash
docker run -d -p 8000:8000 --name api-churn-container api-churn:latest
```

**Parâmetros:**
- `-d` - Executa em background (detached)
- `-p 8000:8000` - Mapeia porta do host:container
- `--name api-churn-container` - Nome do container

### Com variáveis de ambiente

```bash
docker run -d \
  -p 8000:8000 \
  --name api-churn-container \
  -e PYTHONUNBUFFERED=1 \
  api-churn:latest
```

### Com volume (para atualizar predições sem rebuild)

```bash
docker run -d \
  -p 8000:8000 \
  --name api-churn-container \
  -v $(pwd)/outputs:/app/outputs \
  api-churn:latest
```

## 📊 Gerenciar Container

### Ver containers rodando

```bash
docker ps
```

### Ver logs do container

```bash
docker logs api-churn-container
```

### Logs em tempo real

```bash
docker logs -f api-churn-container
```

### Parar o container

```bash
docker stop api-churn-container
```

### Iniciar container parado

```bash
docker start api-churn-container
```

### Remover container

```bash
docker rm api-churn-container
```

### Remover container (forçado, se estiver rodando)

```bash
docker rm -f api-churn-container
```

## 🧪 Testar a API

Após iniciar o container, teste os endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Informações da API
curl http://localhost:8000/

# Consultar cliente
curl http://localhost:8000/churn/15590146

# Documentação interativa
# Abra no navegador: http://localhost:8000/docs
```

## 🐳 Docker Compose (Opcional)

Para facilitar ainda mais, você pode criar um `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api-churn:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: api-churn-container
    ports:
      - "8000:8000"
    volumes:
      - ./outputs:/app/outputs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

**Comandos com Docker Compose:**

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Rebuild e iniciar
docker-compose up -d --build
```

## 🚢 Publicar Imagem (Opcional)

### Docker Hub

```bash
# Login
docker login

# Tag da imagem
docker tag api-churn:latest seu-usuario/api-churn:latest

# Push
docker push seu-usuario/api-churn:latest
```

### GitHub Container Registry

```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag
docker tag api-churn:latest ghcr.io/seu-usuario/api-churn:latest

# Push
docker push ghcr.io/seu-usuario/api-churn:latest
```

## 📏 Tamanho da Imagem

Verificar tamanho da imagem:

```bash
docker images api-churn:latest
```

## 🔧 Troubleshooting

### Container não inicia

```bash
# Ver logs de erro
docker logs api-churn-container

# Executar em modo interativo para debug
docker run -it --rm -p 8000:8000 api-churn:latest /bin/bash
```

### Porta já em uso

```bash
# Verificar o que está usando a porta 8000
lsof -i :8000

# Ou usar outra porta
docker run -p 8080:8000 api-churn:latest
```

### Rebuild limpo (sem cache)

```bash
docker build --no-cache -f Dockerfile.api -t api-churn:latest .
```

### Remover imagens antigas

```bash
# Remover imagens não utilizadas
docker image prune

# Remover tudo que não está em uso
docker system prune -a
```

## 🎯 Exemplo Completo

```bash
# 1. Build da imagem
docker build -f Dockerfile.api -t api-churn:latest .

# 2. Executar container
docker run -d \
  -p 8000:8000 \
  --name api-churn-container \
  -v $(pwd)/outputs:/app/outputs \
  --restart unless-stopped \
  api-churn:latest

# 3. Verificar se está rodando
docker ps

# 4. Ver logs
docker logs -f api-churn-container

# 5. Testar API
curl http://localhost:8000/health

# 6. Acessar documentação
# Abra: http://localhost:8000/docs
```

## 📝 Notas

- A imagem usa Python 3.11 slim para menor tamanho
- O health check verifica automaticamente se a API está respondendo
- Use volumes para atualizar o arquivo de predições sem rebuild
- A opção `--restart unless-stopped` garante que o container reinicie automaticamente

---

**Desenvolvido com Docker + FastAPI** 🐳🚀
