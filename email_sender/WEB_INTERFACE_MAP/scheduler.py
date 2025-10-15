import json

def greedy_scheduler(data):
    schedule = {}
    therapists = data["therapists"]
    patients = data["patients"]
    distances = data["distances"]

    for t in therapists:
        tid = t["id"]
        schedule[tid] = []
        available_patients = [p for p in patients if p["therapy"] == t["therapy"] and p["shift"] == t["shift"]]

        total_time = 0
        visited = set()

        while available_patients and len(schedule[tid]) < 5:
            nearest_patient = min(
                available_patients,
                key=lambda p: distances[tid][p["id"]]["duration_min"]
            )
            pid = nearest_patient["id"]

            travel_time = distances[tid][pid]["duration_min"]
            if total_time + travel_time + 60 > 480:  # 8-hour shift
                break

            schedule[tid].append(pid)
            visited.add(pid)
            available_patients = [p for p in available_patients if p["id"] not in visited]
            total_time += travel_time + 60

    return schedule
