"""
Script para atualizar apenas as estatísticas de tênis no banco de dados
"""

import os
import sys
import argparse
import time
import importlib.util
from datetime import datetime

# Adicionar o diretório do backend ao path do Python
script_path = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.dirname(script_path)  # Subir um nível para o diretório backend
sys.path.append(backend_path)
print(f"Adicionado ao path: {backend_path}")

# Adicionar também o diretório import_data explicitamente
import_data_path = os.path.join(backend_path, "import_data")
if import_data_path not in sys.path:
    sys.path.append(import_data_path)
    print(f"Adicionado ao path: {import_data_path}")

# Importações do projeto
from database import SessionLocal
from import_data.migration import update_head_to_head_stats

def import_module_from_file(module_name, file_path):
    """
    Importa um módulo diretamente de um arquivo usando importlib
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        return None
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def update_tennis_statistics(verbose=False):
    """
    Atualiza todas as estatísticas relacionadas ao tênis no banco de dados
    
    Args:
        verbose: Se True, exibe mensagens detalhadas durante o processo
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando atualização das estatísticas de tênis...")
    start_time = time.time()
    
    # Definir as funções como None inicialmente
    update_player_tournament_stats = None
    calculate_initial_elo = None
    
    try:
        # Tentar importar usando várias abordagens
        try:
            # Abordagem 1: Importar como módulo normal
            if verbose:
                print("Tentando importar import_tennis_data como módulo...")
            from import_data.import_tennis_data import update_player_tournament_stats, calculate_initial_elo
            if verbose:
                print("✅ Importação bem-sucedida como módulo!")
        except ImportError as e1:
            if verbose:
                print(f"Falha na importação como módulo: {e1}")
            
            try:
                # Abordagem 2: Importar como módulo usando caminho absoluto
                import_tennis_data_path = os.path.join(import_data_path, "import_tennis_data.py")
                if os.path.exists(import_tennis_data_path):
                    if verbose:
                        print(f"Tentando importar diretamente do arquivo: {import_tennis_data_path}")
                    
                    tennis_data_module = import_module_from_file("import_tennis_data", import_tennis_data_path)
                    update_player_tournament_stats = getattr(tennis_data_module, "update_player_tournament_stats")
                    calculate_initial_elo = getattr(tennis_data_module, "calculate_initial_elo")
                    if verbose:
                        print("✅ Importação direta bem-sucedida!")
                else:
                    print(f"ERRO: Arquivo import_tennis_data.py não encontrado em {import_tennis_data_path}")
                    # Listar arquivos disponíveis para diagnóstico
                    if os.path.exists(import_data_path):
                        files = os.listdir(import_data_path)
                        print(f"Arquivos disponíveis em {import_data_path}: {', '.join(files)}")
                    return False
            except Exception as e2:
                print(f"Falha na tentativa de importação direta: {e2}")
                raise
        
        # Verificar se conseguimos importar as funções necessárias
        if update_player_tournament_stats is None or calculate_initial_elo is None:
            print("ERRO: Não foi possível importar as funções necessárias.")
            return False
            
        db = SessionLocal()
        try:
            # Etapa 1: Atualizar estatísticas de jogador-torneio
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 1/3 - Atualizando estatísticas jogador-torneio...")
            try:
                # Tentar com o parâmetro verbose
                if verbose:
                    print("Executando com modo verbose...")
                updated_pt = update_player_tournament_stats(db, verbose=verbose)
            except TypeError:
                # Se não aceitar o parâmetro verbose, chamar sem ele
                if verbose:
                    print("A função não suporta modo verbose, continuando sem ele...")
                updated_pt = update_player_tournament_stats(db)
            
            # Etapa 2: Atualizar estatísticas de confrontos diretos
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 2/3 - Atualizando estatísticas de confrontos diretos...")
            updated_h2h = update_head_to_head_stats(db)
            
            # Etapa 3: Recalcular rankings ELO
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 3/3 - Recalculando rankings ELO...")
            try:
                # Tentar com o parâmetro verbose
                updated_elo = calculate_initial_elo(db, verbose=verbose)
            except TypeError:
                # Se não aceitar o parâmetro verbose, chamar sem ele
                if verbose:
                    print("A função de cálculo ELO não suporta modo verbose, continuando sem ele...")
                updated_elo = calculate_initial_elo(db)
            
            # Commit das alterações
            db.commit()
            
            elapsed_time = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Atualização concluída com sucesso em {elapsed_time:.2f} segundos!")
            print(f"  - Estatísticas jogador-torneio: {updated_pt if updated_pt is not None else 'N/A'} registros")
            print(f"  - Confrontos diretos: {updated_h2h if updated_h2h is not None else 'N/A'} partidas processadas")
            print(f"  - Rankings ELO: {updated_elo if updated_elo is not None else 'N/A'} jogadores atualizados")
            return True
            
        except Exception as e:
            db.rollback()
            print(f"❌ Erro ao atualizar estatísticas: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Erro ao inicializar módulos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atualiza apenas as estatísticas de tênis no banco de dados")
    parser.add_argument("-v", "--verbose", action="store_true", help="Exibe mensagens detalhadas durante o processo")
    parser.add_argument("--quick", action="store_true", help="Executa uma atualização rápida (pula recálculo de ELO)")
    
    args = parser.parse_args()
    
    success = update_tennis_statistics(verbose=args.verbose)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
