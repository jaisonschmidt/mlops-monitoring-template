"""
Script para exportar métricas Prometheus em arquivo
Para uso com scripts batch (treinamento, predição, retreinamento)
"""
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from prometheus_client import write_to_textfile, REGISTRY
from utils.metrics import *  # Importa todas as métricas definidas

def export_metrics_to_file(output_path="outputs/prometheus_metrics.txt"):
    """
    Exporta todas as métricas Prometheus para arquivo de texto
    
    Args:
        output_path: Caminho do arquivo de saída
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Escrever métricas no formato Prometheus
    write_to_textfile(str(output_file), REGISTRY)
    print(f"✅ Métricas exportadas para: {output_file}")
    print(f"📊 Total de métricas: {len(list(REGISTRY.collect()))}")
    
    # Mostrar resumo das métricas
    print("\n📈 Resumo das métricas exportadas:")
    for metric in REGISTRY.collect():
        if metric.samples:
            print(f"  - {metric.name}: {metric.type}")

if __name__ == "__main__":
    # Permite passar caminho customizado
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "outputs/prometheus_metrics.txt"
    
    export_metrics_to_file(path)
