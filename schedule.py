import requests
import json

# API URL
url = "http://127.0.0.1:5000/therapists/availability"

# Input data for multiple therapists
data = {
    "therapists": [
        {
            "name": "Dr. A",
            "shift_start": [9, 30],
            "shift_end": [18, 0],
            "appointments": [
                [[12, 0], [13, 0]],
                [[15, 0], [16, 0]]
            ]
        },
        {
            "name": "Dr. B",
            "shift_start": [10, 0],
            "shift_end": [17, 0],
            "appointments": [
                [[11, 0], [12, 0]],
                [[14, 0], [15, 0]]
            ]
        }
    ]
}


response = requests.post(url, json=data)



with open("therapist_availability_output.json", "w") as f:
    json.dump(response.json(), f, indent=4)

print("\nResponse saved to 'therapist_availability_output.json'")
