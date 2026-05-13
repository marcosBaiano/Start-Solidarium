<!DOCTYPE html>
<html>
<head>
  <title>Mapa com OSM</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
</head>
<body>

<div id="map" style="height: 400px;"></div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
  var map = L.map('map').setView([-3.7319, -38.5267], 13); // Fortaleza

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  L.marker([-3.7319, -38.5267]).addTo(map)
    .bindPopup('Você está aqui!')
    .openPopup();
</script>

</body>
</html>