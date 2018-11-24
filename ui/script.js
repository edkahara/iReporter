function getLocationConstant() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(onGeoSuccess, onGeoError);
  } else {
    alert("Your browser or device doesn't support Geolocation");
  }
}

function onGeoSuccess(event) {
  document.getElementById("latitude").value = event.coords.latitude;
  document.getElementById('longitude').value = event.coords.longitude;
}

function onGeoError(event) {
  alert("Error code " + event.code + ". " + event.message);
}
