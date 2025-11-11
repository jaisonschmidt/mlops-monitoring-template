"""
Script para retreinamento do modelo com novos dados
"""
import pandas as pd
import sys

def retreinar_com_novos_dados(arquivo_novos_dados="data/raw/dados_novos_1.csv"):
    """
    Combina dados de treino existentes com novos dados e prepara para retreino
    
    Args:
        arquivo_novos_dados: caminho para o arquivo com novos dados
    """
    print("=== Retreinamento do Modelo ===\n")
    
    # Carregar dados existentes
    print("1. Carregando dados de treino existentes...")
    dados_treino = pd.read_csv("data/raw/dados_treino.csv")
    print(f"   - Registros no treino atual: {len(dados_treino)}")
    
    # Carregar novos dados
    print(f"\n2. Carregando novos dados de: {arquivo_novos_dados}")
    dados_novos = pd.read_csv(arquivo_novos_dados)
    print(f"   - Registros novos: {len(dados_novos)}")
    
    # Combinar datasets
    print("\n3. Combinando datasets...")
    dados_combinados = pd.concat([dados_treino, dados_novos], ignore_index=True)
    
    # Remover duplicatas se houver
    dados_combinados = dados_combinados.drop_duplicates()
    print(f"   - Total de registros após combinação: {len(dados_combinados)}")
    
    # Fazer backup do arquivo original
    print("\n4. Criando backup do arquivo de treino original...")
    dados_treino.to_csv("data/raw/dados_treino_backup.csv", index=False)
    print("   - Backup salvo em: data/raw/dados_treino_backup.csv")
    
    # Salvar novo arquivo de treino
    print("\n5. Salvando novo arquivo de treino...")
    dados_combinados.to_csv("data/raw/dados_treino.csv", index=False)
    print("   - Arquivo atualizado: data/raw/dados_treino.csv")
    
    print("\n✅ Dados preparados para retreino!")
    print("\nPróximo passo: Execute o script de treinamento:")
    print("   python src/treinamento.py")

if __name__ == "__main__":
    # Permite passar o arquivo de novos dados como argumento
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "data/raw/dados_novos_1.csv"
    
    retreinar_com_novos_dados(arquivo)
