from flask import Blueprint,jsonify
from app.models import Doctor
from flask import request,jsonify,Blueprint
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from app.models  import db ,Doctor , Appointment,User



doctors_blueprint = Blueprint('doctors',__name__,url_prefix='/doctors')

def doctor_required(fn):
    @jwt_required()
    def wrapper(*args,**kwargs):
        claims= get_jwt()
        if claims.get('role')  != 'doctor':
            return jsonify({"error": "doctors only!"}), 403
        return fn(*args,**kwargs)
    wrapper.__name__=fn.__name__
    return wrapper
   

@doctors_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_doctor_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or user.role != 'doctor':
        return jsonify({"error": "Access forbidden. Not a doctor."}), 403

    doctor = Doctor.query.filter_by(name=user.full_name).first()

    if not doctor:
        return jsonify({"error": "Doctor profile not found."}), 404

    return jsonify(doctor.to_dict()), 200




@doctors_blueprint.route('/appointments', methods=['GET'])
@jwt_required()
def get_doctor_appointments():
    """
    Get all appointments assigned to the current logged-in doctor.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or user.role != 'doctor':
        return jsonify({"error": "Access forbidden. Not a doctor."}), 403

    # Fetch the doctor
    doctor = Doctor.query.filter_by(name=user.full_name).first()

    if not doctor:
        return jsonify({"error": "Doctor profile not found."}), 404

    # Fetch appointments linked to this doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

    appointment_list = []
    for appointment in appointments:
        appointment_list.append({
            "appointment_id": appointment.id,
            "patient_id": appointment.user_id,
            "start_time": appointment.start_time,
            "end_time": appointment.end_time,
            "status": appointment.status
        })

    return jsonify(appointment_list), 200

 
@doctors_blueprint.route('/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    """
    Get detailed info for a single doctor by ID.
    """
    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return jsonify({"error": "Doctor not found."}), 404

    return jsonify(doctor.to_dict()), 200



