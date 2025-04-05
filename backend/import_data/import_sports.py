"""
Script para importar apenas os dados de esportes do arquivo sports.json
"""

import os
import sys

# Adicionar o diretório do backend ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a função de importação do módulo de migração
from import_data.migration import import_data

def main():
    """
    Função principal que importa dados de esportes do arquivo padrão ou de um arquivo especificado
    """
    # Definir caminho padrão para o arquivo
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    default_sports_path = os.path.join(data_dir, "sports.json")
    
    # Verificar se foi fornecido um caminho alternativo como argumento
    if len(sys.argv) > 1:
        sports_path = sys.argv[1]
    else:
        sports_path = default_sports_path
    
    # Verificar se o arquivo existe
    if not os.path.exists(sports_path):
        print(f"ERRO: Arquivo de esportes não encontrado em {sports_path}")
        print(f"Certifique-se de que o arquivo existe ou forneça o caminho correto como argumento.")
        return 1
    
    print(f"Importando dados de esportes do arquivo: {sports_path}")
    import_data(sports_json_path=sports_path)
    
    print("Importação concluída com sucesso!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
