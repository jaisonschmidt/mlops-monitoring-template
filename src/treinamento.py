# install libs
# ! pip install pandas numpy scikit-learn imbalanced-learn

# libs 
import numpy as np
import pandas as pd

# setar todas as saídas para DataFrames Pandas
from sklearn import set_config
set_config(transform_output="pandas")

# dados
dt = pd.read_csv("data/raw/dados_treino.csv", index_col="id_cliente")
X = dt.drop("saiu", axis=1)
y = dt["saiu"]

# separar variáveis
numerical = ["idade", "saldo_conta", "salario_estimado", "escore_credito"]
categorical = ["pais", "genero", "cartao_credito"]
ordinal = ["anos_cliente", "numero_produtos"]

# divisão treino-teste
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, stratify=y, test_size=0.15)

# imputação de valores ausentes
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

# transformações
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

# SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=32, k_neighbors=10)

# modelo
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

# tuning do limiar de predição
from sklearn.model_selection import TunedThresholdClassifierCV
from sklearn.metrics import make_scorer, fbeta_score

tt_rf = TunedThresholdClassifierCV(
     rf, 
     scoring=make_scorer(fbeta_score, beta=2, average="weighted"), 
     cv=5
     )

# pipeline
pipeline = Pipeline(
    steps=[
        ("imputation", imputers),
        ("transformation", transformers),
        ("poly", poly),
        ("smote", smote),
        ("clf", tt_rf)
    ]
)

# treino
pipeline.fit(X_train, y_train)

# métricas de validação
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

# treino final e exportar
X_final = pd.DataFrame(np.vstack((X_train, X_test)), columns=X.columns)
y_final = pd.Series(np.concatenate((y_train.values, y_test.values)))

pipeline.fit(X_final, y_final)

import joblib
joblib.dump(pipeline, "models/pipeline_modelo_treinado.joblib")
