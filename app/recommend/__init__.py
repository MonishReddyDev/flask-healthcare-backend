from flask import Blueprint,jsonify,request
from app.models import Doctor
from flask_jwt_extended import jwt_required
from app.services.openai_service import get_doctor_recommendations
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import limiter



recommend_bp = Blueprint('recommend',__name__,url_prefix='/recommend')


@recommend_bp.route('/',methods=['POST'])
@jwt_required()
@limiter.limit("2 per minute") 
def recommend_doctor():
    data= request.get_json()
    problem= data.get('problem','').lower()
    
    if  not problem.strip():
        return jsonify({"error": "Problem description is required."}), 400
    
    try:
        #we will Call AI recommendation
        specializations = get_doctor_recommendations(problem)
        if not specializations:
             return jsonify({"message": "No specialization matched for the given problem."}), 200
         
        # doctors = Doctor.query.filter(Doctor.specialization.in_(specializations)).all() # type: ignore
        
        # if not doctors:
        #     return jsonify({"message": f"No doctors available for the recommended specializations: {', '.join(specializations)}."}), 200
        
        # recommended_doctors=[
        # {
        # "id": doctor.id,
        # "name": doctor.name,
        # "specialization": doctor.specialization,
        # "experience": doctor.experience,
        # "availability": doctor.availability,
        # "rating": doctor.rating
        # }
        # for doctor in doctors
        # ]
        # return jsonify({
        #         "problem": problem,
        #         "recommended_specializations": specializations,
        #         "recommended_doctors": recommended_doctors
        # }),200
        
        return jsonify({
            "problem": problem,
            "recommended_specializations": specializations
        }), 200
        
    except Exception as e:
        print(f"Error in recommend_doctor: {str(e)}")
        return jsonify({"error": "Something went wrong while processing your request."}), 500
        

        

        