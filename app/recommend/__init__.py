from flask import Blueprint,jsonify,request
from app.models import Doctor,Appointment
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.services.openai_service import get_doctor_recommendations
from flask_limiter import Limiter
from app import db
from flask_limiter.util import get_remote_address
from app import limiter

from datetime import datetime,timedelta



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
      
 
@recommend_bp.route('/ai/book', methods=['POST'])      
@jwt_required()
def ai_book_appointment():
    """
    will Book and appointment using natural language command using AI
    """
    data = request.get_json()
    command = data.get('command','').strip()
    
    if not command:
        return jsonify({"error": "Command is required."}), 400
    
    # Step 1: Send the command to OpenAI to extract specialization
    specializations = get_doctor_recommendations(command)

    
    if not specializations:
        return jsonify({"error": "Could not understand the specialization from your command."}), 400
    
    raw_specialization= specializations[0]
    
    if raw_specialization.startswith('['):
        import ast
        specialization_list = ast.literal_eval(raw_specialization)
        specialization = specialization_list[0] if specialization_list else None
    else:
        specialization = raw_specialization.strip()
    
    if not specialization:
        return jsonify({"error": "Specialization could not be extracted."}), 400

    
    doctor = Doctor.query.filter_by(specialization=specialization).first()

    
    if not doctor:
        return jsonify({"error": f"No doctor available for specialization '{specialization}'."}), 404
    
    # Step 3: Create a new appointment automatically
    current_user_id = get_jwt_identity()
    
    # Booking for Tomorrow 10AM (for now)
    start_time= datetime.now()+ timedelta(days=1)
    start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time= start_time+timedelta(minutes=30)
    
    # Check overlapping slots just in case (best practice)
    overlapping = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.start_time < end_time, # type: ignore
        Appointment.end_time > start_time, # type: ignore
        Appointment.status.in_(["Pending", "Confirmed"]) # type: ignore
    ).first()
    
    if overlapping:
        return jsonify({"error": "Doctor is not available at the suggested time. Please try again."}), 409

    new_appointment = Appointment(
        user_id=current_user_id,
        doctor_id=doctor.id,
        start_time=start_time,
        end_time=end_time,
        status="Pending"
    )

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({
        "message": "Appointment booked successfully!",
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization
        },
        "appointment": {
            "start_time": start_time.strftime('%Y-%m-%d %H:%M'),
            "end_time": end_time.strftime('%Y-%m-%d %H:%M')
        },
        "status": "Pending"
    }), 201

        