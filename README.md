# NL2Cypher

Convert natural language questions into Cypher queries and view results instantly.

## Features
- Modern Flask web app for NL-to-Cypher conversion
- Uses Neo4j as the backend graph database
- Google Generative AI (Gemini) for query generation
- Displays generated Cypher and query results

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Eyerusalem-Hailemariam/NL2Cypher.git
   cd NL2Cypher/text-to-cypher
   ```

2. **Create a Python virtual environment and install dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your values:
     ```bash
     cp .env.example .env
     ```
   - Required variables in `.env`:
     - `GOOGLE_API_KEY` (Google Gemini API key)
     - `NEO4J_URI` (e.g., `bolt://localhost:7687`)
     - `NEO4J_USER` (Neo4j username)
     - `NEO4J_PASS` (Neo4j password)


4. **Run the app**
   ```bash
   python flask_app.py
   ```
   - Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage
- Enter a natural language question (e.g., "Which directors worked on more than one Matrix movie?")
- Click **Ask** to generate and run the Cypher query
- View results and the raw Cypher query


