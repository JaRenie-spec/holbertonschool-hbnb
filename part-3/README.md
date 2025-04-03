# HBnB Project: Part 3 - Persistence Layer and Authentication
---

## 📌 Overview
---

In Part 3 of the **HBnB Project**, we enhance the application by introducing a **database-backed Persistence Layer** and implementing **Authentication & Authorization** mechanisms.

- ✅ Reliable data storage with **SQLAlchemy**
- ✅ Secure access with **JWT authentication**
- ✅ Role-based access control for sensitive actions

This makes the application more robust, secure, and production-ready.

---

## 🏗️ Project Structure
---

The application now consists of the following layers:

- **Presentation Layer** → Flask + flask-restx API endpoints
- **Business Logic Layer** → Validation, relationships, access control
- **Persistence Layer** → SQLAlchemy ORM for database interactions
- **Authentication Layer** → JWT-based login and access restrictions

---

## 🎯 Objectives
---

### 1️⃣ Database Integration
- Migrate from in-memory repository to **SQLAlchemy ORM**
- Define entities: `User`, `Place`, `Review`, `Amenity`
- Create database schema and ensure **referential integrity**

### 2️⃣ Authentication & Authorization
- Implement **JWT login & token generation**
- Add **role-based access control** (admin / user)
- Secure routes using custom decorators

### 3️⃣ Enhanced API Functionality
- Add login/registration endpoints
- Protect all API routes with authentication
- Extend admin capabilities (user management)

### 4️⃣ Error Handling & Validation
- Handle unauthorized/forbidden access gracefully
- Validate inputs on both API and business levels
- Return clear, user-friendly error messages

---

## 📡 API Endpoints
---

### 🔐 Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Authenticate and get JWT token |

### 🔒 Protected Routes (JWT Required)
> All previous CRUD endpoints (Users, Places, Reviews, Amenities) are now protected.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/` | Retrieve all users (authenticated) |
| POST | `/api/v1/places/` | Create a new place (authenticated) |
| PUT | `/api/v1/reviews/<review_id>` | Update a review (authenticated) |

---

## 💡 Example Usage
---

### ✅ User Login
```
POST /api/v1/auth/login
{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

**Response:**
```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

### 🔐 Accessing a Protected Route
```
GET /api/v1/places/
Authorization: Bearer <access_token>
```

---

## 🧪 Testing
---

- 🔍 Unit tests with **pytest** (models, logic, API routes)
- 🧪 API testing with **Postman/cURL**
- 🔐 JWT token validation & role-based tests

---

## ⚙️ Technologies Used
---

- **Python** - Flask, flask-restx
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - Authentication
- **SQLite/PostgreSQL** - Database
- **pytest** - Unit testing

---

## 🚀 Future Enhancements
---

- Refresh tokens
- Password reset functionality
- dynamic database update
- enhance security

---

## 📚 Resources
---

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/en/latest/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [RESTful API Best Practices](https://restfulapi.net/)

---

## 👨‍💻 Contributors
---

- **Jean-Alain Renié** → https://github.com/JaRenie-spec
- **Killian Ripoche** → https://github.com/KillianRipoche
- **Alexis Battistoni** → https://github.com/Albat93
