# Dockerfile para Treinamento e Predição de Churn
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ src/

# Criar diretórios necessários
RUN mkdir -p data/raw data/docs models outputs

# Variável de ambiente para evitar buffer no Python
ENV PYTHONUNBUFFERED=1

# Comando padrão (pode ser sobrescrito)
CMD ["python", "src/treinamento.py"]

