var map;
var cityName = document.getElementById("city-name");
var addressInput = document.getElementById("address-input2");
var legendIndicator = document.getElementById("legend-indicator");
var results = document.getElementById("results");
var boundingImage = document.getElementById("result-bounding-image");
var streetImage = document.getElementById("result-street-image");
var costYearlySavingsChart;

var costYearlySavings = document.getElementById('chart-cost-yearly-vs-savings-yearly').getContext('2d');

// Data for calculations
var solarPanelEffeciency = 0.25;
// Meteres squared
var eCArea = [55.74, 92.90, 139.35, 185.81, 232.26]; 
// kWh/m^2
var eC = [55.54, 54.57, 57.59, 49.62, 31.00];
var largestEC = 37.67;
// costs
var ontarioCostPerkWh = 0.125;
// Dimensions
var sPWidth = 1.651+0.2;
var sPHeight = 0.9906+0.2;
var sPArea = sPWidth * sPHeight;




// 92 data polygons
// 2.84 - 3.5
var solarMin = 2.84,
  solarMax = 3.5;
var baseFillOpacity = 0.7;
var insideFillOpacity = 0.4;
var buildingLatLng;
var infoWindow;
var currentSolar;
var houseImage;

function getAmountOfSolarPanels(area) {
  return Math.ceil(area / sPArea);
}

function getEnergyConsumptionPerMetersSquared(area) {
  for (let i = 0; i < eCArea.length; i++) {
    if (area <= eCArea[i]) {
      return eC[i];
    }
  }
  return largestEC;
}

function yesClick() {
  axios.get('https://damp-bayou-43879.herokuapp.com/process', {
    params: {
      lat: buildingLatLng.lat(),
      lon: buildingLatLng.lng(),
      solar: currentSolar
    }
  })
  .then(res => {
    data = res.data;
    // per month
    let kWhmSquared = getEnergyConsumptionPerMetersSquared(data.size);
    let kWh = kWhmSquared * data.size;
    let sPAmount = getAmountOfSolarPanels(data.size);
    let monthlyCosts = kWh * ontarioCostPerkWh/2.3;
    let yearlyCosts = monthlyCosts * 12;
    let monthlyEnergyProduced = data.adjusted * sPAmount * solarPanelEffeciency * 30;
    let yearlyEnergyProduced = monthlyEnergyProduced * 12;
    let monthlySavingsAfterSP = monthlyEnergyProduced * ontarioCostPerkWh;
    let yearlySavingsAfterSP = monthlySavingsAfterSP * 12;
    
    document.getElementById("energy-produced").innerHTML = `${Math.trunc(monthlyEnergyProduced)}`;
    document.getElementById("savings").innerHTML = `${Math.trunc(yearlySavingsAfterSP*25)}`;
    document.getElementById("consumption").innerHTML = `${Math.trunc(kWh)}`;
    document.getElementById("bounding-confidence").innerHTML = `${(data.score*100).toFixed(2)}%`;
    document.getElementById("bounding-type").innerHTML = `${data.name}`;
    if (costYearlySavingsChart == null) {
      costYearlySavingsChart = new Chart(costYearlySavings, {
        type: 'doughnut',
        data: {
          labels: ["Yearly Energy Cost (CAD)", "Yearly Energy Savings (CAD)"],
          datasets: [{
            label: "Yearly Energy Costs Vs Savings",
            data: [Math.trunc(yearlyCosts), Math.trunc(yearlySavingsAfterSP)],
            backgroundColor: [
              'rgba(39,117,242, 0.75)',
              'rgba(242,215,39, 0.75)'
            ],
            borderWidth: 1
          }]
        },
        options: {
  
        }
      });
    } else {
      costYearlySavingsChart.data.datasets.forEach((dataset, i) => {
        dataset.data = [Math.trunc(yearlyCosts), Math.trunc(yearlySavingsAfterSP)];
      });
      costYearlySavingsChart.update();
    }
    

    infoWindow.close();
    boundingImage.style.display = "inline";
    boundingImage.setAttribute(
      'src', `data:image/png;base64,${res.data.image}`
    );
    streetImage.style.display = "inline";
    streetImage.setAttribute(
      'src', `https://maps.googleapis.com/maps/api/streetview?size=600x450&location=${buildingLatLng.lat()},${buildingLatLng.lng()}&fov=100&pitch=0&key="YOUR_KEY"`
    )
    results.style.display = "flex";
    results.scrollIntoView({ behavior: "smooth" });
    
   

  })
  .catch(err => {
    console.error(err);
  });
}

function noClick() {
  infoWindow.close();
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 43.73224, lng: -79.61866 },
    zoom: 10,
    mapTypeId: "roadmap",
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false,
    rotateControl: false
  });
  map.setTilt(0);
  infoWindow = new google.maps.InfoWindow({
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
    buildingLatLng = latLng;
    currentSolar = e.feature.getProperty("solar");
    houseImage = `https://maps.googleapis.com/maps/api/streetview?size=600x350&location=${latLng.lat()},${latLng.lng()}&fov=100&pitch=0&key=AIzaSyBhFGvR9_eW2muXvvJvUZ0wnCgT6kw6_1M`;

    infoWindow = new google.maps.InfoWindow({ position: latLng });
    infoWindow.setContent(`
        <div id="info-window">
            <div id="info-header"> 
                <p id="info-header-text">Is this the building?</p>
                <button onclick="yesClick()" class="ui primary button">Yes</button>
                <button onclick="noClick()" class="ui secondary button">No</button>
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

