import os
import uvicorn

# Definir a variável de ambiente para usar SQLite
os.environ["USE_SQLITE"] = "True"

# Importar o app depois de definir a variável de ambiente
from main import app

if __name__ == "__main__":
    print("Executando a aplicação com SQLite para testes locais")
    uvicorn.run(app, host="127.0.0.1", port=8000)
