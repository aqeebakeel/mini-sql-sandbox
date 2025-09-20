from flask import Flask, request, jsonify, render_template
import sqlite3
import os

DB = "ieee_local.db"
TABLE = "enrichment"

app = Flask(__name__)

def get_columns():
    """Return list of columns dynamically from DB"""
    if not os.path.exists(DB):
        return []
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({TABLE});")
    cols = [row[1] for row in cur.fetchall()]
    conn.close()
    return cols

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.json or {}
    cmd = data.get("command", "").strip()
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # Executescript for multiple commands separated by ;
        if ";" in cmd.strip(";"):
            cur.executescript(cmd)
            conn.commit()
            conn.close()
            return jsonify({"status": "ok", "message": "Script executed successfully."})
        cur.execute(cmd)
        if cmd.lower().startswith("select"):
            rows = [dict(r) for r in cur.fetchall()]
            conn.commit()
            conn.close()
            return jsonify({"status": "ok", "rows": rows})
        else:
            conn.commit()
            conn.close()
            return jsonify({"status": "ok", "message": "Command executed successfully."})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

@app.route("/schema")
def schema():
    return jsonify({"columns": get_columns()})

if __name__ == "__main__":
    app.run(debug=True)
