#!/bin/bash

# Script para iniciar toda a stack de monitoramento MLOps
# API + Prometheus + Grafana

set -e  # Parar em caso de erro

# Função para timestamp
log_time() {
    echo "[$(date +'%H:%M:%S')]"
}

echo "=========================================="
echo "🚀 INICIANDO STACK DE MONITORAMENTO MLOPS"
echo "$(log_time)"
echo "=========================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
NETWORK_NAME="mlops-monitoring"

# Detecção de ambiente: GitHub Codespaces vs local
# No Codespaces, as portas são expostas via HTTPS em domínios específicos.
# Exemplo: https://${CODESPACE_NAME}-8000.app.github.dev
get_base_url() {
    local port="$1"
    if [ -n "${CODESPACE_NAME:-}" ]; then
        local domain="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"
        echo "https://${CODESPACE_NAME}-${port}.${domain}"
    else
        echo "http://localhost:${port}"
    fi
}

API_BASE_URL="$(get_base_url 8000)"
PROMETHEUS_BASE_URL="$(get_base_url 9090)"
GRAFANA_BASE_URL="$(get_base_url 3000)"

# URLs de health/metrics para validação externa (Codespaces) ou local.
PROMETHEUS_HEALTH_URL="${PROMETHEUS_BASE_URL}/-/healthy"
GRAFANA_HEALTH_URL="${GRAFANA_BASE_URL}/api/health"
API_HEALTH_URL="${API_BASE_URL}/health"
API_METRICS_URL="${API_BASE_URL}/metrics"

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

wait_for_http_ok() {
    local service_name="$1"
    local url="$2"
    local retries="${3:-20}"
    local delay_seconds="${4:-3}"

    for ((i=1; i<=retries; i++)); do
        if curl -fsS "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ ${service_name}: healthy${NC}"
            return 0
        fi
        echo -e "${YELLOW}⏳ ${service_name}: aguardando... tentativa ${i}/${retries}${NC}"
        sleep "$delay_seconds"
    done

    echo -e "❌ ${service_name}: não respondeu em ${url}"
    return 1
}

check_api_target_up() {
    local targets_json
    targets_json="$(curl -fsS "${PROMETHEUS_BASE_URL}/api/v1/targets" 2>/dev/null || true)"

    if [ -z "$targets_json" ]; then
        echo "0"
        return 0
    fi

    echo "$targets_json" | "$PYTHON_CMD" -c '
import json
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    print("0")
    raise SystemExit(0)

targets = payload.get("data", {}).get("activeTargets", [])
ok = any(
    t.get("labels", {}).get("job") == "api-churn" and t.get("health") == "up"
    for t in targets
)
print("1" if ok else "0")
'
}

# Diretório raiz do projeto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}📦 Etapa 1: Preparando modelo e predições${NC}"
echo "$(log_time) - Iniciando preparação..."

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 não encontrado. Tentando usar python...${NC}"
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Verificar se dependências estão instaladas
echo -e "${YELLOW}📚 Verificando dependências Python...${NC}"
echo "$(log_time) - Importando loguru..."
$PYTHON_CMD -c "import loguru" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Instalando dependências (isso pode levar 1-2 minutos)...${NC}"
    echo "$(log_time) - pip install iniciado..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependências instaladas${NC}"
        echo "$(log_time) - Conclusão de dependências"
    else
        echo -e "${YELLOW}⚠️  Erro ao instalar dependências. Tentando continuar...${NC}"
    fi
else
    echo -e "${GREEN}✅ Dependências já instaladas${NC}"
fi

# Verificar se modelo existe
if [ ! -f "models/pipeline_modelo_treinado.joblib" ]; then
    echo -e "${YELLOW}📚 Modelo não encontrado. Treinando modelo (isso pode levar alguns minutos)...${NC}"
    echo "$(log_time) - Treinamento iniciado..."
    $PYTHON_CMD src/treinamento.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Modelo treinado com sucesso${NC}"
        echo "$(log_time) - Treinamento concluído"
    else
        echo -e "${YELLOW}⚠️  Erro ao treinar modelo, mas continuando...${NC}"
    fi
else
    echo -e "${GREEN}✅ Modelo já existe${NC}"
fi

# Verificar se predições existem
if [ ! -f "outputs/predicoes.csv" ]; then
    echo -e "${YELLOW}🔮 Predições não encontradas. Gerando predições...${NC}"
    echo "$(log_time) - Predição iniciada..."
    $PYTHON_CMD src/predicao.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Predições geradas com sucesso${NC}"
        echo "$(log_time) - Predição concluída"
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
echo "$(log_time) - Build do Prometheus iniciado..."
cd monitoring/prometheus
if [ ! -f "Dockerfile.prometheus" ]; then
    echo "❌ Dockerfile.prometheus não encontrado!"
    exit 1
