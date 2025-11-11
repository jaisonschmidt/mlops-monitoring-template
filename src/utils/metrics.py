"""
Módulo de métricas usando Prometheus Client

Define todas as métricas customizadas para monitoramento da aplicação MLOps,
incluindo métricas de infraestrutura, negócio e machine learning.
"""
from prometheus_client import Counter, Gauge, Histogram, Info, Summary
from config.monitoring_config import BUSINESS_CONFIG

# ============================================================================
# MÉTRICAS DE INFRAESTRUTURA DA API
# ============================================================================

# Counter: Total de predições servidas
model_predictions_total = Counter(
    'model_predictions_total',
    'Número total de predições realizadas pelo modelo',
    ['endpoint']  # Label para diferenciar endpoints
)

# Counter: Cache hits
model_cache_hits = Counter(
    'model_cache_hits',
    'Número de consultas servidas do cache'
)

# Gauge: Predições carregadas em memória
api_predictions_loaded = Gauge(
    'api_predictions_loaded',
    'Número de predições carregadas em memória'
)

# Gauge: Requisições ativas
api_active_requests = Gauge(
    'api_active_requests',
    'Número de requisições HTTP ativas no momento'
)

# Counter: Total de erros
api_errors_total = Counter(
    'api_errors_total',
    'Total de erros HTTP',
    ['status_code', 'endpoint']
)

# ============================================================================
# MÉTRICAS DE NEGÓCIO (CHURN)
# ============================================================================

# Gauge: Clientes em alto risco
churn_predictions_high_risk = Gauge(
    'churn_predictions_high_risk',
    'Número de clientes com alto risco de churn (>0.7)'
)

# Gauge: Distribuição por nível de risco
churn_predictions_by_level = Gauge(
    'churn_predictions_by_level',
    'Número de clientes por nível de risco',
    ['level']  # baixo, medio, alto
)

# Gauge: Score médio de churn
churn_prediction_score_avg = Gauge(
    'churn_prediction_score_avg',
    'Score médio de probabilidade de churn'
)

