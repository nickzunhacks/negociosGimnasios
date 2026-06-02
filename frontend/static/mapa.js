const map = L.map('map').setView([4.65, -74.09], 12); // empieza en Bogota centro con un zoom en el que se puede ver barrios

console.log("Gyms desde javaScript: ",GYMS)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
    }).addTo(map); //dibuja las calles y todo los detalles del mapa

GYMS.forEach(gym => {
    const marker = L.marker([gym.latitude, gym.longitude]).addTo(map); // Se agrega ubicacion de gimnasio por medio de un market

    marker.on("click", () => {
        document.getElementById('nombre').textContent = gym.name
        document.getElementById('descripcion').textContent = gym.description
    }) // card al hacer click en el market, se ve un overview del gimnasio
})

