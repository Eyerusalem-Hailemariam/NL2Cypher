**Natural Language → Cypher Query Generator

  Convert plain English questions into Cypher queries and run them on a Neo4j database using Gemini via LangChain. 
  Explore graph data without writing Cypher manually, and get results returned in plain English.

** Features**

- Translate natural language to Cypher queries

- Auto-correct typos in labels/properties

- Schema-aware query prompts

- Automatic query repair if invalid

- Returns clean, readable results

**Tech Stack**

- Neo4j – Graph database

- LangChain – LLM orchestration

- Gemini – LLM API

- Python 3.10+

**Installation**

  git clone https://github.com/your-username/nl2cypher.git
  cd nl2cypher
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt


**Create a .env file:**

GOOGLE_API_KEY=your_gemini_api_key
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=your_password

**Usage**

python flask_app.py


**How It Works**

- Extract schema from Neo4j

- Build prompt with schema + user input

- Generate Cypher using Gemini

- Validate & repair query

- Return formatted results
