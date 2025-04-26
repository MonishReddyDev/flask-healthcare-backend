# 🏥 Flask Healthcare Booking System (Backend)

This is a scalable, secure, and production-ready backend built with **Flask** for managing user authentication, doctor recommendations, and appointment bookings in a healthcare setting.

---

## ✅ Current Features

- User Registration & Login (JWT-based)
- Role-Based Access Control (Patient / Doctor / Admin)
- Doctor Listing
- Simple Doctor Recommendation (Keyword-based)
- Appointment Booking (with real Start Time and End Time)
- Appointment Overlapping Slot Validation
- View My Appointments
- Cancel Appointment (Soft Cancel - Status Update)
- Admin: Create, Update, Delete Doctors
- Admin: View All Appointments
- Admin: Delete Specific or All Appointments
- Swagger API Documentation (`/apidocs`)
- Edge Case Handling (Double Booking, Unauthorized Access, Time Validations)

---

## 🔧 Technologies Used

- **Flask** — Web Framework
- **Flask-SQLAlchemy** — ORM for Database
- **Flask-JWT-Extended** — Secure Authentication
- **Flask-Migrate** — Database Versioning (Alembic)
- **Flasgger** — API Documentation (Swagger UI)
- **SQLite** — Lightweight Development Database
- **python-dotenv** — Environment Variable Management
- **Postman** — API Testing

---

## 📦 Project Structure

---

---

## 📋 API Endpoints

| Method | Endpoint                                  | Purpose                                     |
| ------ | ----------------------------------------- | ------------------------------------------- |
| POST   | `/auth/register`                          | Register a new user                         |
| POST   | `/auth/login`                             | Login and get JWT token                     |
| GET    | `/auth/me`                                | Get authenticated user info                 |
| GET    | `/doctors/`                               | List all available doctors                  |
| POST   | `/recommend/`                             | Recommend doctors based on user problem     |
| POST   | `/appointments/`                          | Book an appointment (with slot validation)  |
| GET    | `/appointments/me`                        | View your appointments                      |
| PUT    | `/appointments/<appointment_id>/cancel`   | Cancel an appointment                       |
| PUT    | `/appointments/<appointment_id>/complete` | (Coming soon) Mark appointment as complete  |
| POST   | `/admin/doctor`                           | Admin: Create a new doctor                  |
| PUT    | `/admin/doctor/<doctor_id>`               | Admin: Update doctor info                   |
| DELETE | `/admin/doctor/<doctor_id>`               | Admin: Delete a doctor (if no appointments) |
| GET    | `/admin/appointments`                     | Admin: View all appointments                |
| DELETE | `/admin/appointments/<appointment_id>`    | Admin: Delete an appointment or all         |

✅ All APIs protected where necessary using JWT and role-based checks.

✅ Full API Documentation available at [http://127.0.0.1:5050/apidocs](http://127.0.0.1:5050/apidocs)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/MonishReddyDev/flask-healthcare-backend.git
cd flask-healthcare-backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

SECRET_KEY=your_flask_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
DATABASE_URL=sqlite:///healthcare.db

flask db init   # Only if migrations folder not initialized
flask db migrate -m "Initial migration"
flask db upgrade

make dev
or
flask run --host=0.0.0.0 --port=5050

Access API Documentation
Visit: http://127.0.0.1:5050/apidocs
```
