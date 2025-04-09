document.addEventListener('DOMContentLoaded', () => {
    // Vérifier l'authentification
    checkAuthentication();

    // Sélectionner le formulaire de connexion
    const loginForm = document.getElementById('login-form');

    // Vérifier si le formulaire de connexion existe
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Empêcher le comportement par défaut du formulaire

            // Récupérer les valeurs des champs email et mot de passe
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Appeler la fonction pour envoyer la requête de connexion
            await loginUser(email, password);
        });
    }

    // Ajouter les options de filtre de prix
    const priceFilter = document.getElementById('price-filter');
    const priceOptions = [10, 50, 100, 200, 'all'];
    priceOptions.forEach((price) => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = price === 'all' ? 'All' : `$${price}`;
        priceFilter.appendChild(option);
    });

    // Ajouter l'événement de filtre de prix
    priceFilter.addEventListener('change', () => {
        filterPlacesByPrice(); // Appliquer le filtre
    });
});

// Fonction pour envoyer la requête de connexion
async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            const token = data.access_token;

            document.cookie = `token=${token}; path=/`;
            window.location.href = 'index.html'; // Rediriger vers la page index après la connexion
        } else {
            const errorData = await response.json();
            alert('Login failed: ' + errorData.message);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed: ' + error.message);
    }
}

// Fonction pour obtenir un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fonction pour vérifier le statut de l'authentification de l'utilisateur
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.querySelector('.login-button'); // Récupérer le bouton de connexion par la classe

    if (loginLink) {  // Ajout d'une vérification pour s'assurer que l'élément existe
        if (!token) {
            loginLink.style.display = 'block'; // Afficher le lien de connexion si aucun token n'est trouvé
        } else {
            loginLink.style.display = 'none'; // Cacher le lien de connexion si l'utilisateur est authentifié
        }
    }
}


// Fonction pour récupérer les lieux depuis l'API
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();
        // Si la réponse est vide ou invalide, utiliser les données de test
        if (!places || places.length === 0) {
            displayPlaces(getTestPlaces()); // Utiliser les données de test si aucun lieu n'est récupéré
        } else {
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        // Utiliser les données de test en cas d'erreur lors de la récupération des lieux
        displayPlaces(getTestPlaces());
    }
}

// Fonction pour retourner des données de test sur les lieux
function getTestPlaces() {
    return [
        {
            id: 1,
            name: "Test Place 1",
            description: "A beautiful test place near the sea.",
            imageUrl: "https://via.placeholder.com/150",
            price: 50,
        },
        {
            id: 2,
            name: "Test Place 2",
            description: "A luxurious test place in the mountains.",
            imageUrl: "https://via.placeholder.com/150",
            price: 100,
        },
        {
            id: 3,
            name: "Test Place 3",
            description: "An affordable test place in the city center.",
            imageUrl: "https://via.placeholder.com/150",
            price: 25,
        },
    ];
}

// Fonction pour afficher les lieux sur la page
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach((place) => {
        const placeDiv = document.createElement('div');
        placeDiv.classList.add('place-item');
        placeDiv.innerHTML = `
            <img src="${place.imageUrl}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p>$${place.price} per night</p>
            <a href="place.html?place=${place.id}" class="view-details">View Details</a>
        `;
        placesList.appendChild(placeDiv);
    });
}

// Fonction pour filtrer les lieux en fonction du prix
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    const selectedPrice = priceFilter.value;
    const placesList = document.getElementById('places-list');
    const placeItems = placesList.getElementsByClassName('place-item');

    // Parcourir chaque élément de lieu et afficher/masquer en fonction du prix sélectionné
    Array.from(placeItems).forEach((place) => {
        const priceText = place.querySelector('p').textContent; // Récupérer le texte du prix de chaque élément
        const price = parseInt(priceText.replace('$', '').replace(' per night', '')); // Extraire le prix

        if (selectedPrice === 'all' || price <= selectedPrice) {
            place.style.display = 'block'; // Afficher le lieu
        } else {
            place.style.display = 'none'; // Masquer le lieu
        }
    });
}
