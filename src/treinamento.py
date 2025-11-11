# install libs
# ! pip install pandas numpy scikit-learn imbalanced-learn

# libs 
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

# Configurar logging
from utils.logger import setup_logger, logger
setup_logger("training")

logger.info("="*60)
logger.info("Iniciando script de treinamento do modelo")
logger.info("="*60)

# setar todas as saídas para DataFrames Pandas
from sklearn import set_config
set_config(transform_output="pandas")

# dados
logger.info("Etapa 1: Carregamento dos dados")
dt = pd.read_csv("data/raw/dados_treino.csv", index_col="id_cliente")
X = dt.drop("saiu", axis=1)
y = dt["saiu"]
logger.success(f"Dados carregados: {X.shape[0]} amostras, {X.shape[1]} features")
logger.debug(f"Distribuição da variável alvo: {y.value_counts().to_dict()}")

# separar variáveis
numerical = ["idade", "saldo_conta", "salario_estimado", "escore_credito"]
categorical = ["pais", "genero", "cartao_credito"]
ordinal = ["anos_cliente", "numero_produtos"]

# divisão treino-teste
logger.info("Etapa 2: Divisão treino-teste (85/15)")
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, stratify=y, test_size=0.15)
logger.success(f"Treino: {X_train.shape[0]} amostras | Teste: {X_test.shape[0]} amostras")

# imputação de valores ausentes
logger.info("Etapa 3: Configuração de imputação de valores ausentes")
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer

imputers = ColumnTransformer(
    transformers=[
        ("imp_num", KNNImputer(n_neighbors=10), numerical),
        ("imp_cat", SimpleImputer(strategy="most_frequent"), categorical + ordinal),
    ],
    remainder="drop", 
    n_jobs=-1, 
    verbose_feature_names_out=False
)
logger.debug("Imputers configurados: KNN para numéricos, Moda para categóricos")

# transformações
logger.info("Etapa 4: Configuração de transformações")
from sklearn.preprocessing import OneHotEncoder, TargetEncoder, StandardScaler, PowerTransformer, PolynomialFeatures
from imblearn.pipeline import Pipeline

transf_num = Pipeline(steps=[
    ('power_transform', PowerTransformer()),
    ('standard_scale', StandardScaler())
])

transformers = ColumnTransformer(
    transformers=[
        ("numerical", transf_num, numerical),
        ("categorical", OneHotEncoder(sparse_output=False), categorical),
        ("ordinal", TargetEncoder(cv=10), ordinal)
    ],
    remainder="drop", 
    n_jobs=-1, 
    verbose_feature_names_out=True
)

poly = PolynomialFeatures(interaction_only=True, include_bias=False)
logger.debug("Transformers configurados: PowerTransform, OneHot, TargetEncoder, Polynomial")

# SMOTE
logger.info("Etapa 5: Configuração do SMOTE para balanceamento")
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=32, k_neighbors=10)
logger.debug("SMOTE configurado com k=10")

# modelo
logger.info("Etapa 6: Configuração do modelo RandomForest")
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=1000,              
    criterion="gini",               
    max_depth=20,                   
    min_samples_leaf=5,             
    min_samples_split=10,            
    max_features="sqrt",            
    class_weight="balanced",        
    random_state=42,                
    n_jobs=-1                       
)
logger.debug("RandomForest: 1000 árvores, max_depth=20, balanced")

# tuning do limiar de predição
from sklearn.model_selection import TunedThresholdClassifierCV
from sklearn.metrics import make_scorer, fbeta_score

tt_rf = TunedThresholdClassifierCV(
     rf, 
     scoring=make_scorer(fbeta_score, beta=2, average="weighted"), 
     cv=5
     )

# pipeline
logger.info("Etapa 7: Montagem do pipeline completo")
pipeline = Pipeline(
    steps=[
        ("imputation", imputers),
        ("transformation", transformers),
        ("poly", poly),
        ("smote", smote),
        ("clf", tt_rf)
    ]
)
logger.success("Pipeline montado com sucesso")

# treino
logger.info("Etapa 8: Iniciando treinamento do modelo...")
import time
start_time = time.time()

pipeline.fit(X_train, y_train)

training_duration = time.time() - start_time
logger.success(f"Treinamento concluído em {training_duration:.2f} segundos")

# métricas de validação
logger.info("Etapa 9: Calculando métricas de validação")
from sklearn.metrics import precision_score, recall_score, roc_auc_score

y_pred_rf = pipeline.predict(X_test)
y_pred_proba_rf = pipeline.predict_proba(X_test)[:,1]

metricas = {
    "f1_score":fbeta_score(y_test, y_pred_rf, beta=1, average="weighted"),
    "f2_score":fbeta_score(y_test, y_pred_rf, beta=2, average="weighted"),
    "precisão":precision_score(y_test, y_pred_rf, average="weighted"),
    "recall":recall_score(y_test, y_pred_rf, average="weighted"),
    "auc":float(roc_auc_score(y_test, y_pred_proba_rf, average="weighted")),
    }

logger.info("Métricas calculadas:")
for metric, value in metricas.items():
    logger.info(f"  {metric}: {value:.4f}")

metricas_df = pd.DataFrame(metricas, index=range(1)).T
metricas_df.index.name = "Métricas"
metricas_df.rename(columns={0: "Valores"}, inplace=True)

condicoes = [
    (metricas_df['Valores'] > 0.90), 
    (metricas_df['Valores'] > 0.80), 
    (metricas_df['Valores'] > 0.70), 
    (metricas_df['Valores'] > 0.60)]

escolhas = ['Excelente', 'Bom', 'Aceitável', 'Fraco']

metricas_df['Classificação'] = np.select(condicoes, escolhas, default='Ruim')
metricas_df.to_csv("outputs/metricas_desempenho_evasao.csv")
logger.success("Métricas salvas em: outputs/metricas_desempenho_evasao.csv")

# treino final e exportar
logger.info("Etapa 10: Treinamento final com todos os dados")
X_final = pd.DataFrame(np.vstack((X_train, X_test)), columns=X.columns)
y_final = pd.Series(np.concatenate((y_train.values, y_test.values)))

logger.info(f"Dataset final: {X_final.shape[0]} amostras")
pipeline.fit(X_final, y_final)
logger.success("Treinamento final concluído")

import joblib
model_path = "models/pipeline_modelo_treinado.joblib"
joblib.dump(pipeline, model_path)
logger.success(f"Modelo salvo em: {model_path}")

logger.info("="*60)
logger.success("TREINAMENTO CONCLUÍDO COM SUCESSO!")
logger.info("="*60)
logger.info(f"Tempo total: {training_duration:.2f}s")
logger.info(f"F2-Score: {metricas['f2_score']:.4f}")
logger.info(f"AUC: {metricas['auc']:.4f}")
logger.info("="*60)
