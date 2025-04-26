from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Appointment,Doctor,db
from datetime import datetime
from sqlalchemy import and_

appointments_bp = Blueprint('appointments', __name__, url_prefix='/appointments')


@appointments_bp.route('/',methods=['POST'])
@jwt_required()
def book_appointment():
    data = request.get_json()
    doctor_id= data.get('doctor_id')
    start_time_str=data.get('start_time')
    end_time_str = data.get('end_time')
    
    if not doctor_id or not start_time_str or not end_time_str:
        return jsonify({"error": "Doctor ID, start time, and end time are required."}), 400
    
    try:
        start_time = datetime.strptime(start_time_str,'%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM"}), 400
    
    if start_time>=end_time:
        return jsonify({"error": "Start time must be before end time."}), 400
    
    # Check if doctor exists
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return jsonify({"error": "Doctor not found."}), 404
    
    # Check for overlapping appointments
    # Overlapping check
    overlapping = Appointment.query.filter(
    and_(
        Appointment.doctor_id == doctor_id,
        Appointment.start_time < end_time, # type: ignore
        Appointment.end_time > start_time # type: ignore
    )
    ).first()
    
    if overlapping:
        return jsonify({"error": "This time slot is already booked."}), 409

    current_user_id = get_jwt_identity()
    new_appointment = Appointment(
        user_id=current_user_id,
        doctor_id=doctor_id,
        start_time=start_time,
        end_time=end_time,
        status="Booked"
    )
    
    db.session.add(new_appointment)
    db.session.commit()
    
    return jsonify({"message":'Appointment booked successfully!'}),200


@appointments_bp.route('/me',methods=['GET'])
@jwt_required()
def get_my_appointments():
    current_user_id= get_jwt_identity()

    
    my_appointments =  Appointment.query.filter_by(user_id=current_user_id).all()
    
    appointments_list = []
    for appointment in my_appointments:
        doctor = appointment.doctor  # Access doctor directly via relationship
        
        appointments_list.append({
            "appointment_id": appointment.id,
            "doctor_name": doctor.name if doctor else "Unknown Doctor",
            "specialization": doctor.specialization if doctor else "Unknown",
            "appointment_time": appointment.appointment_time,
            "status": appointment.status,
            "created_at": appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    
    return jsonify(appointments_list), 200
        
        
@appointments_bp.route('<int:appointment_id>/cancel',methods=['PUT'])        
@jwt_required()
def cancel_appointment(appointment_id):
    current_user_id= get_jwt_identity()

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found."}), 404
    
    if appointment.user_id != int(current_user_id):
        return jsonify({"error": "You are not authorized to cancel this appointment."}), 403
    
    if appointment.status == "Cancelled":
        return jsonify({"message": "Appointment is already cancelled."}), 200
    
    if appointment.status == "Completed":
        return jsonify({"error": "Completed appointments cannot be cancelled."}), 400
    
    appointment.status = 'Cancelled'
    db.session.commit()
    
    
    return jsonify({"message": "Appointment cancelled successfully."}), 200



@appointments_bp.route('/<int:appointment_id>/complete', methods=['PUT'])
@jwt_required()
def complete_appointment(appointment_id):
    current_user_id = get_jwt_identity()
    
    appointment = Appointment.query.get(appointment_id)
    
    if not appointment:
        return jsonify({"error": "Appointment not found."}), 404

    if appointment.user_id != int(current_user_id):
        return jsonify({"error": "You are not authorized to complete this appointment."}), 403

    if appointment.status == "Completed":
        return jsonify({"message": "Appointment is already marked as completed."}), 200

    if appointment.status == "Cancelled":
        return jsonify({"error": "Cancelled appointments cannot be marked as completed."}), 400

    appointment.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Appointment marked as completed successfully."}), 200
 
    


    
