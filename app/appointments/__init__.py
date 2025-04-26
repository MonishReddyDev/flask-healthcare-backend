from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Appointment,Doctor,db

appointments_bp = Blueprint('appointments', __name__, url_prefix='/appointments')


@appointments_bp.route('/',methods=['POST'])
@jwt_required()
def book_appointment():
    data = request.get_json()
    doctor_id= data.get('doctor_id')
    appointment_time = data.get('appointment_time')
    
    if not doctor_id or not appointment_time:
        return jsonify({"error": "Doctor ID and Appointment Time are required."}), 400
    
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return jsonify({"error": "Doctor not found."}), 404
    
    existing_appointment=Appointment.query.filter_by(
        doctor_id=doctor_id,
        appointment_time=appointment_time,
         status="Booked"
    ).first()
    
    if existing_appointment:
        return jsonify({"error": "Doctor is already booked for this time slot."}), 409  # Conflict


    
    current_user_id= get_jwt_identity()
    
    new_appointment = Appointment(
        user_id=int(current_user_id),
        doctor_id=doctor_id,
        appointment_time=appointment_time
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
 
    


    
