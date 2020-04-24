var map;
var cityName = document.getElementById("city-name");

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 43.732240, lng: -79.618660 },
    zoom: 10,
    mapTypeId: 'hybrid',
    mapTypeControl: false,
    streetViewControl: false
  });
  var infoWindow = new google.maps.InfoWindow({
      content: ''
  });
  // Tilts 45 degrees once zoomed in
  map.setTilt(0);
  map.data.loadGeoJson('test.json')
  // Set style based on each feature (city)
  map.data.setStyle(feature => {
    var val = Math.random();
    var color = val > 0.5 ? 'red': 'blue';
    console.log(feature.getProperty("name"));
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
      let houseImage = `https://maps.googleapis.com/maps/api/streetview?size=600x350&location=${latLng.lat()},${latLng.lng()}&fov=100&pitch=0&key=AIzaSyCwWIWTgA5sHugpBZnjjRG6HcU0a6NAhlc`;
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
