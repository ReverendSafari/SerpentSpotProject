//
// @ Safari
// 
// Resources used: 
// https://developers.google.com/maps/documentation/javascript/overview
// https://github.com/catdad/canvas-confetti

/*
  This script is responsible for initializing the Google Maps API and handling the map interactions.
*/

let map; // This will hold the map object
let currentInfoWindow = null; // This will hold the currently open info window

// Initialize the map when the page has loaded
async function initMap() {
    const center = {lat: 27.3361, lng: -82.5307 }; // Central point for the map
    // Dynamically load the Maps and Marker libraries
    const {Map} = await google.maps.importLibrary("maps");
    const {AdvancedMarkerElement} = await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("map"), {
    zoom: 8,
    center: center,
    mapId: "92b4876303f4f956",  
    disableDoubleClickZoom: true
});

    // Add a double click listener to the map
    //Drops a pin on location and passes coordinates to the form
    map.addListener('dblclick', function (e) {
    placeMarkerAndPanTo(e.latLng, map);
    document.getElementById('latitude').value = e.latLng.lat();
    document.getElementById('longitude').value = e.latLng.lng();
        });
}

/*
Places a marker on the map and pans to the location
    @param {google.maps.LatLng} latLng - The latitude and longitude of the location
    @param {google.maps.Map} map - The map object
*/
async function placeMarkerAndPanTo(latLng, map) {
    if (window.marker) window.marker.setMap(null);
    const {AdvancedMarkerElement} = await google.maps.importLibrary("marker");
    window.marker = new AdvancedMarkerElement({
    position: latLng,
    map: map
    });

    map.panTo(latLng);
}


/*
This function fetches the observations from the back end and displays them on the map.

No args, No return
*/
function fetchData() {
    var submitButton = document.querySelector('button[type="submit"]');
    var lat = document.getElementById('latitude').value;
    var lng = document.getElementById('longitude').value;
    var radiusInMiles = document.getElementById('radius').value; // Get the radius in miles
    var radiusInKm = radiusInMiles * 1.60934; // Convert radius to kilometers
    var dateRange = document.getElementById('dateRange').value;  // Get the selected date range
    var url = `/snakemap/map_view?latitude=${lat}&longitude=${lng}&radius=${radiusInKm}&date_range=${dateRange}`;

    // Disable the button and change the text to show loading spinner
    submitButton.innerHTML = 'Loading... <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    submitButton.disabled = true;

    fetch(url)
        .then(response => response.json())
        .then(data => {
        console.log('Data received:', data);
        drawSearchArea(new google.maps.LatLng(lat, lng), radiusInKm);

        var observationsCount = data.observations.length;
        var observationCountElement = document.getElementById('observationCount');
        var hrElement = document.getElementById('dynamicHr');

        if (observationsCount > 0) {
            observationCountElement.textContent = `Snakemap found ${observationsCount} observations in the area.`;
            hrElement.style.display = 'block'; // Show the HR if there are observations
            console.log('Throwing confetti!', confetti)
            throwConfetti(); // Fire off the confetti effect
        } else {
            observationCountElement.textContent = 'No observations found.';
            hrElement.style.display = 'none'; // Hide the HR if there are no observations
        }

        // Clear existing markers if any
        if (window.markers) {
        window.markers.forEach(marker => marker.setMap(null));
                    }
        window.markers = [];

         // Create a marker for each observation received
        data.observations.forEach(obs => {
            const obsPos = {lat: obs.coordinates[1], lng: obs.coordinates[0] }; // Note the order of coordinates [lng, lat]
            const marker = new google.maps.Marker({
                position: obsPos,
            map: map,
            title: `${obs.common_name} (${obs.scientific_name})`
                                });
            window.markers.push(marker);
   
        // Create an info window for each marker
        const infoWindow = new google.maps.InfoWindow({
            content: `<div><strong>${obs.common_name}</strong><br>Scientific Name: ${obs.scientific_name}<br>Coordinates: ${obs.coordinates[1]}, ${obs.coordinates[0]}</div>`
            });


        // Add a click listener to the marker
        marker.addListener('click', function () {
        // Close the current info window if it exists
        if (currentInfoWindow) {
            currentInfoWindow.close();
        }
        // Open the new info window
        infoWindow.open(map, marker);
        // Update the reference to the current info window
        currentInfoWindow = infoWindow;
        });
               });
        // Restore the original button text and enable it again
        submitButton.innerHTML = 'Find Observations';
        submitButton.disabled = false;
                })            
            .catch(error => {
        console.error('Error fetching data:', error);
            });
        }


/*
Function to draw a circular radius around given coordinates

@param {google.maps.LatLng} center - The center of the circle
@param {number} radiusInKm - The radius of the circle in kilometers

No return
*/

function drawSearchArea(center, radiusInKm) {
   if (window.circle) window.circle.setMap(null); // Remove the previous circle if it exists
      window.circle = new google.maps.Circle({
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: map,
      center: center,
      radius: radiusInKm * 1000  // Radius in meters
   });
}


/*
Presets for the confetti effect
*/
var snakeEmoji = confetti.shapeFromText({ text: '🐍', scalar: 2 });

var defaults = {
   spread: 360,
   ticks: 60,
   gravity: 0,
   decay: 0.96,
   startVelocity: 20,
   shapes: [snakeEmoji],
   scalar: 2
};

/*
Function to throw the confetti effect on the screen

No args, No return
*/

function throwConfetti() {
   confetti({
      ...defaults,
      particleCount: 30
   });

   confetti({
      ...defaults,
      particleCount: 5,
      flat: true
   });

   confetti({
      ...defaults,
      particleCount: 15,
      scalar: 1,
      shapes: ['circle'] // Mixing snake emojis with circles
   });

   // Fire off confetti at intervals
   setTimeout(() => confetti({ ...defaults, particleCount: 20 }), 100);
   setTimeout(() => confetti({ ...defaults, particleCount: 20 }), 200);
   setTimeout(() => confetti({ ...defaults, particleCount: 20 }), 300);
}
