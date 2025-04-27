# 🏥 Flask Healthcare Booking System (Backend)

This is a scalable, secure, and production-ready backend built with **Flask** for managing user authentication, AI-based doctor recommendations, and appointment bookings in a healthcare setting.

---

## ✅ Features Implemented

- **User Authentication** (JWT-based)
- **Doctor Listing** API
- **AI-Powered Doctor Recommendation**
  - Using OpenAI (gpt-3.5-turbo)
  - Based on user-described symptoms
  - Returns clean specialization list
- **Appointment Booking API** (basic setup)
- **Rate Limiting** to protect AI API calls
- **Swagger API Documentation** available at `/apidocs`
- **Error Handling** (JSON responses for rate limits, invalid requests)

---

## 📦 Technologies Used

- **Flask** — Web Framework
- **Flask-JWT-Extended** — Secure Authentication
- **Flask-SQLAlchemy** — ORM for SQLite
- **Flask-Migrate** — Database Migrations
- **Flasgger** — API Documentation (Swagger UI)
- **Flask-Limiter** — API Rate Limiting
- **OpenAI** — AI Recommendation (gpt-3.5-turbo)
- **SQLite** — Development Database
- **python-dotenv** — Environment Management

---

## 📋 Key API Endpoints

| Method | Endpoint           | Purpose                                   |
| ------ | ------------------ | ----------------------------------------- |
| POST   | `/auth/register`   | Register a new user                       |
| POST   | `/auth/login`      | Login and get JWT token                   |
| GET    | `/auth/me`         | Get current user info (protected)         |
| GET    | `/doctors/`        | List all doctors                          |
| POST   | `/recommend/`      | AI-based doctor specialization suggestion |
| POST   | `/appointments/`   | Book an appointment (basic)               |
| GET    | `/appointments/me` | View my booked appointments               |

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/MonishReddyDev/flask-healthcare-backend.git
cd flask-healthcare-backend


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

SECRET_KEY=your_flask_secret
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///healthcare.db
OPENAI_API_KEY=your_openai_api_key


flask db init   # Only if migrations folder not initialized
flask db migrate -m "Initial migration"
flask db upgrade

make dev
or
flask run --host=0.0.0.0 --port=5050

Access API Documentation
Visit: http://127.0.0.1:3000/apidocs
```
