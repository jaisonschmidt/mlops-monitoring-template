"""
Script para teste de carga da API de predição de churn
Simula requisições para gerar métricas no Prometheus
"""
import requests
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Configuração
API_URL = "http://localhost:8000"
NUM_REQUESTS = 100  # Total de requisições
CONCURRENT_WORKERS = 10  # Requisições paralelas
DELAY_BETWEEN_BATCHES = 0.5  # Segundos

# Dados de exemplo para predição
SAMPLE_CLIENTS = [
    {
        "pais": "França",
        "genero": "Feminino",
        "idade": 42,
        "anos_cliente": 8,
        "saldo_conta": 159660.80,
        "numero_produtos": 3,
        "cartao_credito": 1,
        "membro_ativo": 0,
        "salario_estimado": 113931.57,
        "escore_credito": 608
    },
    {
        "pais": "Espanha",
        "genero": "Feminino",
        "idade": 41,
        "anos_cliente": 1,
        "saldo_conta": 0.0,
        "numero_produtos": 2,
        "cartao_credito": 0,
        "membro_ativo": 1,
        "salario_estimado": 112542.58,
        "escore_credito": 502
    },
    {
        "pais": "França",
        "genero": "Feminino",
        "idade": 42,
        "anos_cliente": 8,
        "saldo_conta": 113755.78,
        "numero_produtos": 1,
        "cartao_credito": 1,
        "membro_ativo": 1,
        "salario_estimado": 149756.71,
        "escore_credito": 699
    },
    {
        "pais": "França",
        "genero": "Masculino",
        "idade": 39,
        "anos_cliente": 1,
        "saldo_conta": 0.0,
        "numero_produtos": 2,
        "cartao_credito": 0,
        "membro_ativo": 0,
        "salario_estimado": 93826.63,
        "escore_credito": 850
    },
    {
        "pais": "Espanha",
        "genero": "Masculino",
        "idade": 43,
        "anos_cliente": 2,
        "saldo_conta": 125510.82,
        "numero_produtos": 1,
        "cartao_credito": 1,
        "membro_ativo": 1,
        "salario_estimado": 79084.10,
        "escore_credito": 645
    }
]

def gerar_cliente_aleatorio():
    """Gera dados de cliente com variação aleatória"""
    base = random.choice(SAMPLE_CLIENTS).copy()
    
    # Adicionar variação
    base["idade"] += random.randint(-5, 5)
    base["saldo_conta"] *= random.uniform(0.5, 1.5)
    base["salario_estimado"] *= random.uniform(0.8, 1.2)
    base["escore_credito"] = max(300, min(850, base["escore_credito"] + random.randint(-50, 50)))
    
    return base

def fazer_predicao(client_id):
    """Faz uma requisição de predição"""
    try:
        cliente = gerar_cliente_aleatorio()
        
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/predict",
            json=cliente,
            timeout=10
        )
        latency = (time.time() - start_time) * 1000  # ms
        
        if response.status_code == 200:
            resultado = response.json()
            return {
                "id": client_id,
                "status": "success",
                "latency_ms": latency,
                "prediction": resultado["probabilidade_churn"],
                "risk": resultado["nivel_risco"]
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
    
    print("✅ API disponível!")
    
    # Configuração do teste
    print(f"\n📊 Configuração do teste:")
    print(f"   • Total de requisições: {NUM_REQUESTS}")
    print(f"   • Workers paralelos: {CONCURRENT_WORKERS}")
    print(f"   • Delay entre batches: {DELAY_BETWEEN_BATCHES}s")
    
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
        futures = [executor.submit(fazer_predicao, i) for i in range(NUM_REQUESTS)]
        
        for future in as_completed(futures):
            resultado = future.result()
            
            if resultado["status"] == "success":
                resultados["success"] += 1
                resultados["latencies"].append(resultado["latency_ms"])
                resultados["predictions"].append(resultado["prediction"])
                print(f"✅ Req {resultado['id']:3d} | {resultado['latency_ms']:6.1f}ms | Churn: {resultado['prediction']:.3f} | {resultado['risk']}")
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
    print(f"   • Prometheus: http://localhost:9090")
    print(f"   • Grafana: http://localhost:3000")
    print(f"   • Métricas da API: {API_URL}/metrics")
    print("="*70)

if __name__ == "__main__":
    executar_teste()
