from flask import Blueprint,jsonify,request
from app.models import Doctor
from flask_jwt_extended import jwt_required


recommend_bp = Blueprint('recommend',__name__,url_prefix='/recommend')

# Simple keyword to specialization mapping
problem_mapping = {
    "skin": "Dermatologist",
    "rash": "Dermatologist",
    "heart": "Cardiologist",
    "chest pain": "Cardiologist",
    "brain": "Neurologist",
    "headache": "Neurologist",
    "diabetes": "Endocrinologist",
    "allergy": "Allergist"
}

@recommend_bp.route('/',methods=['POST'])
@jwt_required()
def recommend_doctor():
    data= request.get_json()
    problem = data.get('problem','').lower()
    
    if not problem.strip():
        return  jsonify({"error": "Problem description is required."}), 400
    
    matched_specialization= None
    for keyword, specialization in problem_mapping.items():
        if keyword in problem:
            matched_specialization=specialization
            break
    
    if not matched_specialization:
        return jsonify({"message": "No specialization matched for the given problem."}), 200
    
    
    doctors = Doctor.query.filter_by(specialization=matched_specialization).all()
    
    if not doctors:
        return jsonify({"message":f"No doctors available for specialization {matched_specialization}."}),200
    
    recommended_doctors = []
    for doctor in doctors:
        recommended_doctors.append({
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "experience": doctor.experience,
            "availability": doctor.availability,
            "rating": doctor.rating
        })
    
    
    return jsonify({
        "problem": problem,
        "matched_specialization": matched_specialization,
        "recommended_doctors": recommended_doctors
    }), 200