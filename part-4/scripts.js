/**
 * Récupère la valeur d'un cookie
 */
function getCookie(name) {
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split("=");
    if (key === name) return value;
  }
  return null;
}

/**
 * Affichage des boutons Login et Logout
 */
function updateAuthButtons() {
  const token = getCookie("token");
  const loginLink = document.getElementById("login-link");
  const logoutBtn = document.getElementById("logout-button");

  if (token) {
    if (loginLink) loginLink.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "inline-block";
  } else {
    if (loginLink) loginLink.style.display = "block";
    if (logoutBtn) logoutBtn.style.display = "none";
  }
}

/**
 * Logout : supprime le cookie et redirige vers login
 */
function initLogout() {
  const logoutBtn = document.getElementById("logout-button");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      window.location.href = "login.html";
    });
  }
}

/**
 * Affiche la liste des lieux et configure le filtre
 */
async function fetchPlaces() {
  try {
    const token = getCookie("token");
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = "Bearer " + token;

    const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
      method: "GET",
      headers,
      credentials: "include",
    });
    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      console.error("Erreur fetchPlaces:", response.statusText);
    }
  } catch (err) {
    console.error("Erreur fetchPlaces:", err);
  }
}

function displayPlaces(places) {
  const list = document.getElementById("places-list");
  if (!list) return;
  list.innerHTML = "";

  places.forEach((place) => {
    const card = document.createElement("div");
    card.className = "place-card";
    card.setAttribute("data-price", place.price);

    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price} per night</p>
      <p>${place.description}</p>
      <button class="btn" onclick="viewDetails('${place.id}')">View Details</button>
    `;
    list.appendChild(card);
  });
}

function viewDetails(placeId) {
  window.location.href = `place.html?id=${placeId}`;
}

function initPriceFilter() {
  const filter = document.getElementById("price-filter");
  if (filter) {
    filter.addEventListener("change", (event) => {
      const max = event.target.value;
      document.querySelectorAll(".place-card").forEach((card) => {
        const price = parseFloat(card.getAttribute("data-price"));
        card.style.display =
          max === "All" || price <= parseFloat(max) ? "block" : "none";
      });
    });
  }
}

function getPlaceIdFromURL() {
  return new URLSearchParams(window.location.search).get("id");
}

async function fetchPlaceDetails() {
  const token = getCookie("token");
  const placeId = getPlaceIdFromURL();
  try {
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = "Bearer " + token;

    const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: "GET",
      headers,
    });
    if (!res.ok) throw new Error(res.statusText);
    const place = await res.json();
    displayPlaceDetails(place);
    loadReviews(placeId);
  } catch (err) {
    console.error("Erreur fetchPlaceDetails:", err);
  }
}

function displayPlaceDetails(place) {
  document.getElementById("place-name").textContent = place.title;
  document.getElementById(
    "place-host"
  ).textContent = `Host: ${place.owner.first_name} ${place.owner.last_name}`;
  document.getElementById("place-price").textContent = `Price: $${place.price}`;
  document.getElementById(
    "place-description"
  ).textContent = `Description: ${place.description}`;

  const icons = {
    wifi: "<img src='./images/icon_wifi.png' alt='Wifi' style='height:20px;'>",
    bathroom:
      "<img src='./images/icon_bath.png' alt='Bathroom' style='height:20px;'>",
    bed: "<img src='./images/icon_bed.png' alt='Bed' style='height:20px;'>",
  };
  const amenEl = document.getElementById("place-amenities");
  if (place.amenities.length === 0) {
    amenEl.textContent = "Amenities: None";
  } else {
    const html = place.amenities
      .map((a) => {
        const key = a.name.toLowerCase().trim();
        const img = icons[key] || "";
        return `${img} ${a.name}`;
      })
      .join(" | ");

    amenEl.innerHTML = "Amenities: " + html;
  }

  document.getElementById("place-image").src =
    place.image || "https://www.costas-casas.fr/db/huizen/1357/123765-2_57.jpg";
}

async function loadReviews(placeId) {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/v1/reviews/");
    if (!res.ok) throw new Error(res.statusText);
    const all = await res.json();
    const reviews = all.filter((r) => r.place_id === placeId);

    const container = document.getElementById("reviews");
    container.innerHTML = "<h3>Reviews</h3>";
    if (reviews.length === 0) {
      container.innerHTML += "<p>No reviews yet.</p>";
    } else {
      reviews.forEach((r) => {
        const el = document.createElement("article");
        el.className = "review-card";
        el.innerHTML = `<p>"${r.text}"</p><p>Rating: ${r.rating}/5</p>`;
        container.appendChild(el);
      });
    }
  } catch (err) {
    console.error("Erreur loadReviews:", err);
  }
}

function initAddReviewButton() {
  const btn = document.getElementById("add-review-button");
  if (!btn) return;
  const token = getCookie("token");
  const placeId = getPlaceIdFromURL();
  btn.addEventListener("click", () => {
    if (token) {
      window.location.href = `add_review.html?id=${placeId}`;
    } else {
      window.location.href = "login.html";
    }
  });
}

/**
 * Stocke le token et redirige.
 */
async function loginUser(email, password) {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });
    if (response.ok) {
      const data = await response.json();
      const token = data.access_token || data.token;
      document.cookie = `token=${token}; path=/;`;
      document.getElementById("login-message").textContent =
        "Connexion réussie ! Redirection…";
      setTimeout(() => (window.location.href = "index.html"), 1000);
    } else {
      document.getElementById("error-message").textContent =
        "Login failed: " + response.statusText;
      document.getElementById("error-message").style.display = "block";
    }
  } catch (err) {
    console.error("Erreur loginUser:", err);
    document.getElementById("error-message").textContent =
      "Une erreur est survenue lors du login.";
    document.getElementById("error-message").style.display = "block";
  }
}

/**
 * ADD REVIEW PAGE Accessible uniquement si login
 */
async function submitReview() {
  const token = getCookie("token");
  const placeId = getPlaceIdFromURL();
  const text = document.getElementById("review").value;
  const rating = parseInt(document.getElementById("rating").value, 10);

  try {
    const res = await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({ text, rating, place_id: placeId }),
    });
    if (res.ok) {
      alert("Review submitted successfully!");
      document.getElementById("review-form").reset();
    } else {
      alert("Failed to submit review.");
    }
  } catch (err) {
    console.error("Erreur submitReview:", err);
    alert("Erreur lors de l'envoi de l'avis.");
  }
}

/**
 * Initialisation
 */
document.addEventListener("DOMContentLoaded", () => {
  updateAuthButtons();
  initLogout();

  if (document.body.id === "index-page") {
    fetchPlaces();
    initPriceFilter();
  }

  if (document.body.id === "place-page") {
    fetchPlaceDetails();
    initAddReviewButton();
  }

  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      loginUser(
        document.getElementById("email").value,
        document.getElementById("password").value
      );
    });
  }

  if (document.body.id === "add-review-page") {
    const token = getCookie("token");
    if (!token) {
      window.location.href = "login.html";
      return;
    }
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
      reviewForm.addEventListener("submit", (e) => {
        e.preventDefault();
        submitReview();
      });
    }
  }
});
