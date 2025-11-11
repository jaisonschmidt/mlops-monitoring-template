# API de Predição de Churn

API REST desenvolvida com FastAPI para consultar predições de risco de churn de clientes.

## 🚀 Iniciando a API

### 1. Instalar dependências

```bash
pip install fastapi uvicorn pandas python-multipart
```

### 2. Iniciar o servidor

```bash
# Na raiz do projeto
uvicorn src.api_churn:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação Interativa

Acesse a documentação automática gerada pelo FastAPI:

- **Swagger UI (Recomendado)**: URL_API/docs
  - Interface interativa para testar todos os endpoints
  - Permite fazer requisições diretamente pelo navegador
  - Visualize schemas de request/response
  
- **ReDoc**: URL_API/redoc
  - Documentação em formato de referência
  - Ideal para leitura e consulta

> 💡 **Dica**: Use o Swagger UI (`/docs`) para testar a API de forma interativa sem precisar escrever código!

## 🔌 Endpoints Disponíveis

### 1. **GET /** - Informações da API

Retorna informações básicas sobre a API e seus endpoints.

**Exemplo:**
```bash
curl http://localhost:8000/
```

**Resposta:**
```json
{
  "api": "API de Predição de Churn",
  "versao": "1.0.0",
  "endpoints": {
    "health": "/health",
    "churn_por_id": "/churn/{id_cliente}",
    "todas_predicoes": "/churn/todas",
    "docs": "/docs",
    "redoc": "/redoc"
  }
}
```

---

### 2. **GET /health** - Health Check

Verifica o status da API e dos dados carregados.

**Exemplo:**
```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "OK",
  "total_predicoes": 2000
}
```

---

### 3. **GET /churn/{id_cliente}** - Obter Risco de Churn por ID

Retorna o risco de churn para um cliente específico.

**Parâmetros:**
- `id_cliente` (path): ID do cliente (RowNumber do dataset)

**Exemplo:**
```bash
curl https://refactored-space-telegram-5vw9jvgjwxqc4vv4-8000.app.github.dev/churn/15590146
```

**Resposta:**
```json
{
  "id_cliente": 15590146,
  "risco_churn": 0.6328,
  "previsao_churn": 1,
  "mensagem": "Risco de churn: ALTO (63.28%) - Risco alto "
}
```

**Classificação de Risco:**
- 🟢 **BAIXO**: < 30%
- 🟡 **MÉDIO**: 30% - 60%
- 🔴 **ALTO**: > 60%

---

### 4. **GET /churn/todas/predicoes** - Obter Todas as Predições

Retorna uma lista com todas as predições de churn.

**Parâmetros de Query:**
- `limite` (opcional): Número máximo de registros (padrão: 100)
- `risco_minimo` (opcional): Filtrar apenas clientes com risco >= este valor (0.0 a 1.0)

**Exemplos:**

```bash
# Obter primeiros 10 registros
curl "http://localhost:8000/churn/todas/predicoes?limite=10"

# Obter clientes com risco >= 70%
curl "http://localhost:8000/churn/todas/predicoes?risco_minimo=0.7&limite=50"
```

**Resposta:**
```json
{
  "total_registros": 10,
  "filtros": {
    "limite": 10,
    "risco_minimo": null
  },
  "predicoes": [
    {
      "id_cliente": 15590146,
      "risco_churn": 0.6328,
      "previsao_churn": 1,
      "classificacao": "Risco alto "
    },
    {
      "id_cliente": 15647890,
      "risco_churn": 0.1841,
      "previsao_churn": 0,
      "classificacao": "Risco muito alto"
    }
  ]
}
```

---

### 5. **POST /recarregar** - Recarregar Dados

Recarrega os dados do arquivo `predicoes.csv`. Útil quando o arquivo é atualizado.

**Exemplo:**
```bash
curl -X POST http://localhost:8000/recarregar
```

**Resposta:**
```json
{
  "status": "Dados recarregados com sucesso",
  "total_registros": 2000
}
```

## 🧪 Testando a API

### Usando cURL

```bash
# Health check
curl URL_API/health

# Consultar cliente específico
curl URL_API/churn/15590146

# Obter clientes de alto risco
curl "URL_API/churn/todas/predicoes?risco_minimo=0.8&limite=20"

## 🐳 Deploy com Docker

Se você quiser executar a API em um container Docker:

```dockerfile
# Adicione ao seu Dockerfile:
EXPOSE 8000
CMD ["uvicorn", "src.api_churn:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t api-churn .

# Run
docker run -p 8000:8000 api-churn
```

## 📊 Estrutura de Dados

A API lê os dados do arquivo `outputs/predicoes.csv`, que contém:

- `id_cliente`: ID único do cliente
- `preds`: Probabilidade de churn (0.0 a 1.0)
- `Classificação`: Classificação do risco (ex: "Risco alto", "Risco muito alto", etc.)

**Exemplo de dados:**
```csv
id_cliente,preds,Classificação
15590146,0.6327910500003517,Risco alto 
15647890,0.1840700490482832,Risco muito alto
15619029,0.1431372371050004,Risco muito alto
```

## ⚠️ Tratamento de Erros

A API retorna códigos HTTP apropriados:

- `200`: Sucesso
- `404`: Cliente não encontrado
- `400`: Parâmetros inválidos
- `503`: Serviço indisponível (dados não carregados)
- `500`: Erro interno do servidor

**Exemplo de erro:**
```json
{
  "detail": "Cliente com ID 99999 não encontrado"
}
```

## 🔧 Configuração

O arquivo de predições é carregado automaticamente ao iniciar a API. O caminho padrão é:
```
outputs/predicoes.csv
```

Para usar um arquivo diferente, modifique a variável `PREDICOES_PATH` em `src/api_churn.py`.

## 📝 Logs

A API gera logs informativos no console:

```
✓ Arquivo de predições carregado: 2000 registros
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🛠️ Desenvolvimento

A API usa o modo `--reload` do Uvicorn, que detecta automaticamente mudanças no código e reinicia o servidor.

Para desenvolvimento:
```bash
uvicorn src.api_churn:app --reload --log-level debug
```

---

**Desenvolvido com FastAPI** 🚀
