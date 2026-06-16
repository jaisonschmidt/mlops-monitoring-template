"""
Script para teste de carga da API de predição de churn
Simula consultas para gerar métricas no Prometheus
"""
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os

# Resolução dinâmica do host da API:
# Prioridade 1: variável de ambiente API_URL
# Prioridade 2: auto-detecção via GitHub Codespaces
# Prioridade 3: localhost (padrão local)
def _resolve_api_url() -> str:
    if url := os.environ.get("API_URL"):
        return url.rstrip("/")
    codespace_name = os.environ.get("CODESPACE_NAME")
    if codespace_name:
        domain = os.environ.get(
            "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev"
        )
        return f"https://{codespace_name}-8000.{domain}"
    return "http://localhost:8000"


def _resolve_service_url(port: int) -> str:
    codespace_name = os.environ.get("CODESPACE_NAME")
    if codespace_name:
        domain = os.environ.get(
            "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev"
        )
        return f"https://{codespace_name}-{port}.{domain}"
    return f"http://localhost:{port}"


# Configuração
API_URL = _resolve_api_url()
NUM_REQUESTS = 100  # Total de requisições
CONCURRENT_WORKERS = 10  # Requisições paralelas
DELAY_BETWEEN_BATCHES = 0.5  # Segundos
ID_CLIENTES = []


def obter_ids_clientes():
    """Busca IDs válidos diretamente da API para teste de carga."""
    try:
        response = requests.get(
            f"{API_URL}/churn/todas/predicoes",
            params={"limite": 1000},
            timeout=10,
        )
        if response.status_code != 200:
            return []

        payload = response.json()
        predicoes = payload.get("predicoes", [])
        return [item.get("id_cliente") for item in predicoes if "id_cliente" in item]
    except Exception:
        return []


def fazer_consulta(client_id):
    """Faz uma requisição de consulta de churn por ID."""
    try:
        id_cliente = random.choice(ID_CLIENTES)
        
        start_time = time.time()
        response = requests.get(f"{API_URL}/churn/{id_cliente}", timeout=10)
        latency = (time.time() - start_time) * 1000  # ms
        
        if response.status_code == 200:
            resultado = response.json()
            return {
                "id": client_id,
                "status": "success",
                "latency_ms": latency,
                "id_cliente": resultado["id_cliente"],
                "prediction": resultado["risco_churn"],
                "message": resultado["mensagem"],
            }
        else:
            return {
                "id": client_id,
                "status": "error",
                "latency_ms": latency,
                "error": response.text
            }
    except Exception as e:
        return {
            "id": client_id,
            "status": "exception",
            "error": str(e)
        }

def checar_health():
    """Verifica se a API está disponível"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def executar_teste():
    """Executa o teste de carga"""
    print("="*70)
    print("🚀 TESTE DE CARGA - API DE PREDIÇÃO DE CHURN")
    print("="*70)
    
    # Verificar se API está disponível
    print(f"\n🔍 Verificando disponibilidade da API em {API_URL}...")
    if not checar_health():
        print("❌ API não está disponível!")
        print("   Execute: docker run -d --name api-churn -p 8000:8000 api-churn")
        return

    global ID_CLIENTES
    ID_CLIENTES = obter_ids_clientes()
    if not ID_CLIENTES:
        print("❌ Não foi possível obter IDs de clientes para teste.")
        print("   Verifique se o endpoint /churn/todas/predicoes está acessível.")
        return
    
    print("✅ API disponível!")
    
    # Configuração do teste
    print(f"\n📊 Configuração do teste:")
    print(f"   • Total de requisições: {NUM_REQUESTS}")
    print(f"   • Workers paralelos: {CONCURRENT_WORKERS}")
    print(f"   • Delay entre batches: {DELAY_BETWEEN_BATCHES}s")
    print(f"   • IDs disponíveis para consulta: {len(ID_CLIENTES)}")
    
    # Executar teste
    print(f"\n🏃 Iniciando teste às {datetime.now().strftime('%H:%M:%S')}...\n")
    
    resultados = {
        "success": 0,
        "error": 0,
        "exception": 0,
        "latencies": [],
        "predictions": []
    }
    
    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        futures = [executor.submit(fazer_consulta, i) for i in range(NUM_REQUESTS)]
        
        for future in as_completed(futures):
            resultado = future.result()
            
            if resultado["status"] == "success":
                resultados["success"] += 1
                resultados["latencies"].append(resultado["latency_ms"])
                resultados["predictions"].append(resultado["prediction"])
                print(
                    f"✅ Req {resultado['id']:3d} | Cliente {resultado['id_cliente']:5d} | "
                    f"{resultado['latency_ms']:6.1f}ms | Churn: {resultado['prediction']:.3f}"
                )
            elif resultado["status"] == "error":
                resultados["error"] += 1
                print(f"❌ Req {resultado['id']:3d} | Erro HTTP: {resultado.get('error', 'Unknown')}")
            else:
                resultados["exception"] += 1
                print(f"⚠️  Req {resultado['id']:3d} | Exceção: {resultado.get('error', 'Unknown')}")
            
            time.sleep(DELAY_BETWEEN_BATCHES / CONCURRENT_WORKERS)
    
    duration_total = time.time() - start_total
    
    # Estatísticas
    print("\n" + "="*70)
    print("📈 RESULTADOS DO TESTE")
    print("="*70)
    
    print(f"\n⏱️  Duração total: {duration_total:.2f}s")
    print(f"🎯 Taxa de sucesso: {resultados['success']/NUM_REQUESTS*100:.1f}%")
    print(f"✅ Sucesso: {resultados['success']}")
    print(f"❌ Erros: {resultados['error']}")
    print(f"⚠️  Exceções: {resultados['exception']}")
    
    if resultados["latencies"]:
        latencies = sorted(resultados["latencies"])
        print(f"\n📊 Latência (ms):")
        print(f"   • Média: {sum(latencies)/len(latencies):.2f}")
        print(f"   • Mediana: {latencies[len(latencies)//2]:.2f}")
        print(f"   • P95: {latencies[int(len(latencies)*0.95)]:.2f}")
        print(f"   • P99: {latencies[int(len(latencies)*0.99)]:.2f}")
        print(f"   • Mínimo: {min(latencies):.2f}")
        print(f"   • Máximo: {max(latencies):.2f}")
    
    if resultados["predictions"]:
        predictions = resultados["predictions"]
        print(f"\n🎲 Predições de Churn:")
        print(f"   • Média: {sum(predictions)/len(predictions):.4f}")
        print(f"   • Mínimo: {min(predictions):.4f}")
        print(f"   • Máximo: {max(predictions):.4f}")
        
        # Distribuição de risco
        alto_risco = sum(1 for p in predictions if p >= 0.7)
        medio_risco = sum(1 for p in predictions if 0.3 <= p < 0.7)
        baixo_risco = sum(1 for p in predictions if p < 0.3)
        
        print(f"\n📊 Distribuição de Risco:")
        print(f"   • Alto (≥70%): {alto_risco} ({alto_risco/len(predictions)*100:.1f}%)")
        print(f"   • Médio (30-70%): {medio_risco} ({medio_risco/len(predictions)*100:.1f}%)")
        print(f"   • Baixo (<30%): {baixo_risco} ({baixo_risco/len(predictions)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("✅ Teste concluído!")
    print(f"🔗 Verifique as métricas em:")
    print(f"   • Prometheus: {_resolve_service_url(9090)}")
    print(f"   • Grafana: {_resolve_service_url(3000)}")
    print(f"   • Métricas da API: {API_URL}/metrics")
    print("="*70)

if __name__ == "__main__":
    executar_teste()
