# install libs
# ! pip install pandas numpy scikit-learn imbalanced-learn

# libs 
import numpy as np
import pandas as pd
import joblib
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

# Configurar logging e métricas
from utils.logger import setup_logger, logger
from utils.metrics import (
    MODEL_PREDICTIONS_TOTAL,
    update_churn_distribution_metrics,
    CHURN_SCORE_AVERAGE
)
setup_logger("prediction")

logger.info("="*60)
logger.info("Iniciando script de predição")
logger.info("="*60)

# config
from sklearn import set_config
set_config(transform_output="pandas")

# carregar dados
logger.info("Etapa 1: Carregando dados novos")
dt = pd.read_csv("data/raw/dados_novos_1.csv", index_col="id_cliente")
X = dt.drop("saiu", axis=1)
y = dt["saiu"]
logger.success(f"Dados carregados: {X.shape[0]} amostras, {X.shape[1]} features")

# carregar pipeline do modelo
logger.info("Etapa 2: Carregando modelo treinado")
pipeline = joblib.load("models/pipeline_modelo_treinado.joblib")
logger.success("Modelo carregado com sucesso")

# fazer predições
logger.info("Etapa 3: Realizando predições")
preds = pipeline.predict_proba(X)[:,1]
logger.success(f"Predições realizadas para {len(preds)} clientes")

# Atualizar contador de predições
MODEL_PREDICTIONS_TOTAL.labels(endpoint='batch').inc(len(preds))
logger.debug(f"Contador de predições incrementado: +{len(preds)}")

# preds para DataFrame
logger.info("Etapa 4: Processando resultados")
df_preds = pd.DataFrame(preds, index=X.index, columns=["preds"])

# classificação de risco
condicoes = [
    (df_preds['preds'] > 0.90), 
    (df_preds['preds'] > 0.70), 
    (df_preds['preds'] > 0.50),
    (df_preds['preds'] < 0.50)]

escolhas = ["Risco baixo", "Risco moderado", "Risco alto ", "Risco muito alto"]

df_preds["Classificação"] = np.select(condicoes, escolhas, default='Ruim')

# Análise de distribuição
dist = df_preds['Classificação'].value_counts()
logger.info("Distribuição de risco:")
for nivel, count in dist.items():
    logger.info(f"  {nivel}: {count} clientes ({count/len(df_preds)*100:.1f}%)")

score_medio = df_preds['preds'].mean()
logger.info(f"Score médio de churn: {score_medio:.4f}")

# Atualizar métricas Prometheus de distribuição
update_churn_distribution_metrics(df_preds['preds'].values)
CHURN_SCORE_AVERAGE.set(score_medio)
logger.success("Métricas de distribuição de risco atualizadas no Prometheus")

# salvar em .CSV
output_path = "outputs/predicoes.csv"
df_preds.to_csv(output_path)
logger.success(f"Predições salvas em: {output_path}")

logger.info("="*60)
logger.success("PREDIÇÃO CONCLUÍDA COM SUCESSO!")
logger.info("="*60)
