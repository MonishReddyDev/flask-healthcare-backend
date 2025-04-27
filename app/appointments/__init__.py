from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Appointment,Doctor,db,User
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
        Appointment.end_time > start_time, # type: ignore
        Appointment.status.in_(["Pending", "Confirmed"]) # type: ignore
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
        status="Pending"
    )
    
    db.session.add(new_appointment)
    db.session.commit()
    
    return jsonify({
        "message": "Appointment booked successfully. Awaiting doctor confirmation.",
        "appointment_id": new_appointment.id
    }), 201


@appointments_bp.route('/<int:appointment_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(appointment_id):
    """
    Cancel an appointment (Patient or Doctor).
    """
    current_user_id = get_jwt_identity()
    
    user = User.query.get(current_user_id)

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found."}), 404
    
    if not user:
        return jsonify({"error": "User not found"}), 403

    # Check if user is the patient who booked or doctor assigned
    doctor = Doctor.query.filter_by(name=user.full_name).first()

    is_patient = appointment.user_id == current_user_id
    is_doctor = doctor and appointment.doctor_id == doctor.id

    if not (is_patient or (user.role == 'doctor' and is_doctor)):
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
    """
    Complete an appointment (Doctor only).
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or user.role != 'doctor':
        return jsonify({"error": "Only doctors can mark appointments as completed."}), 403

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found."}), 404

    # Check if doctor is assigned
    doctor = Doctor.query.filter_by(name=user.full_name).first()

    if not doctor or appointment.doctor_id != doctor.id:
        return jsonify({"error": "You are not authorized to complete this appointment."}), 403

    if appointment.status == "Completed":
        return jsonify({"message": "Appointment is already marked as completed."}), 200

    if appointment.status == "Cancelled":
        return jsonify({"error": "Cancelled appointments cannot be marked as completed."}), 400

    appointment.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Appointment marked as completed successfully."}), 200

 
 
@appointments_bp.route('/<int:appointment_id>/confirm', methods=['PUT'])
@jwt_required()
def confirm_appointment(appointment_id):
    """
    Doctor confirms a pending appointment (only his own).
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or user.role != 'doctor':
        return jsonify({"error": "Access forbidden. Only doctors can confirm appointments."}), 403

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found."}), 404

    # Find doctor entity from user full name (assuming user.full_name == doctor.name)
    doctor = Doctor.query.filter_by(name=user.full_name).first()

    if not doctor:
        return jsonify({"error": "Doctor profile not found."}), 404

    # ⚡ Important Security Check
    if appointment.doctor_id != doctor.id:
        return jsonify({"error": "You are not authorized to confirm this appointment."}), 403

    # Allow confirm only if pending
    if appointment.status != "Pending":
        return jsonify({"error": f"Cannot confirm appointment. Current status: {appointment.status}"}), 400

    # Confirm it
    appointment.status = "Confirmed"
    db.session.commit()

    return jsonify({"message": "Appointment confirmed successfully."}), 200

    


    
