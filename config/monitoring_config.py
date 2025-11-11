"""
Configurações centralizadas para o sistema de monitoramento
"""
import os
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
MONITORING_DIR = BASE_DIR / "monitoring"

# Configurações de Logging (Loguru)
LOG_CONFIG = {
    "rotation": "10 MB",  # Rotacionar quando arquivo atingir 10 MB
    "retention": "7 days",  # Manter logs por 7 dias
    "compression": "zip",  # Comprimir logs antigos
    "level": "INFO",  # Nível padrão de log
    "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    "serialize": False,  # True para logs em JSON
}

# Arquivos de log por componente
LOG_FILES = {
    "api": LOGS_DIR / "{time:YYYY-MM-DD}_api.log",
    "training": LOGS_DIR / "{time:YYYY-MM-DD}_training.log",
    "prediction": LOGS_DIR / "{time:YYYY-MM-DD}_prediction.log",
    "retraining": LOGS_DIR / "{time:YYYY-MM-DD}_retraining.log",
}

# Configurações do Prometheus
PROMETHEUS_CONFIG = {
    "port": 9090,
    "scrape_interval": "15s",
    "evaluation_interval": "15s",
}

# Configurações do Grafana
GRAFANA_CONFIG = {
    "port": 3000,
    "admin_user": os.getenv("GRAFANA_ADMIN_USER", "admin"),
    "admin_password": os.getenv("GRAFANA_ADMIN_PASSWORD", "admin"),
}

# Thresholds para alertas
ALERT_THRESHOLDS = {
    "api_error_rate": 0.05,  # 5% de taxa de erro
    "api_latency_p95": 2.0,  # 2 segundos
    "model_f2_score_min": 0.7,  # F2-Score mínimo aceitável
    "model_auc_min": 0.75,  # AUC mínimo aceitável
    "high_risk_clients_max": 1000,  # Número máximo de clientes em alto risco
    "churn_score_avg_max": 0.6,  # Score médio máximo aceitável
}

# Configurações de métricas de negócio
BUSINESS_CONFIG = {
    "risk_levels": {
        "baixo": (0.0, 0.5),
        "medio": (0.5, 0.7),
        "alto": (0.7, 1.0),
    }
}

# Criar diretórios se não existirem
LOGS_DIR.mkdir(exist_ok=True)
