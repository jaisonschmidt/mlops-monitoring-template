#!/bin/bash

# Script para parar e limpar toda a stack de monitoramento

set -e

echo "=========================================="
echo "🛑 PARANDO STACK DE MONITORAMENTO"
echo "=========================================="

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Função para parar container
stop_container() {
    CONTAINER=$1
    if docker ps -q -f name=$CONTAINER &> /dev/null; then
        echo -e "${YELLOW}🛑 Parando $CONTAINER...${NC}"
        docker stop $CONTAINER &> /dev/null
        echo -e "${GREEN}✅ $CONTAINER parado${NC}"
    else
        echo -e "ℹ️  $CONTAINER não está rodando"
    fi
}

# Função para remover container
remove_container() {
    CONTAINER=$1
    if docker ps -a -q -f name=$CONTAINER &> /dev/null; then
        echo -e "${YELLOW}🗑️  Removendo $CONTAINER...${NC}"
        docker rm $CONTAINER &> /dev/null
        echo -e "${GREEN}✅ $CONTAINER removido${NC}"
    fi
}

echo ""
echo "Parando containers..."
stop_container "api-churn"
stop_container "prometheus"
stop_container "grafana"

echo ""
if [ "$1" == "--clean" ]; then
    echo "Removendo containers..."
    remove_container "api-churn"
    remove_container "prometheus"
    remove_container "grafana"
    
    echo ""
    echo "Removendo imagens (opcional)..."
    docker rmi -f api-churn prometheus-mlops grafana-mlops &> /dev/null || true
    echo -e "${GREEN}✅ Imagens removidas${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ STACK PARADA COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo "Para iniciar novamente:"
echo -e "   ${YELLOW}./scripts/start_monitoring.sh${NC}"
echo ""
echo "Para remover containers e imagens:"
echo -e "   ${YELLOW}./scripts/stop_monitoring.sh --clean${NC}"
echo "=========================================="
