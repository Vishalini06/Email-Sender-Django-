let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 11.0168, lng: 76.9558 }, // Coimbatore center
    zoom: 12
  });
}

async function runScheduler() {
  const response = await fetch("/run-scheduler");
  const result = await response.json();
  console.log("Scheduler result:", result); // Debug

  const schedule = result.schedule;
  const therapists = result.therapists;
  const patients = result.patients;

  displayRoutes(schedule, therapists, patients);
}

function displayRoutes(schedule, therapists, patients) {
  const colors = ["red", "yellow", "violet"];
  let therapistIndex = 0;

  for (const therapistName in schedule) {
    const assignedPatients = schedule[therapistName];
    const color = colors[therapistIndex % colors.length];

    // Match therapist object
    let therapist = therapists.find(t => therapistName.includes(t.name));
    if (!therapist) continue;

    let origin = { lat: therapist.lat, lng: therapist.lng };

    // Add a marker for the therapist
    new google.maps.Marker({
      position: origin,
      map: map,
      label: therapist.name,
      icon: { url: "http://maps.google.com/mapfiles/ms/icons/" + color + "-dot.png" }
    });

    assignedPatients.forEach(patientName => {
      let patient = patients.find(p => p.name === patientName);
      if (!patient) return;

      const directionsService = new google.maps.DirectionsService();
      const directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: false,
        polylineOptions: { strokeColor: color, strokeWeight: 5 }
      });
      directionsRenderer.setMap(map);

      directionsService.route(
        {
          origin: origin,
          destination: { lat: patient.lat, lng: patient.lng },
          travelMode: google.maps.TravelMode.DRIVING
        },
        (result, status) => {
          if (status === "OK") {
            directionsRenderer.setDirections(result);
          } else {
            console.error("Directions request failed:", status);
          }
        }
      );

      // Update origin → next patient
      origin = { lat: patient.lat, lng: patient.lng };

      // Add a marker for the patient
      new google.maps.Marker({
        position: origin,
        map: map,
        label: patient.name
      });
    });

    therapistIndex++;
  }
}

window.onload = initMap;
