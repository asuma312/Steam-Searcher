# 🎮 Steam Game Explorer & Recommender

Um sistema inteligente de recomendação de jogos da Steam usando **Processamento de Linguagem Natural (PLN)** e **Recuperação Aumentada por Geração (RAG)**. Coleta dados da Steam, armazena em **DuckDB** e permite buscas semânticas com linguagem natural.

---

## 🔧 Funcionalidades Principais

- 🔍 **Coleta de Dados da Steam**: Obtém informações detalhadas sobre jogos disponíveis na Steam.
- 🗃️ **Armazenamento com DuckDB**: Armazena eficientemente os dados localmente.
- 🤖 **Sistema de Recomendação RAGs**: Utiliza embeddings e LLMs para oferecer sugestões com base em descrições fornecidas.
- 💬 **Interface Natural**: Busque jogos com perguntas do tipo: "quero um jogo de estratégia medieval com elementos de RPG".

---

## 📦 Pré-requisitos

Certifique-se de ter:

- Python `3.7+`

---

## 🚀 Instalação

1. **Clone o repositório:**

```bash
git clone <url_do_seu_repositorio>
cd steam-game-explorer-recommender
```

2. **Crie e ative um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```
---

## ⚙️ Uso

### 1. Coletar e armazenar dados da Steam

Execute:

```bash
python app/services/routiones.py
```

Isso irá coletar informações como título, descrição e tags de jogos da Steam, salvando em `app/db/db_files/steam-searcher.duckdb`.

---

### TODO: Configurar o Sistema RAGs


---

### Objetivo final:

Após os dados e embeddings estarem prontos:

```bash
python main.py
```

O sistema entrará no modo de consulta interativa:

```
Bem-vindo ao Steam Game Explorer & Recommender!
Digite sua consulta (ou 'sair' para encerrar):

Você: quero um jogo de estratégia medieval com elementos de RPG
```

Resultados esperados:

```
Sugestões:
1. Crusader Kings III: Um jogo épico de estratégia de dinastia ambientado na Idade Média, com fortes elementos de RPG.
2. Mount & Blade II: Bannerlord: Mergulhe em um mundo medieval de fantasia com combate realista, gerenciamento de reino e oportunidades de RPG.
3. Total War: Medieval II: Experimente batalhas épicas em larga escala e gerenciamento estratégico em um cenário medieval detalhado.
```



---

## 🤝 Como Contribuir

Sinta-se à vontade para contribuir! Você pode:

- Melhorar a coleta de dados
- Otimizar performance das consultas
- Testar novos modelos de embedding e LLMs
- Adicionar filtros (gênero, preço, etc.)
- Melhorar a interface

Envie um Pull Request com suas melhorias 🚀

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**.