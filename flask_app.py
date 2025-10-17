from flask import Flask, render_template, request, jsonify
from app import nl_to_cypher_and_run

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_input = request.form.get("question")

    try:
        cypher, readable_text = nl_to_cypher_and_run(user_input)
        return jsonify({"result": readable_text, "cypher": cypher})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