# Histogram: Distribuição dos scores
churn_prediction_score_distribution = Histogram(
    'churn_prediction_score_distribution',
    'Distribuição dos scores de churn',
    buckets=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# ============================================================================
# MÉTRICAS DE MACHINE LEARNING
# ============================================================================

# Gauge: F2-Score do modelo
model_f2_score = Gauge(
    'model_f2_score',
    'F2-Score do modelo em validação'
)

# Gauge: AUC-ROC
model_auc_score = Gauge(
    'model_auc_score',
    'AUC-ROC do modelo em validação'
)

# Gauge: Tempo de treinamento
model_training_duration_seconds = Gauge(
    'model_training_duration_seconds',
    'Duração do último treinamento em segundos'
)

# Gauge: Número de amostras de treino
model_training_samples = Gauge(
    'model_training_samples',
    'Número de amostras usadas no treinamento'
)

# Info: Versão do modelo
model_version_info = Info(
    'model_version',
    'Informações sobre a versão do modelo'
)

# Gauge: Precisão
model_precision = Gauge(
    'model_precision',
    'Precisão do modelo em validação'
)

# Gauge: Recall
model_recall = Gauge(
    'model_recall',
    'Recall do modelo em validação'
)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def update_churn_distribution_metrics(predictions_data):
    """
    Atualiza métricas de distribuição de churn
    
    Args:
        predictions_data: Array numpy ou DataFrame com as predições
    """
    import numpy as np
    import pandas as pd
    
    if predictions_data is None:
        return
    
    # Converter para array se for DataFrame
    if isinstance(predictions_data, pd.DataFrame):
        if predictions_data.empty:
            return
        preds_array = predictions_data['preds'].values if 'preds' in predictions_data.columns else predictions_data.values
    elif isinstance(predictions_data, (list, np.ndarray)):
        preds_array = np.array(predictions_data)
    else:
        return
    
    if len(preds_array) == 0:
        return
    
    # Score médio
    avg_score = float(np.mean(preds_array))
    churn_prediction_score_avg.set(avg_score)
    
    # Clientes em alto risco (>0.7)
    high_risk_count = int(np.sum(preds_array > 0.7))
    churn_predictions_high_risk.set(high_risk_count)
    
    # Distribuição por nível
    risk_levels = BUSINESS_CONFIG['risk_levels']
    
    baixo_count = int(np.sum((preds_array >= risk_levels['baixo'][0]) & 
                             (preds_array < risk_levels['baixo'][1])))
    medio_count = int(np.sum((preds_array >= risk_levels['medio'][0]) & 
                             (preds_array < risk_levels['medio'][1])))
    alto_count = int(np.sum((preds_array >= risk_levels['alto'][0]) & 
                            (preds_array <= risk_levels['alto'][1])))
    
    churn_predictions_by_level.labels(level='baixo').set(baixo_count)
    churn_predictions_by_level.labels(level='medio').set(medio_count)
    churn_predictions_by_level.labels(level='alto').set(alto_count)
    
    # Atualizar histograma
    for score in preds_array:
        churn_prediction_score_distribution.observe(float(score))


def update_model_metrics(metrics_dict=None, **kwargs):
    """
    Atualiza métricas do modelo
    
    Args:
        metrics_dict: Dicionário com métricas (f2_score, auc, precisão, recall, etc)
        **kwargs: Ou passar métricas como argumentos nomeados
    """
    # Se passou dicionário, usa ele, senão usa kwargs
    metrics = metrics_dict if metrics_dict is not None else kwargs
    
    if 'f2_score' in metrics:
        model_f2_score.set(metrics['f2_score'])
    
    if 'auc' in metrics or 'auc_score' in metrics:
        model_auc_score.set(metrics.get('auc', metrics.get('auc_score')))
    
    if 'precisão' in metrics or 'precision' in metrics:
        model_precision.set(metrics.get('precisão', metrics.get('precision')))
    
    if 'recall' in metrics:
        model_recall.set(metrics['recall'])


def set_model_version(version_info):
    """
    Define informações da versão do modelo
    
    Args:
        version_info: String com versão ou dicionário com informações (version, date, algorithm, etc)
    """
    if isinstance(version_info, str):
        model_version_info.info({'version': version_info})
    else:
        model_version_info.info(version_info)


# ============================================================================
# DECORATORS
# ============================================================================

import time
import functools

def track_api_request(endpoint_name):
    """
    Decorator para rastrear requisições da API
    
    Args:
        endpoint_name: Nome do endpoint
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            api_active_requests.inc()
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                model_predictions_total.labels(endpoint=endpoint_name).inc()
                return result
            except Exception as e:
                # Rastrear erro (status code será capturado pelo middleware)
                raise
            finally:
                api_active_requests.dec()
                duration = time.time() - start_time
        
        return wrapper
    return decorator


# Exportar todas as métricas
__all__ = [
    # Infraestrutura
    'model_predictions_total',
    'model_cache_hits',
    'api_predictions_loaded',
    'api_active_requests',
    'api_errors_total',
    
    # Negócio
    'churn_predictions_high_risk',
    'churn_predictions_by_level',
    'churn_prediction_score_avg',
    'churn_prediction_score_distribution',
    
    # ML
    'model_f2_score',
    'model_auc_score',
    'model_training_duration_seconds',
    'model_training_samples',
    'model_version_info',
    'model_precision',
    'model_recall',
    
    # Funções
    'update_churn_distribution_metrics',
    'update_model_metrics',
    'set_model_version',
    'track_api_request',
    
    # Aliases em maiúsculas para compatibilidade
    'MODEL_PREDICTIONS_TOTAL',
    'MODEL_TRAINING_DURATION',
    'MODEL_TRAINING_SAMPLES',
    'MODEL_RETRAINING_TOTAL',
    'CHURN_SCORE_AVERAGE',
]

# ============================================================================
# ALIASES EM MAIÚSCULAS PARA COMPATIBILIDADE
# ============================================================================
MODEL_PREDICTIONS_TOTAL = model_predictions_total
MODEL_TRAINING_DURATION = model_training_duration_seconds
MODEL_TRAINING_SAMPLES = model_training_samples
MODEL_RETRAINING_TOTAL = Counter(
    'model_retraining_total',
    'Número total de retreinamentos realizados'
)
CHURN_SCORE_AVERAGE = churn_prediction_score_avg
