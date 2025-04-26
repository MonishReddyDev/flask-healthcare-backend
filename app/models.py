#Where we’ll define DB schemas

from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship



class User(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="patient")
    
    
    def __init__(self, full_name: str, email: str, role: str = "patient") -> None:
        self.full_name = full_name
        self.email = email
        self.role = role
    
    #encrypts password before saving
    def set_password(self,password):
        self.password_hash= generate_password_hash(password)
        
    #compares raw input with hashed one
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        

class Doctor(db.Model):
    
    id:str
    name:str
    specialization:str
    experience:int 
    availability:str
    rating:float
    
        
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Text, nullable=False)  # storing JSON as text
    rating = db.Column(db.Float, default=0.0)
    
    
    def __init__(self, name: str, specialization: str, experience: int, availability: str, rating: float = 0.0):
        self.name = name
        self.specialization = specialization
        self.experience = experience
        self.availability = availability
        self.rating = rating



class Appointment(db.Model):
    id: int
    user_id: int
    doctor_id: int
    start_time:datetime
    end_time:datetime
    status: str
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(
    db.Integer,
    db.ForeignKey('doctor.id', name='fk_appointment_doctor_id'),
    nullable=False)# ✅ Fixed Foreign Key
    start_time = db.Column(db.DateTime,nullable=False)
    end_time= db.Column(db.DateTime,nullable=False) 
    status = db.Column(db.String(50), default="Booked")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = relationship("Doctor", backref="appointments", lazy=True)  # ✅ Now relationship works

    def __init__(self, user_id: int, doctor_id: int,start_time:datetime,end_time:datetime, status: str = "Booked"):
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.start_time = start_time
        self.end_time =end_time
        self.status = status
