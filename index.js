var map;
var cityName = document.getElementById("city-name");
var addressInput = document.getElementById("address-input");

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 43.732240, lng: -79.618660 },
    zoom: 10,
    mapTypeId: 'roadmap',
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false
  });
  var infoWindow = new google.maps.InfoWindow({
      content: ''
  });
  // Autocomplete
  autocomplete = new google.maps.places.Autocomplete(addressInput, {
    bounds: new google.maps.LatLngBounds(new google.maps.LatLng(40.913529, -96.952345), new google.maps.LatLng(55.850662, -73.661330)),
    strictBounds: true,
    types: ['address']
  });

  autocomplete.addListener('place_changed', () => {
    infoWindow.close();
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      // User entered name of place not suggested
      window.alert("No details available for: '" + place.name + "'" + ", please input a valid suggestion");
      return;
    }
    // Place was suggested
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(18);
    }
  });
  // Tilts 45 degrees once zoomed in
  map.setTilt(0);
  map.data.loadGeoJson('test.json')
  // Set style based on each feature (city)
  map.data.setStyle(feature => {
    var val = Math.random();
    // var color = val > 0.5 ? 'red': 'blue';
    // 1.98 - 5.96
    var mid = (1.98+5.96)/2;
    var baseBlue = 120;
    var minMax = 30;
    var newBlue = baseBlue;
    var newOffset = minMax;
    
    if (feature.getProperty("solar")) {
      // If has parent
      minMax = Math.pow((1/(feature.getProperty("solar")-mid)), 1) * minMax;
      console.log(minMax);
      if (feature.getProperty("parent")) {
        let parent = map.data.getFeatureById(feature.getProperty("parent")).getProperty("solar");
        let child = feature.getProperty("solar");
        console.log("Parent: " + parent + ", Child: " + child);
      }
    }
    var color = `rgb(0,0,${newBlue+newOffset},1)`;
    // console.log(feature.getProperty("name")); 
    
    return {
        fillColor: color,
        strokeWeight: 2,
        strokeOpacity: 0.9,
        strokeColor: "white",
        fillOpacity: 0.22
    }
  });
  // Show pop-up when clicked on a location
  map.data.addListener("click", e => {
      // Close info window before opening a new one
      infoWindow.close();

      let latLng = e.latLng;
      let houseImage = `https://maps.googleapis.com/maps/api/streetview?size=600x350&location=${latLng.lat()},${latLng.lng()}&fov=100&pitch=0&key=AIzaSyBhFGvR9_eW2muXvvJvUZ0wnCgT6kw6_1M`;
      console.log(latLng.lat() + ": " + latLng.lng());
      console.log(houseImage);

      infoWindow = new google.maps.InfoWindow({position: latLng});
      infoWindow.setContent(`
        <div id="info-window">
            <div id="info-header"> 
                <p id="info-header-text">Is this the building?</p>
                <button class="pure-material-button-contained info-header-button">Yes</button>
                <button class="pure-material-button-contained info-header-button">No</button>
            </div>
            <img src= "${houseImage}">
        </div>
      `);
      infoWindow.open(map);

  });
  // Changes text when mouse enters and leaves a city
  map.data.addListener('mouseover', e => {
    console.log("Entering: " + e.feature.getProperty("name"));
    cityName.innerHTML = e.feature.getProperty("name");
    cityName.style.opacity = 1;
  });

  map.data.addListener('mouseout', e => {
    console.log("Leaving: " + e.feature.getProperty("name"));
    cityName.style.opacity = 0;
  });

}
