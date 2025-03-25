## SportHive

## 🚀 React + FastAPI Starter

Este projeto é um exemplo básico de integração entre React (Frontend) e FastAPI (Backend).

## 🛠 Tecnologias Utilizadas

- **Frontend:** React (Vite, Axios)
- **Backend:** FastAPI (Uvicorn, CORS Middleware)
- **Comunicação:** Requisições HTTP via API REST

## 📦 Instalação e Uso

### 🔹 1. Configurar o Backend (Python + FastAPI)

Clone o repositório e entre na pasta do backend:

```bash
git clone https://github.com/isranetoo/SportHive.git
cd backend
```

Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

Instale as dependências:

```bash
pip install fastapi uvicorn
```

Inicie o servidor FastAPI:

```bash
uvicorn main:app --reload
```

O backend estará rodando em http://127.0.0.1:8000.

### 🔹 2. Configurar o Frontend (React + Vite)

Vá para a pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie o servidor do React:

```bash
npm run dev
```

Acesse http://localhost:5173 para visualizar o site.

## 🔄 Fluxo de Funcionamento

1. O React faz uma requisição para http://127.0.0.1:8000/api/dataset.
2. O FastAPI responde com um JSON contendo dados.
3. O React exibe os dados na interface.

## 📌 Melhorias Futuras

<!-- Aqui você pode adicionar melhorias planejadas para o projeto -->

## 📌 Contribuição

Sinta-se à vontade para contribuir e melhorar este projeto! 😃
