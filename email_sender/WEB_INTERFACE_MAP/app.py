from flask import Flask, render_template, jsonify
import json
from utils import geocode_address, compute_distance_matrix
from scheduler import greedy_scheduler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-scheduler")
def run_scheduler():
    with open("database.json", "r") as f:
        data = json.load(f)

    # Add lat/lng if missing
    for t in data["therapists"]:
        if "lat" not in t:
            t["lat"], t["lng"] = geocode_address(t["address"])
    for p in data["patients"]:
        if "lat" not in p:
            p["lat"], p["lng"] = geocode_address(p["address"])

    # Compute distances
    data["distances"] = compute_distance_matrix(data["therapists"], data["patients"])

    # Run scheduling
    schedule = greedy_scheduler(data)

    # Save results
    with open("schedule.json", "w") as f:
        json.dump({"schedule": schedule, "data": data}, f, indent=4)

    return jsonify({"schedule": schedule, "therapists": data["therapists"], "patients": data["patients"]})

if __name__ == "__main__":
    app.run(debug=True)
