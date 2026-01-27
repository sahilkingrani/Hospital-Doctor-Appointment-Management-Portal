import os
import json
from flask import Flask, render_template, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "appointments.json")

app = Flask(__name__)
with open(DATA_PATH, "r", encoding="utf-8") as f:
    appointments = json.load(f)
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/appointments", methods=["GET", "POST"])
def get_appointments():
    
    if request.method == "GET":
        return jsonify(appointments)
   
    payload = request.get_json(silent=True) or {}
    
    required = ["patient", "doctor", "date", "time", "status"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    
    existing_ids = {a.get("id") for a in appointments if a.get("id")}
    new_id = payload.get("id")
    if not new_id or new_id in existing_ids:
        
        def parse_num(i):
            try:
                return int(str(i).replace("APT", ""))
            except Exception:
                return 0
        max_num = max([parse_num(i) for i in existing_ids], default=0)
        new_id = f"APT{max_num + 1:03d}"
    payload["id"] = new_id

    
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            current = json.load(f)
        if not isinstance(current, list):
            current = []
        current.append(payload)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(current, f, ensure_ascii=False, indent=2)
        # Update in-memory list so subsequent GET reflects the change
        appointments.append(payload)
        return jsonify({"message": "Saved successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to save: {e}"}), 500


@app.route("/api/appointments/<appt_id>")
def get_appointment(appt_id):
    for appt in appointments:
        if appt["id"] == appt_id:
            return jsonify(appt)
    return jsonify({"error": "Appointment not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5900)
