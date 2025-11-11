# install libs
# ! pip install pandas numpy scikit-learn imbalanced-learn

# libs 
import numpy as np
import pandas as pd
import joblib

# config
from sklearn import set_config
set_config(transform_output="pandas")

# carregar dados
dt = pd.read_csv("data/raw/dados_novos_1.csv", index_col="id_cliente")
X = dt.drop("saiu", axis=1)
y = dt["saiu"]

# carregar pipeline do modelo
pipeline = joblib.load("models/pipeline_modelo_treinado.joblib")

# fazer predições
preds = pipeline.predict_proba(X)[:,1]

# preds para DataFrame
df_preds = pd.DataFrame(preds, index=X.index, columns=["preds"])

# classificação de risco
condicoes = [
    (df_preds['preds'] > 0.90), 
    (df_preds['preds'] > 0.70), 
    (df_preds['preds'] > 0.50),
    (df_preds['preds'] < 0.50)]

escolhas = ["Risco baixo", "Risco moderado", "Risco alto ", "Risco muito alto"]

df_preds["Classificação"] = np.select(condicoes, escolhas, default='Ruim')

# salvar em .CSV
df_preds.to_csv("outputs/predicoes.csv")
