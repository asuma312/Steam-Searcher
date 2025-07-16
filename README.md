# 🎮 SteamSearcher - Steam Game Explorer & Recommender

An intelligent Steam game search and recommendation system that uses **Natural Language Processing (NLP)** and **Retrieval-Augmented Generation (RAG)** to discover games based on natural language descriptions.

---

## 🔧 Key Features

- 🔍 **Steam Data Collection**: Gathers detailed information about games available on the Steam platform.
- 🗃️ **DuckDB Storage**: Efficiently stores the collected data locally.
- 🤖 **RAG Recommendation System**: Uses embeddings and LLMs to suggest games based on user-provided descriptions.
- 💬 **Natural Language Interface**: Allows searching for games with prompts like: "I want a medieval strategy game with RPG elements."
- 🎨 **Modern Web Interface**: React frontend with a responsive design and intuitive user experience.
- ⚡ **REST API**: Flask backend for communication between the frontend and the search system.

---

## 🏗️ Architecture

### Backend (Python/Flask)
- **Crawlers**: Collects data from the Steam API.
- **Processing**: Transforms and cleans the collected data.
- **Embeddings**: Generates embeddings using OpenAI for semantic search.
- **API**: REST endpoints for game searches.

### Frontend (React/TypeScript)
- **Search Interface**: Main page with an intuitive search field.
- **Results**: Displays games with detailed information.
- **Responsive Design**: Works perfectly on desktop and mobile.

### Database
- **DuckDB**: Efficient local storage.
- **Embeddings**: Vector search for semantic recommendations.

---

## 📦 Prerequisites

- Python `3.7+`
- Node.js `16+`
- OpenAI API Key (for embeddings)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your_repository_url>
cd steam-game-explorer-recommender
```

### 2. Configure the Backend

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key_here
PROXY=your_proxy_if_needed
PROXY_AUTH=proxy_auth_if_needed
```

### 4. Configure the Frontend

```bash
cd app/frontend
npm install
```

Create a `.env` file in `app/frontend`:

```env
VITE_BACKEND_URL=http://localhost:5000
```

---

## ⚙️ Usage

### 1. Collect and process Steam data

You can download the dataset in kaggle and create your own duckdb:
[Steam Searcher Dataset](https://www.kaggle.com/datasets/lucasbuenogodoy/steam-searcher-dataset)

Or you can run the specific Kaggle collector to create & update your db:
```bash
python kaggle_collector.py
```

### 2. Start the Backend

```bash
python run.py
```

The Flask server will be running at `http://localhost:5000`

### 3. Start the Frontend

```bash
cd app/frontend
npm run dev
```

The web application will be available at `http://localhost:5173`

### 4. Use the Application

1. Access `http://localhost:5173`
2. Type your search in natural language, such as:
   - "Medieval strategy games with RPG elements"
   - "Fun arcade racing games"
   - "RPGs with open world and crafting"
3. See the results with detailed information about the games.

---

## 🎯 Search Examples

The application understands natural language searches:

```
"I want a medieval strategy game with RPG elements"
```

Expected results:
- Crusader Kings III
- Mount & Blade II: Bannerlord
- Total War: Medieval II

```
"Indie platformer games with pixel art"
```

Expected results:
- Celeste
- Hollow Knight
- Dead Cells

---

## 📁 Project Structure

```
├── app/
│   ├── crawlers/          # Steam data collection
│   ├── db/               # Database configuration
│   ├── frontend/         # React application
│   ├── models/           # Data models
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   └── utils/            # Utilities
├── run.py               # Flask server
└── requirements.txt     # Python dependencies
```

---

## 🔧 API Endpoints

### POST `/api/search`
Searches for games based on a natural language query.

**Request:**```json
{
  "query": "medieval strategy games"
}
```

**Response:**
```json
[
  {
    "id": 1158310,
    "name": "Crusader Kings III",
    "description": "Paradox Development Studio brings you the sequel to one of the most popular strategy games ever made.",
    "price": 49.99,
    "image": "https://cdn.akamai.steamstatic.com/steam/apps/1158310/header.jpg",
    "link": "https://store.steampowered.com/app/1158310",
    "pc_requirements": {...},
    "genres": ["Strategy", "Simulation"],
    "categories": ["Single-player", "Multi-player"]
  }
]
```

---

## 🤝 Contributing

Contributions are welcome! You can:

- Improve Steam data collection
- Optimize query performance
- Experiment with different embedding models
- Add filters (genre, price, etc.)
- Enhance the user interface
- Add automated tests

Submit a Pull Request with your improvements 🚀

---

## 🔮 Upcoming Features

- [X] Advanced filters (price, genre, ratings)
- [ ] Smart caching for better performance

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🛠️ Technologies Used

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

**Infrastructure:**
- DuckDB (database)
- OpenAI API (embeddings)
- Steam API (game data)