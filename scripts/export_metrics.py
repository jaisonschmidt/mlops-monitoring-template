#!/usr/bin/env python3
"""
Script para exportar métricas do Prometheus para análise

Este script consulta o Prometheus e exporta métricas para arquivos JSON/CSV
"""
import requests
import json
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

from config.monitoring_config import PROMETHEUS_CONFIG

PROMETHEUS_URL = f"http://localhost:{PROMETHEUS_CONFIG['port']}"


def query_prometheus(query):
    """
    Executa uma query no Prometheus
    
    Args:
        query: Query PromQL
        
    Returns:
        Resultado da query ou None se houver erro
    """
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={'query': query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'success':
            return data['data']['result']
        else:
            print(f"❌ Erro na query: {data.get('error', 'Desconhecido')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar ao Prometheus: {e}")
        return None


def export_metrics_to_json(output_file="outputs/metrics_export.json"):
    """
    Exporta principais métricas para JSON
    
    Args:
        output_file: Caminho do arquivo de saída
    """
    print("="*60)
    print("Exportando Métricas do Prometheus")
    print("="*60)
    
    metrics_queries = {
        # Métricas de ML
        "model_f2_score": "model_f2_score",
        "model_auc_score": "model_auc_score",
        "model_precision": "model_precision",
        "model_recall": "model_recall",
        "model_training_duration_seconds": "model_training_duration_seconds",
        "model_training_samples": "model_training_samples",
        
        # Métricas de Negócio
        "churn_predictions_high_risk": "churn_predictions_high_risk",
        "churn_prediction_score_avg": "churn_prediction_score_avg",
        "churn_predictions_baixo": 'churn_predictions_by_level{level="baixo"}',
        "churn_predictions_medio": 'churn_predictions_by_level{level="medio"}',
        "churn_predictions_alto": 'churn_predictions_by_level{level="alto"}',
        
        # Métricas de API
        "api_predictions_loaded": "api_predictions_loaded",
        "model_predictions_total": "sum(model_predictions_total)",
        "http_requests_total": "sum(http_requests_total)",
        "http_requests_rate": "rate(http_requests_total[5m])",
    }
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "prometheus_url": PROMETHEUS_URL,
        "metrics": {}
    }
    
    for metric_name, query in metrics_queries.items():
        print(f"Consultando: {metric_name}...", end=" ")
        result = query_prometheus(query)
        
        if result:
            if len(result) > 0:
                value = result[0]['value'][1]  # [timestamp, value]
                results["metrics"][metric_name] = float(value)
                print(f"✓ {value}")
            else:
                results["metrics"][metric_name] = None
                print("⚠ Sem dados")
        else:
            results["metrics"][metric_name] = None
            print("❌ Erro")
    
    # Salvar JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print(f"✅ Métricas exportadas para: {output_path}")
    print("="*60)
    
    return results


def export_metrics_to_csv(output_file="outputs/metrics_export.csv"):
    """
    Exporta métricas para CSV
    
    Args:
        output_file: Caminho do arquivo de saída
    """
    results = export_metrics_to_json()
    
    if results and results["metrics"]:
        df = pd.DataFrame([results["metrics"]])
        df['timestamp'] = results['timestamp']
        
        # Reorganizar colunas
        cols = ['timestamp'] + [col for col in df.columns if col != 'timestamp']
        df = df[cols]
        
        # Salvar CSV
        output_path = Path(output_file)
        df.to_csv(output_path, index=False)
        
        print(f"✅ Métricas também exportadas para: {output_path}")
        
        return df
    
    return None


def print_metrics_summary():
    """
    Imprime resumo das métricas no console
    """
    results = export_metrics_to_json()
    
    if not results or not results["metrics"]:
        print("\n❌ Não foi possível obter métricas")
        return
    
    metrics = results["metrics"]
    
    print("\n" + "="*60)
    print("📊 RESUMO DE MÉTRICAS")
    print("="*60)
    
    print("\n🤖 Machine Learning:")
    print(f"  F2-Score:         {metrics.get('model_f2_score', 'N/A')}")
    print(f"  AUC-ROC:          {metrics.get('model_auc_score', 'N/A')}")
    print(f"  Precisão:         {metrics.get('model_precision', 'N/A')}")
    print(f"  Recall:           {metrics.get('model_recall', 'N/A')}")
    
    duration = metrics.get('model_training_duration_seconds')
    if duration:
        print(f"  Tempo Treino:     {duration:.2f}s ({duration/60:.2f} min)")
    
    print(f"  Amostras Treino:  {metrics.get('model_training_samples', 'N/A')}")
    
    print("\n💼 Negócio (Churn):")
    print(f"  Alto Risco:       {metrics.get('churn_predictions_high_risk', 'N/A')}")
    print(f"  Score Médio:      {metrics.get('churn_prediction_score_avg', 'N/A')}")
    print(f"  Baixo Risco:      {metrics.get('churn_predictions_baixo', 'N/A')}")
    print(f"  Médio Risco:      {metrics.get('churn_predictions_medio', 'N/A')}")
    print(f"  Alto Risco:       {metrics.get('churn_predictions_alto', 'N/A')}")
    
    total = sum([
        metrics.get('churn_predictions_baixo', 0) or 0,
        metrics.get('churn_predictions_medio', 0) or 0,
        metrics.get('churn_predictions_alto', 0) or 0
    ])
    if total > 0:
        print(f"  Total Clientes:   {total}")
    
    print("\n🌐 API:")
    print(f"  Predições Loaded: {metrics.get('api_predictions_loaded', 'N/A')}")
    print(f"  Predições Total:  {metrics.get('model_predictions_total', 'N/A')}")
    print(f"  Requests Total:   {metrics.get('http_requests_total', 'N/A')}")
    print(f"  Request Rate:     {metrics.get('http_requests_rate', 'N/A')}")
    
    print("\n" + "="*60)


def check_prometheus_health():
    """
    Verifica se o Prometheus está acessível
    """
    try:
        response = requests.get(f"{PROMETHEUS_URL}/-/healthy", timeout=5)
        response.raise_for_status()
        print(f"✅ Prometheus está rodando em {PROMETHEUS_URL}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Prometheus não está acessível: {e}")
        print(f"   Certifique-se de que está rodando em {PROMETHEUS_URL}")
        return False


if __name__ == "__main__":
    print("\n🔍 Verificando Prometheus...")
    if not check_prometheus_health():
        print("\n💡 Dica: Execute 'docker run -d -p 9090:9090 prometheus-mlops:latest'")
        sys.exit(1)
    
    print()
    
    # Exportar métricas
    if len(sys.argv) > 1:
        if sys.argv[1] == "--json":
            export_metrics_to_json()
        elif sys.argv[1] == "--csv":
            export_metrics_to_csv()
        elif sys.argv[1] == "--summary":
            print_metrics_summary()
        else:
            print("Uso: python export_metrics.py [--json|--csv|--summary]")
    else:
        # Por padrão, mostrar resumo e exportar JSON
        print_metrics_summary()
        export_metrics_to_json()
