var map;
var cityName = document.getElementById("city-name");
var addressInput = document.getElementById("address-input2");
var legendIndicator = document.getElementById("legend-indicator");

// 92 data polygons
// 2.84 - 3.5
var solarMin = 2.84,
  solarMax = 3.5;
var baseFillOpacity = 0.7;
var insideFillOpacity = 0.4;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 43.73224, lng: -79.61866 },
    zoom: 10,
    mapTypeId: "roadmap",
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false,
  });
  var infoWindow = new google.maps.InfoWindow({
    content: "",
  });

  // Autocomplete
  autocomplete = new google.maps.places.Autocomplete(addressInput, {
    bounds: new google.maps.LatLngBounds(
      new google.maps.LatLng(40.913529, -96.952345),
      new google.maps.LatLng(55.850662, -73.66133)
    ),
    strictBounds: true,
    types: ["address"],
  });

  autocomplete.addListener("place_changed", () => {
    infoWindow.close();
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      // User entered name of place not suggested
      window.alert(
        "No details available for: '" +
          place.name +
          "'" +
          ", please input a valid suggestion"
      );
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
  map.data.loadGeoJson("test.json");
  // Set style based on each feature (city)
  map.data.setStyle((feature) => {
	if (feature.getProperty("solar") > 3.3) {
		console.log(feature.getProperty("name") + "'s SV: " + feature.getProperty("solar"));
	}
    // 1.98 - 5.96
    // 54°, 40%, 100%-> 54°, 90%, 100%
    var low = [61, 73, 65]; // Smallest color
    var high = [0, 84, 61];
    let sv = feature.getProperty("solar");

    // delta represents where the value sits between min and max
    var delta = (sv - solarMin) / (solarMax - solarMin);

    var color = [];

    for (let i = 0; i < 3; i++) {
      // Calculate integer color based on the delta
      color[i] = (high[i] - low[i]) * delta + low[i];
    }


    return {
      fillColor: "hsl(" + color[0] + "," + color[1] + "%," + color[2] + "%)",
      strokeWeight: 2,
      strokeOpacity: 0.9,
      strokeColor: "white",
      fillOpacity: baseFillOpacity,
    };
  });

  // Zoom change
  google.maps.event.addDomListener(map, "zoom_changed", () => {
    let zoomLevel = map.getZoom();
    // Making area more visible
    if (zoomLevel >= 15 && zoomLevel < 17) {
      map.data.forEach((feature) => {
        map.data.overrideStyle(feature, { fillOpacity: insideFillOpacity });
      });
    } else {
      map.data.forEach((feature) => {
        map.data.overrideStyle(feature, { fillOpacity: baseFillOpacity });
      });
    }
    // Changing to satellite view
    if (zoomLevel >= 17) {
      map.setMapTypeId(google.maps.MapTypeId.HYBRID);
      map.data.forEach((feature) => {
        map.data.overrideStyle(feature, { fillOpacity: 0 });
      });
    } else {
	  map.setMapTypeId(google.maps.MapTypeId.ROADMAP);
    }
  });
  // Show pop-up when clicked on a location
  map.data.addListener("click", (e) => {
    // Close info window before opening a new one
    infoWindow.close();

    let latLng = e.latLng;
    let houseImage = `https://maps.googleapis.com/maps/api/streetview?size=600x350&location=${latLng.lat()},${latLng.lng()}&fov=100&pitch=0&key=AIzaSyBhFGvR9_eW2muXvvJvUZ0wnCgT6kw6_1M`;

    infoWindow = new google.maps.InfoWindow({ position: latLng });
    infoWindow.setContent(`
        <div id="info-window">
            <div id="info-header"> 
                <p id="info-header-text">Is this the building?</p>
                <button class="ui primary button">Yes</button>
                <button class="ui secondary button">No</button>
            </div>
            <img src= "${houseImage}">
        </div>
      `);
    infoWindow.open(map);
  });
  // Changes text when mouse enters and leaves a city
  map.data.addListener("mouseover", (e) => {
    cityName.innerHTML = e.feature.getProperty("name");
	cityName.style.opacity = 1;
	
	// Calculate legend indicator offset
	var percent = (e.feature.getProperty("solar") - solarMin) / (solarMax - solarMin) * 100;
	legendIndicator.style.paddingLeft = percent + "%";
  });

  map.data.addListener("mouseout", (e) => {
    cityName.innerHTML = "Pick your House";
    cityName.style.opacity = 1;
  });
}
