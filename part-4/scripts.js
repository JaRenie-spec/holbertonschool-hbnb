document.addEventListener('DOMContentLoaded', () => {

  // Dynamically populate places list
  const places = [
    { name: 'Place 1', price: 100, image: 'place1.jpg', detailsLink: 'place1.html' },
    { name: 'Place 2', price: 150, image: 'place2.jpg', detailsLink: 'place2.html' },
    { name: 'Place 3', price: 120, image: 'place3.jpg', detailsLink: 'place3.html' }
  ];

  // Sélectionner l'élément de la liste des lieux
  const placesList = document.getElementById('places-list');

  // Vérifier si placesList existe et qu'il n'y a pas déjà d'éléments dans la liste pour éviter les doublons
  if (placesList && placesList.children.length === 0) {
    places.forEach(place => {
      // Créer une carte de lieu pour chaque élément
      const placeCard = document.createElement('div');
      placeCard.classList.add('place-card');

      // Ajouter le contenu à la carte du lieu
      placeCard.innerHTML = `
        <img src="${place.image}" alt="${place.name}">
        <h3>${place.name}</h3>
        <p>Price per night: $${place.price}</p>
        <a href="${place.detailsLink}" class="details-button">View Details</a>
      `;

      // Ajouter la carte du lieu à la section places-list
      placesList.appendChild(placeCard);
    });
  }

  // Handling form submission for login and review
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', (event) => {
      event.preventDefault();
      // Handle review submission (e.g., send to server or local storage)
    });
  }
});
