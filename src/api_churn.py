"""
API FastAPI para Predição de Risco de Churn

Esta API expõe os dados de predição de churn dos clientes,
permitindo consultas por ID do cliente.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
from typing import Optional

# Inicializar FastAPI
app = FastAPI(
    title="API de Predição de Churn",
    description="API para consultar risco de churn de clientes",
    version="1.0.0"
)

# Caminho para o arquivo de predições
PREDICOES_PATH = Path(__file__).parent.parent / "outputs" / "predicoes.csv"

# Cache para armazenar os dados
predicoes_df = None


def carregar_predicoes():
    """Carrega o arquivo de predições em memória"""
    global predicoes_df
    try:
        predicoes_df = pd.read_csv(PREDICOES_PATH)
        print(f"✓ Arquivo de predições carregado: {len(predicoes_df)} registros")
    except FileNotFoundError:
        print(f"✗ Arquivo não encontrado: {PREDICOES_PATH}")
        predicoes_df = None
    except Exception as e:
        print(f"✗ Erro ao carregar predições: {e}")
        predicoes_df = None


# Carregar dados na inicialização
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da API"""
    carregar_predicoes()


# Modelos de resposta
class ChurnResponse(BaseModel):
    """Modelo de resposta para consulta de churn"""
    id_cliente: int
    risco_churn: float
    previsao_churn: int
    mensagem: str


class HealthResponse(BaseModel):
    """Modelo de resposta para health check"""
    status: str
    total_predicoes: int


# Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Endpoint raiz - Informações da API"""
    return {
        "api": "API de Predição de Churn",
        "versao": "1.0.0",
        "endpoints": {
            "health": "/health",
            "churn_por_id": "/churn/{id_cliente}",
            "todas_predicoes": "/churn/todas",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Verifica o status da API e dos dados"""
    if predicoes_df is None:
        raise HTTPException(
            status_code=503,
            detail="Serviço indisponível - Dados de predição não carregados"
        )
    
    return HealthResponse(
        status="OK",
        total_predicoes=len(predicoes_df)
    )


@app.get("/churn/{id_cliente}", response_model=ChurnResponse, tags=["Churn"])
async def obter_churn_cliente(id_cliente: int):
    """
    Obtém o risco de churn para um cliente específico
    
    Args:
        id_cliente: ID do cliente
        
    Returns:
        Informações sobre o risco de churn do cliente
    """
    if predicoes_df is None:
        raise HTTPException(
            status_code=503,
            detail="Serviço indisponível - Dados não carregados"
        )
    
    # Buscar cliente no DataFrame
    cliente = predicoes_df[predicoes_df['id_cliente'] == id_cliente]
    
    if cliente.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {id_cliente} não encontrado"
        )
    
    # Extrair dados do cliente
    registro = cliente.iloc[0]
    risco = float(registro['preds'])
    classificacao = str(registro['Classificação'])
    
    # Determinar previsão binária baseado no risco
    previsao = 1 if risco > 0.5 else 0
    
    # Classificar risco
    if risco < 0.3:
        nivel_risco = "BAIXO"
    elif risco < 0.6:
        nivel_risco = "MÉDIO"
    else:
        nivel_risco = "ALTO"
    
    return ChurnResponse(
        id_cliente=id_cliente,
        risco_churn=round(risco, 4),
        previsao_churn=previsao,
        mensagem=f"Risco de churn: {nivel_risco} ({risco*100:.2f}%) - {classificacao}"
    )


@app.get("/churn/todas/predicoes", tags=["Churn"])
async def obter_todas_predicoes(
    limite: Optional[int] = 100,
    risco_minimo: Optional[float] = None
):
    """
    Obtém todas as predições de churn
    
    Args:
        limite: Número máximo de registros a retornar (padrão: 100)
        risco_minimo: Filtrar apenas clientes com risco >= este valor (0.0 a 1.0)
        
    Returns:
        Lista de predições
    """
    if predicoes_df is None:
        raise HTTPException(
            status_code=503,
            detail="Serviço indisponível - Dados não carregados"
        )
    
    df_filtrado = predicoes_df.copy()
    
    # Aplicar filtro de risco mínimo se fornecido
    if risco_minimo is not None:
        if not (0.0 <= risco_minimo <= 1.0):
            raise HTTPException(
                status_code=400,
                detail="risco_minimo deve estar entre 0.0 e 1.0"
            )
        df_filtrado = df_filtrado[df_filtrado['preds'] >= risco_minimo]
    
    # Aplicar limite
    df_filtrado = df_filtrado.head(limite)
    
    # Converter para lista de dicionários
    predicoes = []
    for _, row in df_filtrado.iterrows():
        risco = float(row['preds'])
        previsao = 1 if risco > 0.5 else 0
        predicoes.append({
            'id_cliente': int(row['id_cliente']),
            'risco_churn': round(risco, 4),
            'previsao_churn': previsao,
            'classificacao': str(row['Classificação'])
        })
    
    return {
        'total_registros': len(predicoes),
        'filtros': {
            'limite': limite,
            'risco_minimo': risco_minimo
        },
        'predicoes': predicoes
    }


@app.post("/recarregar", tags=["Administração"])
async def recarregar_dados():
    """
    Recarrega os dados de predição do arquivo CSV
    
    Útil quando o arquivo de predições é atualizado
    """
    carregar_predicoes()
    
    if predicoes_df is None:
        raise HTTPException(
            status_code=500,
            detail="Erro ao recarregar dados"
        )
    
    return {
        'status': 'Dados recarregados com sucesso',
        'total_registros': len(predicoes_df)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
