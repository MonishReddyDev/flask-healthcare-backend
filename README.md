# 🏥 Flask Healthcare Booking System (Backend Only)

This is a scalable, secure, and production-ready backend built with **Flask** for managing user authentication, doctor recommendations, and appointment bookings in a healthcare setting.

### ✅ Current Features Implemented

#### 🔐 Authentication System

- **User Registration** (`/auth/register`)
  - Accepts full name, email, password, and role (`patient`, `doctor`, `admin`)
  - Passwords are hashed using Werkzeug for security
  - Duplicate email check with proper error handling
- **User Login** (`/auth/login`)
  - Validates credentials
  - Returns a secure **JWT token** with user info
  - Token includes user ID as `sub` and custom claims (`email`, `role`)
- **Protected Route** (`/auth/me`)
  - Requires valid JWT token
  - Returns authenticated user's data (id, email, role)

#### 🔧 Core Technologies Used

- **Flask** – Lightweight web framework
- **Flask-JWT-Extended** – JWT authentication
- **Flask-SQLAlchemy** – ORM for SQLite
- **Flask-Migrate** – Database migrations
- **python-dotenv** – Environment variable management
- **Postman** – Used for manual API testing

---

### 📦 Project Structure

healthcare_app/ │ ├── app/ │ ├── init.py # App factory setup │ ├── config.py # Environment configs │ ├── models.py # SQLAlchemy models │ ├── auth/ # Auth Blueprint (register, login, me) │ │ └── init.py │ ├── routes/ # (Reserved for future Blueprints) │ ├── migrations/ # Auto-generated DB migrations ├── .env # Secret keys and config variables ├── .gitignore ├── run.py # App entry point ├── requirements.txt └── README.md

---

### ⚙️ Setup Instructions

1. Clone the repo:

   ```bash
   git clone https://github.com/MonishReddyDev/flask-healthcare-backend.git
   cd flask-healthcare-backend

   ```

2. Set up virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Create .env file:
   SECRET_KEY=your_flask_secret
   JWT_SECRET_KEY=your_jwt_secret
   DATABASE_URL=sqlite:///healthcare.db

4. Run migrations:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

5. Start the server:
   flask run

---

Let me know if you'd like a more casual version, or if you're ready to move forward with **Step 3: Doctor Listing** 🧑‍⚕️!
