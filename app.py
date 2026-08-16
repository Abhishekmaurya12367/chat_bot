import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# ── Add bot folder to Python path ────────────────────────────
ROOT_DIR = Path(__file__).parent.resolve()
BOT_DIR = ROOT_DIR / "bot"
sys.path.insert(0, str(BOT_DIR))

# Import the RAG chain
from rag_chain import rag_chain

# ── Flask Application ─────────────────────────────────────────
app = Flask(__name__, template_folder=str(ROOT_DIR / "templates"))


@app.route("/")
def index():
    """Render the chat interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """API endpoint for chat queries."""
    data = request.get_json(force=True, silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question cannot be empty."}), 400

    try:
        print(f"\n[Web Query] Received: '{question}'", flush=True)
        answer = rag_chain(question)
        print(f"[Web Query] Generated answer ({len(answer)} chars)", flush=True)
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        print(f"[Web Query Error] {e}", flush=True)
        return jsonify({"error": f"Failed to generate answer: {str(e)}"}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "GovScheme AI Chatbot"})


if __name__ == "__main__":
    print("\n=======================================================")
    print("🚀 GovScheme AI Web App Running!")
    print("🌐 Open in your browser: http://127.0.0.1:5000")
    print("=======================================================\n", flush=True)
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
