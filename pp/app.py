import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load appointments from JSON file
with open("appointments.json", "r") as f:
    appointments = json.load(f)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Get all appointments
@app.route("/api/appointments")
def get_appointments():
    return jsonify(appointments)

# Get single appointment by ID
@app.route("/api/appointments/<apt_id>")
def get_appointment(apt_id):
    for apt in appointments:
        if apt["id"] == apt_id:
            return jsonify(apt)
    return jsonify({"error": "Appointment not found"}), 404

# Update appointment
@app.route("/api/appointments/<apt_id>", methods=["PUT"])
def update_appointment(apt_id):
    payload = request.get_json(silent=True) or {}
    for apt in appointments:
        if apt["id"] == apt_id:
            for key in ["patient", "doctor", "date", "time", "status"]:
                if key in payload:
                    apt[key] = payload[key]
            with open("appointments.json", "w") as f:
                json.dump(appointments, f, indent=2)
            return jsonify(apt)
    return jsonify({"error": "Appointment not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
