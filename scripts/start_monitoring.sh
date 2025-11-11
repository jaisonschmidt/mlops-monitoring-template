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
echo -e "${BLUE}📦 Etapa 1: Limpando containers antigos${NC}"
cleanup_container "prometheus"
cleanup_container "grafana"
cleanup_container "api-churn"
echo -e "${GREEN}✅ Limpeza concluída${NC}"

# Build e start Prometheus
echo ""
echo -e "${BLUE}📦 Etapa 2: Iniciando Prometheus${NC}"
cd monitoring/prometheus
if [ ! -f "Dockerfile.prometheus" ]; then
    echo "❌ Dockerfile.prometheus não encontrado!"
    exit 1
fi

docker build -t prometheus-mlops -f Dockerfile.prometheus . --quiet
docker run -d \
    --name prometheus \
    -p 9090:9090 \
    --network host \
    prometheus-mlops

echo -e "${GREEN}✅ Prometheus iniciado em http://localhost:9090${NC}"

# Build e start Grafana
echo ""
echo -e "${BLUE}📊 Etapa 3: Iniciando Grafana${NC}"
cd ../grafana
if [ ! -f "Dockerfile.grafana" ]; then
    echo "❌ Dockerfile.grafana não encontrado!"
    exit 1
fi

docker build -t grafana-mlops -f Dockerfile.grafana . --quiet
docker run -d \
    --name grafana \
    -p 3000:3000 \
    --network host \
    grafana-mlops

echo -e "${GREEN}✅ Grafana iniciado em http://localhost:3000${NC}"
echo -e "   Credenciais: ${YELLOW}admin / admin${NC}"

# Build e start API
echo ""
echo -e "${BLUE}🚀 Etapa 4: Iniciando API de Churn${NC}"
cd "$PROJECT_ROOT"
if [ ! -f "Dockerfile.api" ]; then
    echo "❌ Dockerfile.api não encontrado!"
    exit 1
fi

docker build -t api-churn -f Dockerfile.api . --quiet
docker run -d \
    --name api-churn \
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
echo -e "${BLUE}🔍 Etapa 5: Verificando saúde dos containers${NC}"

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
echo -e "${BLUE}🎯 Etapa 6: Verificando coleta de métricas${NC}"
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
