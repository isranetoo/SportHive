"""
Script para importar apenas os dados de tênis do arquivo atp_tennis.csv
"""

import os
import sys

# Adicionar o diretório do backend ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a função de importação do módulo de migração
from import_data.migration import import_data, update_statistics

def main():
    """
    Função principal que importa dados de tênis do arquivo padrão ou de um arquivo especificado
    """
    # Definir caminho padrão para o arquivo
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    default_tennis_path = os.path.join(data_dir, "atp_tennis.csv")
    
    # Verificar se foi fornecido um caminho alternativo como argumento
    if len(sys.argv) > 1:
        tennis_path = sys.argv[1]
    else:
        tennis_path = default_tennis_path
    
    # Verificar se o arquivo existe
    if not os.path.exists(tennis_path):
        print(f"ERRO: Arquivo de tênis não encontrado em {tennis_path}")
        print(f"Certifique-se de que o arquivo existe ou forneça o caminho correto como argumento.")
        return 1
    
    print(f"Importando dados de tênis do arquivo: {tennis_path}")
    import_data(tennis_csv_path=tennis_path)
    
    # Perguntar se deseja atualizar estatísticas
    update_stats = input("Deseja atualizar as estatísticas após a importação? (s/n): ").lower() == 's'
    if update_stats:
        update_statistics()
    
    print("Importação concluída com sucesso!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
