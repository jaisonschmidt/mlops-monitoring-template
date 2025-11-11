"""
Script para retreinamento do modelo com novos dados
"""
import pandas as pd
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

# Configurar logging
from utils.logger import setup_logger, logger
setup_logger("retraining")

def retreinar_com_novos_dados(arquivo_novos_dados="data/raw/dados_novos_1.csv"):
    """
    Combina dados de treino existentes com novos dados e prepara para retreino
    
    Args:
        arquivo_novos_dados: caminho para o arquivo com novos dados
    """
    logger.info("="*60)
    logger.info("Iniciando processo de retreinamento")
    logger.info("="*60)
    
    # Carregar dados existentes
    logger.info("Etapa 1: Carregando dados de treino existentes")
    dados_treino = pd.read_csv("data/raw/dados_treino.csv")
    logger.success(f"Registros no treino atual: {len(dados_treino)}")
    
    # Carregar novos dados
    logger.info(f"Etapa 2: Carregando novos dados de: {arquivo_novos_dados}")
    dados_novos = pd.read_csv(arquivo_novos_dados)
    logger.success(f"Registros novos: {len(dados_novos)}")
    
    # Combinar datasets
    logger.info("Etapa 3: Combinando datasets")
    dados_combinados = pd.concat([dados_treino, dados_novos], ignore_index=True)
    total_antes = len(dados_combinados)
    
    # Remover duplicatas se houver
    dados_combinados = dados_combinados.drop_duplicates()
    total_depois = len(dados_combinados)
    duplicatas_removidas = total_antes - total_depois
    
    if duplicatas_removidas > 0:
        logger.warning(f"Duplicatas removidas: {duplicatas_removidas}")
    
    logger.success(f"Total de registros após combinação: {total_depois}")
    
    # Fazer backup do arquivo original
    logger.info("Etapa 4: Criando backup do arquivo de treino original")
    backup_path = "data/raw/dados_treino_backup.csv"
    dados_treino.to_csv(backup_path, index=False)
    logger.success(f"Backup salvo em: {backup_path}")
    
    # Salvar novo arquivo de treino
    logger.info("Etapa 5: Salvando novo arquivo de treino")
    dados_combinados.to_csv("data/raw/dados_treino.csv", index=False)
    logger.success("Arquivo atualizado: data/raw/dados_treino.csv")
    
    logger.info("="*60)
    logger.success("DADOS PREPARADOS PARA RETREINO!")
    logger.info("="*60)
    logger.info("Próximo passo: Execute o script de treinamento:")
    logger.info("   python src/treinamento.py")
    logger.info("="*60)

if __name__ == "__main__":
    # Permite passar o arquivo de novos dados como argumento
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "data/raw/dados_novos_1.csv"
    
    retreinar_com_novos_dados(arquivo)
