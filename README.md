# NL2Cypher

Natural language to Cypher demo using Flask, Neo4j, and a generative model.

## Setup

1. Create a Python virtual environment and install dependencies:

```
pip install -r requirements.txt
```

2. Configure environment variables. Copy `.env.example` to `.env` and fill in your values:

```
cp .env.example .env
```

Required variables in `.env`:
- `GOOGLE_API_KEY`
- `NEO4J_URI` (e.g., `bolt://localhost:7687`)
- `NEO4J_USER`
- `NEO4J_PASS`

> Note: `.env` is ignored by git via `.gitignore` to prevent committing secrets.

3. Run the app:

```
python flask_app.py
```

Open `http://localhost:5000` in your browser.
