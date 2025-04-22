# 🌍 Venue Booking Platform

A simple web app that allows users to browse and filter venues, view details, and post reviews. Includes login/logout functionality and protected review submission.

## 📁 Project Structure


## 🚀 Features

- **User login/logout** with JWT stored in cookies
- **Dynamic venue display** from a REST API
- **Price filtering** via front-end
- **Venue details page** with host, price, description, and amenities
- **Review system**: display and post reviews (authenticated)
- **Dynamic auth buttons** based on session state

## 🧠 Tech Stack

- HTML, CSS, JavaScript (ES6+)
- REST API backend (e.g., Flask)
- Token-based authentication

## 🔐 Authentication

- JWT is saved in a cookie after login
- Token is included in `Authorization` header for protected requests
- Used to control UI visibility and access to review submission

## 📜 JavaScript Highlights (`scripts.js`)

- Cookie management
- Auth button toggling
- API fetching (places, details, reviews)
- Review submission
- Login/logout handling

## 🎨 Design

- Responsive layout
- Clean and minimal UI
- Custom icons for amenities
- Cards for places and reviews

