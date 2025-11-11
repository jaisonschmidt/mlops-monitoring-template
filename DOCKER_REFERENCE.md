# 🐳 Referência Rápida - Docker Commands

## Comandos Essenciais

### 1️⃣ Treinar Modelo
```bash
docker build -t mlops-churn:latest .
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/treinamento.py
```

### 2️⃣ Fazer Predições
```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/predicao.py
```

### 3️⃣ Subir API
```bash
docker build -f Dockerfile.api -t api-churn:latest .
docker run -d -p 8000:8000 --name api-churn-container \
  -v $(pwd)/outputs:/app/outputs:ro \
  api-churn:latest
```

### 4️⃣ Gerenciar API
```bash
# Ver logs
docker logs -f api-churn-container

# Parar
docker stop api-churn-container

# Iniciar novamente
docker start api-churn-container

# Remover
docker rm -f api-churn-container
```

## 💻 Comandos para Windows

### PowerShell
Substitua `$(pwd)` por `${PWD}`:
```powershell
docker run --rm -v ${PWD}/data:/app/data ...
```

### CMD
Substitua `$(pwd)` por `%cd%`:
```cmd
docker run --rm -v %cd%/data:/app/data ...
```

## 🚀 Fluxo Completo

```bash
# Build
docker build -t mlops-churn:latest .

# Treinar
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/treinamento.py

# Predizer
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  mlops-churn:latest python src/predicao.py

# API
docker build -f Dockerfile.api -t api-churn:latest .
docker run -d -p 8000:8000 --name api-churn-container \
  -v $(pwd)/outputs:/app/outputs:ro api-churn:latest

# Testar
curl http://localhost:8000/health
curl http://localhost:8000/churn/15590146
```

## 📚 Documentação

- README geral: [README.md](README.md)
- API: [API_CHURN_README.md](API_CHURN_README.md)  
- Docker detalhado: [DOCKER_API.md](DOCKER_API.md)
