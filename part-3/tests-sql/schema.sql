-- =========================================
-- Création des tables pour le projet HBnB
-- =========================================

-- 1. Table User
CREATE TABLE IF NOT EXISTS "User" (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 2. Table Place
CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    CONSTRAINT fk_place_owner FOREIGN KEY (owner_id) REFERENCES "User"(id)
);

-- 3. Table Review
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES "User"(id),
    CONSTRAINT fk_review_place FOREIGN KEY (place_id) REFERENCES Place(id),
    CONSTRAINT unique_user_place_review UNIQUE (user_id, place_id)
);

-- 4. Table Amenity
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- 5. Table d'association Place_Amenity (Many-to-Many)
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    CONSTRAINT fk_pa_place FOREIGN KEY (place_id) REFERENCES Place(id),
    CONSTRAINT fk_pa_amenity FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

-- =========================================
-- Insertion des données initiales
-- =========================================

-- Insertion de l'administrateur
INSERT INTO "User" (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$J9HulbKcV/IsEmzR6KqJkeVV4XqLQ4xLkJ/Ze9oCrF3d7vMW0IyiK', -- Mot de passe "admin1234" hashé avec bcrypt
    TRUE
);

-- Insertion des Amenities
INSERT INTO Amenity (id, name)
VALUES
    ('fbd74c6e-96c5-4c8b-9b88-cbba7279f8eb', 'WiFi'),
    ('3b5b6799-e3f1-47b7-bd8c-b7a0ed9f52b2', 'Swimming Pool'),
    ('fe80c9f3-b423-46ca-a60c-b2f5ca010d8e', 'Air Conditioning');

-- =========================================
-- Exemple de test CRUD (optionnel)
-- =========================================

-- Sélectionner tous les utilisateurs
SELECT * FROM "User";

-- Sélectionner toutes les places
SELECT * FROM Place;

-- Mise à jour d'un utilisateur (exemple)
UPDATE "User"
SET first_name = 'Super'
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Suppression d'une amenity (exemple)
DELETE FROM Amenity
WHERE name = 'Air Conditioning';
