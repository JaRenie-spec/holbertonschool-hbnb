document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        const priceOptions = [10, 50, 100, 200, 'all'];
        priceOptions.forEach((price) => {
            const option = document.createElement('option');
            option.value = price;
            option.textContent = price === 'all' ? 'All' : `$${price}`;
            priceFilter.appendChild(option);
        });

        priceFilter.addEventListener('change', () => {
            filterPlacesByPrice();
        });
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    if (placeId) {
        fetchPlaceDetails(token);
    } else {
        if (document.getElementById('places-list')) {
            fetchPlaces(token);
        }
    }
});

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('place');
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.querySelector('.login-button');
    const addReviewSection = document.getElementById('add-review');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
            if (addReviewSection) addReviewSection.style.display = 'none';
        } else {
            loginLink.style.display = 'none';
            if (addReviewSection) addReviewSection.style.display = 'block';
        }
    }
}

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
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            alert('Login failed: ' + errorData.message);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed: ' + error.message);
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) throw new Error('Failed to fetch places');
        const places = await response.json();
        if (!places || places.length === 0) {
            displayPlaces(getTestPlaces());
        } else {
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        displayPlaces(getTestPlaces());
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
    const token = getCookie('token');

    places.forEach((place) => {
        const placeDiv = document.createElement('div');
        placeDiv.classList.add('place-item');

        const buttonHTML = `<button class="view-details" onclick="viewDetails('${place.id}')">View Details</button>`;

        placeDiv.innerHTML = `
            <img src="${place.imageUrl}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p class="price">$${place.price} per night</p>
            ${buttonHTML}
        `;
        placesList.appendChild(placeDiv);
    });
}

function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    const selectedPrice = priceFilter.value;
    const placesList = document.getElementById('places-list');
    const placeItems = placesList.getElementsByClassName('place-item');

    Array.from(placeItems).forEach((place) => {
        const priceText = place.querySelector('.price').textContent;
        const price = parseInt(priceText.replace('$', '').replace(' per night', ''));
        if (selectedPrice === 'all' || price <= parseInt(selectedPrice)) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}

async function fetchPlaceDetails(token) {
    const placeId = getPlaceIdFromURL();
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function getTestPlaces() {
    return [
        {
            id: 'place1',
            name: 'Cozy Cottage',
            description: 'A beautiful cozy cottage perfect for a peaceful retreat.',
            price: 120,
            imageUrl: 'place1.jpg'
        },
        {
            id: 'place2',
            name: 'Urban Loft',
            description: 'Modern loft in the heart of the city.',
            price: 200,
            imageUrl: 'place2.jpg'
        },
        {
            id: 'place3',
            name: 'Mountain Cabin',
            description: 'Secluded cabin in the mountains for a nature getaway.',
            price: 95,
            imageUrl: 'place3.jpg'
        },
        {
            id: 'place4',
            name: 'Cheap Tent',
            description: 'Budget-friendly tent for a camping experience.',
            price: 45,
            imageUrl: 'place4.jpg'
        },
        {
            id: 'place5',
            name: 'Luxury Villa',
            description: 'Spacious villa with a private pool and luxury amenities.',
            price: 280,
            imageUrl: 'place5.jpg'
        }
    ];
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    placeDetailsSection.innerHTML = '';

    const placeDiv = document.createElement('div');
    placeDiv.classList.add('place-item');

    const amenities = Array.isArray(place.amenities) ? place.amenities.join(', ') : 'N/A';
    const reviewsHTML = Array.isArray(place.reviews) && place.reviews.length > 0 ?
        place.reviews.map(review => `
            <div class="review">
                <p>"${review.text}" - <strong>${review.user}</strong></p>
                <span class="rating">${'★'.repeat(review.rating)}</span>
            </div>
        `).join('') : '<p>No reviews available</p>';

    placeDiv.innerHTML = `
        <img src="${place.imageUrl}" alt="${place.name}">
        <h2>${place.name}</h2>
        <p>${place.description}</p>
        <p>Price: $${place.price}</p>
        <p>Amenities: ${amenities}</p>
        <div id="reviews">
            <h3>Reviews</h3>
            ${reviewsHTML}
        </div>
    `;

    placeDetailsSection.appendChild(placeDiv);
}

function viewDetails(placeId) {
    window.location.href = `place.html?place=${placeId}`;
}

