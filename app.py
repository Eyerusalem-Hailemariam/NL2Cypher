import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASS = os.environ["NEO4J_PASS"]


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY
)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


def get_schema(session):
    labels = [record["label"] for record in session.run("CALL db.labels()")] 
    rel_types = [record["relationshipType"] for record in session.run("CALL db.relationshipTypes()")]
    property_keys = [record["propertyKey"] for record in session.run("CALL db.propertyKeys()")]
    return labels, rel_types, property_keys

def build_prompt(user_input, labels, rel_types, property_keys):
    labels_str = ", ".join(labels) if labels else "none"
    rels_str = ", ".join(rel_types) if rel_types else "none"
    props_str = ", ".join(property_keys) if property_keys else "none"
    return (
        f"You are a Cypher query generator. Only use the following labels: {labels_str}. "
        f"Only use the following relationships: {rels_str}. "
        f"Available property keys in the database: {props_str}.\n\n"
        "Instructions:\n"
        "- Output exactly one Cypher READ query (MATCH ... RETURN)\n"
        "- If the user specifies a number (e.g., '0', '5', '10'), apply it as a LIMIT in the query.\n"
        "- If the user says '0', use LIMIT 0 so no results are returned.\n"
        "- Do not explain, do not include any text other than the query, and do not use Markdown.\n"
        "- If the user text contains a typo in a property name, correct it to use one of the available property keys above.\n"
        "- Prefer concise property names and use numeric comparisons when appropriate.\n\n"
        f"User request: {user_input}\n\nCypher:"
    )


def _ask_llm_for_repair(original_cypher,labels, rel_types, property_keys, error_message=None, reason="EXPLAIN failed"):
    props_str = ", ".join(property_keys) if property_keys else "none"
    labels_str = ", ".join(labels) if labels else "none"
    rels_str = ", ".join(rel_types) if rel_types else "none"
    repair_prompt = (
        f"The database has labels: {labels_str}. Relationships: {rels_str}. Property keys: {props_str}.\n"
        f"A generated Cypher query (intended to answer the user's request) is: {original_cypher}\n"
        f"The query failed with: {error_message}\n" if error_message else ""
        f"Reason: {reason}.\n"
        "Please provide a corrected single Cypher READ query (MATCH ... RETURN) that will run against the schema above. "
        "Do NOT add any explanation or surrounding text — output only the corrected Cypher query."
    )
    repaired = llm.invoke(repair_prompt)
    return repaired.content.strip()

def results_to_text(rows):
    if not rows:
        return "No results found."

    def format_value(val):
        if hasattr(val, "items"):  
            return ", ".join(str(v) for v in val.values())
        return str(val)

    lines = []
    for r in rows:
        vals = [format_value(v) for v in r.values()]
        vals = [v for v in vals if v.strip()]
        lines.append(", ".join(vals))

    return "\n".join(lines)



def nl_to_cypher_and_run(user_input: str):
    with driver.session() as session:
        labels, rel_types, property_keys = get_schema(session)

    prompt_text = build_prompt(user_input, labels, rel_types, property_keys)
    cypher_raw = llm.invoke(prompt_text)
    cypher = cypher_raw.content.strip()

    with driver.session() as session:
        try:
            session.run("EXPLAIN " + cypher)
        except Exception as e:
            repaired = _ask_llm_for_repair(cypher, user_input, labels, rel_types, property_keys, error_message=str(e), reason="EXPLAIN failed")
            cypher = repaired
            try:
                session.run("EXPLAIN " + cypher)
            except Exception as e2:
                raise ValueError(f"EXPLAIN failed after repair: {e2} (original: {e})")

        rows = [dict(r) for r in session.run(cypher)]

    readable_text = results_to_text(rows)
    return cypher, readable_text

