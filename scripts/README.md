# Scripts Auxiliares

Este diretório contém scripts para auxiliar no desenvolvimento, testes e operação do sistema de monitoramento.

## Scripts Disponíveis

### Monitoramento
- `start_monitoring.sh` - Inicia a stack de monitoramento (Prometheus + Grafana)
- `stop_monitoring.sh` - Para todos os containers de monitoramento

### Testes
- `test_api_load.py` - Executa testes de carga na API
- `export_metrics.py` - Exporta métricas do Prometheus

## Como Usar

```bash
# Dar permissão de execução aos scripts shell
chmod +x scripts/*.sh

# Executar um script
./scripts/start_monitoring.sh
```
