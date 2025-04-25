#Where we’ll define DB schemas

from . import db
from werkzeug.security import generate_password_hash,check_password_hash



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
        
    