fi

docker build -t prometheus-mlops -f Dockerfile.prometheus .
docker run -d \
    --name prometheus \
    --network "$NETWORK_NAME" \
    -p 9090:9090 \
    prometheus-mlops

echo -e "${GREEN}✅ Prometheus iniciado em ${PROMETHEUS_BASE_URL}${NC}"
echo "$(log_time) - Prometheus pronto"

# Build e start Grafana
echo ""
echo -e "${BLUE}📊 Etapa 4: Iniciando Grafana${NC}"
echo "$(log_time) - Build do Grafana iniciado..."
cd ../grafana
if [ ! -f "Dockerfile.grafana" ]; then
    echo "❌ Dockerfile.grafana não encontrado!"
    exit 1
fi

docker build -t grafana-mlops -f Dockerfile.grafana .
docker run -d \
    --name grafana \
    --network "$NETWORK_NAME" \
    -p 3000:3000 \
    -e "GF_SERVER_DOMAIN=$([ -n "${CODESPACE_NAME:-}" ] && echo "${CODESPACE_NAME}-3000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}" || echo "localhost")" \
    -e "GF_SERVER_ROOT_URL=${GRAFANA_BASE_URL}/" \
    grafana-mlops

echo -e "${GREEN}✅ Grafana iniciado em ${GRAFANA_BASE_URL}${NC}"
echo -e "   Credenciais: ${YELLOW}admin / admin${NC}"
echo "$(log_time) - Grafana pronto"

# Build e start API
echo ""
echo -e "${BLUE}🚀 Etapa 5: Iniciando API de Churn${NC}"
echo "$(log_time) - Build da API iniciado..."
cd "$PROJECT_ROOT"
if [ ! -f "Dockerfile.api" ]; then
    echo "❌ Dockerfile.api não encontrado!"
    exit 1
fi

docker build -t api-churn -f Dockerfile.api .
docker run -d \
    --name api-churn \
    --network "$NETWORK_NAME" \
    -p 8000:8000 \
    api-churn

echo -e "${GREEN}✅ API iniciada em ${API_BASE_URL}${NC}"
echo -e "   Documentação: ${BLUE}${API_BASE_URL}/docs${NC}"
echo "$(log_time) - API pronto"

# Verificar saúde dos containers
echo ""
echo -e "${BLUE}🔍 Etapa 6: Verificando saúde dos containers${NC}"
echo "$(log_time) - Iniciando health checks..."

if ! wait_for_http_ok "Prometheus" "$PROMETHEUS_HEALTH_URL" 20 3; then
    echo -e "${YELLOW}⚠️  Prosseguindo para diagnóstico, mas Prometheus não ficou healthy${NC}"
fi

if ! wait_for_http_ok "Grafana" "$GRAFANA_HEALTH_URL" 20 3; then
    echo -e "${YELLOW}⚠️  Prosseguindo para diagnóstico, mas Grafana não ficou healthy${NC}"
fi

if ! wait_for_http_ok "API" "$API_HEALTH_URL" 20 3; then
    echo -e "${YELLOW}⚠️  Prosseguindo para diagnóstico, mas API não ficou healthy${NC}"
fi

# Verificar se Prometheus está coletando métricas da API
echo ""
echo -e "${BLUE}🎯 Etapa 7: Verificando coleta de métricas${NC}"

if wait_for_http_ok "Endpoint /metrics da API" "$API_METRICS_URL" 10 2; then
    echo -e "${GREEN}✅ API expondo métricas Prometheus${NC}"
else
    echo -e "${YELLOW}⚠️  API ainda não está expondo /metrics${NC}"
fi

sleep 5  # Aguardar primeiro scrape

API_TARGET_UP="$(check_api_target_up)"
if [ "$API_TARGET_UP" = "1" ]; then
    echo -e "${GREEN}✅ Prometheus coletando métricas da API${NC}"
else
    echo -e "${YELLOW}⚠️  Target api-churn ainda não está UP no Prometheus${NC}"
fi

# Resumo final
echo ""
echo "=========================================="
echo -e "${GREEN}✅ STACK INICIADA COM SUCESSO!${NC}"
echo "$(log_time) - Stack pronta para uso"
echo "=========================================="
echo ""
echo "📊 URLs de acesso:"
echo -e "   • API:        ${BLUE}${API_BASE_URL}${NC}"
echo -e "   • API Docs:   ${BLUE}${API_BASE_URL}/docs${NC}"
echo -e "   • Metrics:    ${BLUE}${API_BASE_URL}/metrics${NC}"
echo -e "   • Prometheus: ${BLUE}${PROMETHEUS_BASE_URL}${NC}"
echo -e "   • Grafana:    ${BLUE}${GRAFANA_BASE_URL}${NC} (admin/admin)"
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
