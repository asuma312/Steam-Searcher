# 🎮 Steam Game Explorer & Recommender

An intelligent recommendation system for Steam games using **Natural Language Processing (NLP)** and **Retrieval-Augmented Generation (RAG)**. It collects data from Steam, stores it in **DuckDB**, and allows users to search for games using natural language.

---

## 🔧 Main Features

- 🔍 **Steam Data Collection**: Retrieves detailed information about games available on the Steam platform.
- 🗃️ **DuckDB Storage**: Efficiently stores the collected data locally.
- 🤖 **RAG-Based Recommendation System**: Uses embeddings and LLMs to suggest games based on user-provided descriptions.
- 💬 **Natural Language Interface**: Enables users to search for games with prompts like: “I want a medieval strategy game with RPG elements.”

---

## 📦 Prerequisites

Make sure you have:

- Python `3.7+`

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone <your_repository_url>
cd steam-game-explorer-recommender
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 1. Collect and store Steam data

Run:

```bash
python app/services/routiones.py
```

This will collect game information such as title, description, and tags from Steam and save it to `app/db/db_files/steam-searcher.duckdb`.

---

### TODO: Configure the RAG System

> This section is still under development.

---

### Final Goal

Once the data and embeddings are ready:

```bash
python main.py
```

The system will enter interactive query mode:

```
Welcome to Steam Game Explorer & Recommender!
Enter your query (or 'exit' to quit):

You: I want a medieval strategy game with RPG elements
```

Expected results:

```
Suggestions:
1. Crusader Kings III: An epic medieval dynasty strategy game with strong RPG elements.
2. Mount & Blade II: Bannerlord: Dive into a medieval fantasy world with realistic combat, kingdom management, and RPG opportunities.
3. Total War: Medieval II: Experience epic large-scale battles and strategic management in a detailed medieval setting.
```

---

## 🤝 Contributing

Feel free to contribute! You can:

- Improve Steam data collection
- Optimize query performance
- Experiment with different embedding models and LLMs
- Add filters (genre, price, etc.)
- Improve the user interface

Submit a Pull Request with your improvements 🚀

---

## 📄 License

This project is licensed under the **MIT License**.