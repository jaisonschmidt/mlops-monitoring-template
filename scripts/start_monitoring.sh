#!/bin/bash

# Script para iniciar toda a stack de monitoramento MLOps
# API + Prometheus + Grafana

set -e  # Parar em caso de erro

echo "=========================================="
echo "🚀 INICIANDO STACK DE MONITORAMENTO MLOPS"
echo "=========================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
NETWORK_NAME="mlops-monitoring"

# Função para verificar se um container está rodando
check_container() {
    if docker ps -q -f name=$1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Função para parar e remover container se existir
cleanup_container() {
    if docker ps -a -q -f name=$1 &> /dev/null; then
        echo -e "${YELLOW}⚠️  Container $1 já existe. Removendo...${NC}"
        docker rm -f $1 &> /dev/null || true
    fi
}

# Diretório raiz do projeto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}📦 Etapa 1: Preparando modelo e predições${NC}"

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 não encontrado. Tentando usar python...${NC}"
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Verificar se dependências estão instaladas
echo -e "${YELLOW}📚 Verificando dependências Python...${NC}"
$PYTHON_CMD -c "import loguru" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Instalando dependências...${NC}"
    $PYTHON_CMD -m pip install -q -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependências instaladas${NC}"
    else
        echo -e "${YELLOW}⚠️  Erro ao instalar dependências. Tentando continuar...${NC}"
    fi
else
    echo -e "${GREEN}✅ Dependências já instaladas${NC}"
fi

# Verificar se modelo existe
if [ ! -f "models/pipeline_modelo_treinado.joblib" ]; then
    echo -e "${YELLOW}📚 Modelo não encontrado. Treinando modelo...${NC}"
    $PYTHON_CMD src/treinamento.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Modelo treinado com sucesso${NC}"
    else
        echo -e "${YELLOW}⚠️  Erro ao treinar modelo, mas continuando...${NC}"
    fi
else
    echo -e "${GREEN}✅ Modelo já existe${NC}"
fi

# Verificar se predições existem
if [ ! -f "outputs/predicoes.csv" ]; then
    echo -e "${YELLOW}🔮 Predições não encontradas. Gerando predições...${NC}"
    $PYTHON_CMD src/predicao.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Predições geradas com sucesso${NC}"
    else
        echo -e "${YELLOW}⚠️  Erro ao gerar predições, mas continuando...${NC}"
    fi
else
    echo -e "${GREEN}✅ Predições já existem${NC}"
fi

echo ""
echo -e "${BLUE}📦 Etapa 2: Limpando containers antigos${NC}"
cleanup_container "prometheus"
cleanup_container "grafana"
cleanup_container "api-churn"
echo -e "${GREEN}✅ Limpeza concluída${NC}"

# Criar rede Docker dedicada (se não existir)
if ! docker network inspect "$NETWORK_NAME" &> /dev/null; then
    echo -e "${YELLOW}🌐 Criando rede Docker $NETWORK_NAME...${NC}"
    docker network create "$NETWORK_NAME" &> /dev/null
fi
echo -e "${GREEN}✅ Rede Docker pronta: $NETWORK_NAME${NC}"

# Build e start Prometheus
echo ""
echo -e "${BLUE}📦 Etapa 3: Iniciando Prometheus${NC}"
cd monitoring/prometheus
if [ ! -f "Dockerfile.prometheus" ]; then
    echo "❌ Dockerfile.prometheus não encontrado!"
    exit 1
fi

docker build -t prometheus-mlops -f Dockerfile.prometheus . --quiet
docker run -d \
    --name prometheus \
    --network "$NETWORK_NAME" \
    -p 9090:9090 \
    prometheus-mlops

echo -e "${GREEN}✅ Prometheus iniciado em http://localhost:9090${NC}"

# Build e start Grafana
echo ""
echo -e "${BLUE}📊 Etapa 4: Iniciando Grafana${NC}"
cd ../grafana
if [ ! -f "Dockerfile.grafana" ]; then
    echo "❌ Dockerfile.grafana não encontrado!"
    exit 1
fi

docker build -t grafana-mlops -f Dockerfile.grafana . --quiet
docker run -d \
    --name grafana \
    --network "$NETWORK_NAME" \
    -p 3000:3000 \
    grafana-mlops

echo -e "${GREEN}✅ Grafana iniciado em http://localhost:3000${NC}"
echo -e "   Credenciais: ${YELLOW}admin / admin${NC}"

# Build e start API
echo ""
echo -e "${BLUE}🚀 Etapa 5: Iniciando API de Churn${NC}"
cd "$PROJECT_ROOT"
if [ ! -f "Dockerfile.api" ]; then
    echo "❌ Dockerfile.api não encontrado!"
    exit 1
fi

docker build -t api-churn -f Dockerfile.api . --quiet
docker run -d \
    --name api-churn \
    --network "$NETWORK_NAME" \
    -p 8000:8000 \
    api-churn

echo -e "${GREEN}✅ API iniciada em http://localhost:8000${NC}"
echo -e "   Documentação: ${BLUE}http://localhost:8000/docs${NC}"

# Aguardar containers iniciarem
echo ""
echo -e "${YELLOW}⏳ Aguardando containers iniciarem (10s)...${NC}"
sleep 10

# Verificar saúde dos containers
echo ""
echo -e "${BLUE}🔍 Etapa 6: Verificando saúde dos containers${NC}"

# Check Prometheus
if curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo -e "${GREEN}✅ Prometheus: healthy${NC}"
else
    echo -e "❌ Prometheus: não está respondendo"
fi

# Check Grafana
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo -e "${GREEN}✅ Grafana: healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Grafana: ainda inicializando...${NC}"
fi

# Check API
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ API: healthy${NC}"
else
    echo -e "❌ API: não está respondendo"
fi

# Verificar se Prometheus está coletando métricas da API
echo ""
echo -e "${BLUE}🎯 Etapa 7: Verificando coleta de métricas${NC}"
sleep 5  # Aguardar primeiro scrape

TARGETS=$(curl -s http://localhost:9090/api/v1/targets | grep -o '"health":"up"' | wc -l)
if [ "$TARGETS" -gt 0 ]; then
    echo -e "${GREEN}✅ Prometheus coletando métricas da API${NC}"
else
    echo -e "${YELLOW}⚠️  Aguarde alguns segundos para primeiro scrape...${NC}"
fi

# Resumo final
echo ""
echo "=========================================="
echo -e "${GREEN}✅ STACK INICIADA COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo "📊 URLs de acesso:"
echo -e "   • API:        ${BLUE}http://localhost:8000${NC}"
echo -e "   • API Docs:   ${BLUE}http://localhost:8000/docs${NC}"
echo -e "   • Metrics:    ${BLUE}http://localhost:8000/metrics${NC}"
echo -e "   • Prometheus: ${BLUE}http://localhost:9090${NC}"
echo -e "   • Grafana:    ${BLUE}http://localhost:3000${NC} (admin/admin)"
echo ""
echo "🎯 Dashboards do Grafana:"
echo "   1. API Health & Performance"
echo "   2. ML Model Metrics"
echo "   3. Business Intelligence - Churn"
echo "   4. System Overview"
echo ""
echo "🧪 Para testar a API:"
echo -e "   ${YELLOW}python scripts/test_api_load.py${NC}"
echo ""
echo "🛑 Para parar tudo:"
echo -e "   ${YELLOW}./scripts/stop_monitoring.sh${NC}"
echo ""
echo "📋 Ver logs:"
echo -e "   ${YELLOW}docker logs -f prometheus${NC}"
echo -e "   ${YELLOW}docker logs -f grafana${NC}"
echo -e "   ${YELLOW}docker logs -f api-churn${NC}"
echo "=========================================="
