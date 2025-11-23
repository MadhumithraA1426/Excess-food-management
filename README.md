
# Excess Food Management System

A simple web application to manage and share excess food donations using Flask for backend, PostgreSQL for database, and HTML/CSS for frontend.

---

## Features

- Donor registration and login.
- Donors can upload excess food details with expiry date.
- Donors can view and delete their uploaded foods.
- Users can search for available foods by location.
- Automatic deletion of expired food entries.
- Clean and responsive HTML/CSS frontend.

---

## Prerequisites

- Python 3.8 or higher
- PostgreSQL server installed and running
- Basic knowledge of terminal/command prompt

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/MadhumithraA1426/Excess-food-management.git
cd Excess-food-management
```

### 2. Create and activate Python virtual environment

```
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure database connection

- Create a `.env` file in the project root with contents:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=excess_food_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

- Replace `your_postgres_password` with your actual password.

### 5. Create PostgreSQL database and tables

- Using pgAdmin or psql, create the database `excess_food_db`.

- Create tables with this SQL:

```
CREATE TABLE donors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE foods (
    id SERIAL PRIMARY KEY,
    donor_id INT REFERENCES donors(id) ON DELETE CASCADE,
    food_name VARCHAR(200) NOT NULL,
    quantity VARCHAR(100),
    location VARCHAR(200),
    contact_phone VARCHAR(50),
    expiry_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 6. Run the application

```
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Usage

- Donors can sign up and log in.
- Donors can upload food items with expiry date.
- Donors can view and delete their active food items.
- Users can search available food items by location on the user page.
- Food expired items are automatically cleaned on each app request.

---

## Project Structure

```
excess_food_app/
│
├─ app.py             # Flask app and routes
├─ db.py              # Database connection and queries
├─ config.py          # DB config using environment variables
├─ requirements.txt   # Python dependencies list
├─ templates/
│   ├─ base.html
│   ├─ login.html
│   ├─ donor.html
│   └─ user.html
└─ static/
    └─ styles.css     # CSS for styling
```

---

## Notes

- Passwords are stored as plain text in this demo (not recommended for production). Use hash functions like bcrypt in production.
- Update `secret_key` in `app.py` with a secure key for production.
- Customize styling and frontend UI as needed.

---

