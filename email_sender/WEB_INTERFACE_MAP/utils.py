import requests
import json

API_KEY = "AIzaSyAt-jeXSXhU7dMBeIisv991Fb33O9s_bbM"

def geocode_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url).json()
    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None

def compute_distance_matrix(therapists, patients):
    origins = [t["address"] for t in therapists]
    destinations = [p["address"] for p in patients]

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(origins),
        "destinations": "|".join(destinations),
        "key": API_KEY
    }
    response = requests.get(url, params=params).json()

    distances = {}
    for i, t in enumerate(therapists):
        tid = t["id"]
        distances[tid] = {}
        for j, p in enumerate(patients):
            pid = p["id"]
            element = response["rows"][i]["elements"][j]
            distances[tid][pid] = {
                "distance_km": element["distance"]["value"] / 1000,
                "duration_min": element["duration"]["value"] // 60
            }
    return distances
