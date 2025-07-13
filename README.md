# 🎮 SteamSearcher - Steam Game Explorer & Recommender

Um sistema inteligente de busca e recomendação de jogos Steam que utiliza **Processamento de Linguagem Natural (NLP)** e **Retrieval-Augmented Generation (RAG)** para descobrir jogos baseado em descrições em linguagem natural.

---

## 🔧 Principais Funcionalidades

- 🔍 **Coleta de Dados Steam**: Obtém informações detalhadas sobre jogos disponíveis na plataforma Steam
- 🗃️ **Armazenamento DuckDB**: Armazena os dados coletados de forma eficiente localmente
- 🤖 **Sistema de Recomendação RAG**: Usa embeddings e LLMs para sugerir jogos baseado em descrições fornecidas pelo usuário
- 💬 **Interface em Linguagem Natural**: Permite buscar jogos com prompts como: "Quero um jogo de estratégia medieval com elementos de RPG"
- 🎨 **Interface Web Moderna**: Frontend React com design responsivo e experiência de usuário intuitiva
- ⚡ **API REST**: Backend Flask para comunicação entre frontend e sistema de busca

---

## 🏗️ Arquitetura

### Backend (Python/Flask)
- **Crawlers**: Coleta dados da API Steam
- **Processamento**: Transforma e limpa os dados coletados
- **Embeddings**: Gera embeddings usando OpenAI para busca semântica
- **API**: Endpoints REST para busca de jogos

### Frontend (React/TypeScript)
- **Interface de Busca**: Página principal com campo de busca intuitivo
- **Resultados**: Exibição de jogos com informações detalhadas
- **Design Responsivo**: Funciona perfeitamente em desktop e mobile

### Banco de Dados
- **DuckDB**: Armazenamento local eficiente
- **Embeddings**: Busca vetorial para recomendações semânticas

---

## 📦 Pré-requisitos

- Python `3.7+`
- Node.js `16+`
- Chave da API OpenAI (para embeddings)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <your_repository_url>
cd steam-game-explorer-recommender
```

### 2. Configure o Backend

```bash
# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
PROXY=seu_proxy_se_necessario
PROXY_AUTH=auth_do_proxy_se_necessario
```

### 4. Configure o Frontend

```bash
cd app/frontend
npm install
```

Crie um arquivo `.env` em `app/frontend`:

```env
VITE_BACKEND_URL=http://localhost:5000
```

---

## ⚙️ Uso

### 1. Colete e processe dados do Steam

```bash
# Colete dados dos jogos
python app/services/routines.py

# Processe e transforme os dados
python app/services/transformer.py

# Gere embeddings para busca semântica
python app/services/embedder.py
```

Este processo irá:
- Coletar informações de jogos do Steam
- Processar e limpar os dados
- Salvar no banco DuckDB (`app/db/db_files/steam-searcher.duckdb`)
- Gerar embeddings para busca semântica

### 2. Inicie o Backend

```bash
python run.py
```

O servidor Flask estará rodando em `http://localhost:5000`

### 3. Inicie o Frontend

```bash
cd app/frontend
npm run dev
```

A aplicação web estará disponível em `http://localhost:5173`

### 4. Use a Aplicação

1. Acesse `http://localhost:5173`
2. Digite sua busca em linguagem natural, como:
   - "Jogos de estratégia medieval com elementos RPG"
   - "Jogos de corrida arcade divertidos"
   - "RPGs com mundo aberto e crafting"
3. Veja os resultados com informações detalhadas dos jogos

---

## 🎯 Exemplos de Busca

A aplicação entende buscas em linguagem natural:

```
"Quero um jogo de estratégia medieval com elementos de RPG"
```

Resultados esperados:
- Crusader Kings III
- Mount & Blade II: Bannerlord
- Total War: Medieval II

```
"Jogos indie de plataforma com pixel art"
```

Resultados esperados:
- Celeste
- Hollow Knight
- Dead Cells

---

## 📁 Estrutura do Projeto

```
├── app/
│   ├── crawlers/          # Coleta de dados Steam
│   ├── db/               # Configuração banco de dados
│   ├── frontend/         # Aplicação React
│   ├── models/           # Modelos de dados
│   ├── routes/           # Rotas da API
│   ├── services/         # Lógica de negócio
│   └── utils/            # Utilitários
├── run.py               # Servidor Flask
└── requirements.txt     # Dependências Python
```

---

## 🔧 API Endpoints

### POST `/api/search`
Busca jogos baseado em query em linguagem natural.

**Request:**
```json
{
  "query": "jogos de estratégia medieval"
}
```

**Response:**
```json
[
  {
    "id": 428020,
    "name": "Crusader Kings III",
    "description": "Paradox Development Studio brings you the sequel to one of the most popular strategy games ever made.",
    "price": 49.99,
    "image": "https://cdn.akamai.steamstatic.com/steam/apps/428020/header.jpg",
    "link": "https://store.steampowered.com/app/428020",
    "pc_requirements": {...},
    "genres": ["Strategy", "Simulation"],
    "categories": ["Single-player", "Multi-player"]
  }
]
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Você pode:

- Melhorar a coleta de dados Steam
- Otimizar performance das consultas
- Experimentar com diferentes modelos de embedding
- Adicionar filtros (gênero, preço, etc.)
- Melhorar a interface do usuário
- Adicionar testes automatizados

Envie um Pull Request com suas melhorias 🚀

---

## 🔮 Próximas Funcionalidades

- [ ] Filtros avançados (preço, gênero, avaliações)
- [ ] Sistema de favoritos
- [ ] Recomendações personalizadas baseadas no histórico
- [ ] Integração com outras plataformas de jogos
- [ ] Cache inteligente para melhor performance
- [ ] Modo offline para buscas

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**.

---

## 🛠️ Tecnologias Utilizadas

**Backend:**
- Python 3.7+
- Flask
- DuckDB
- OpenAI Embeddings
- BeautifulSoup
- Pandas/Polars

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Vite
- React Router

**Infraestrutura:**
- DuckDB (banco de dados)
- OpenAI API (embeddings)
- Steam API (dados dos jogos)