from flask import request,jsonify,Blueprint
from flask_jwt_extended import jwt_required,get_jwt
from app.models  import db ,Doctor , Appointment,User


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(fn):
    @jwt_required()
    def wrapper(*args,**kwargs):
        claims= get_jwt()
        if claims.get('role')  != 'admin':
            return jsonify({"error": "Admins only!"}), 403
        return fn(*args,**kwargs)
    wrapper.__name__=fn.__name__
    return wrapper
    

@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found."}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully."}), 200
    
    
    
@admin_bp.route('/doctor', methods=['POST'])
@admin_required
def create_doctor():
    data=request.get_json()
    name = data.get('name')
    specialization = data.get('specialization')
    experience = data.get('experience')
    availability = data.get('availability')
   
    if not name and not specialization:
          return jsonify({"error": "Name and specialization are required."}), 400
      
    new_doctor=Doctor(
        name=name,
        specialization=specialization,
        experience=experience,
        availability=availability
    )
    
    db.session.add(new_doctor)
    db.session.commit()
    
    return jsonify({
        "message": "Doctor created successfully!",
        "doctor_id": new_doctor.id
    }), 201
    
    
@admin_bp.route('/doctor/<int:doctor_id>', methods=['PUT'])
@admin_required
def update_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found."}), 404
    
    data= request.get_json()
    doctor.name = data.get('name', doctor.name)
    doctor.specialization = data.get('specialization', doctor.specialization)
    doctor.experience = data.get('experience', doctor.experience)
    doctor.availability = data.get('availability', doctor.availability)
    
    db.session.commit()
    return jsonify({"message": "Doctor updated successfully."}), 200
    
    

@admin_bp.route('/doctor/<int:doctor_id>', methods=['DELETE'])
@admin_required
def delete_doctor(doctor_id):
    
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return jsonify({"error": "Doctor not found."}), 404

    if doctor.appointments:
        return jsonify({"error": "Cannot delete doctor with existing appointments."}), 400
  
    db.session.delete(doctor)
    db.session.commit()

    return jsonify({"message": "Doctor deleted successfully."}), 200

    
 
@admin_bp.route('/appointments', methods=['GET'])
@admin_required
def view_all_appointments():
    appointments = Appointment.query.all()

    appointments_list = []
    for appointment in appointments:
        appointments_list.append({
            "appointment_id": appointment.id,
            "user_id": appointment.user_id,
            "doctor_id": appointment.doctor_id,
         
            "status": appointment.status,
            "created_at": appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(appointments_list), 200


@admin_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@admin_required
def delete_appointment(appointment_id):
    if appointment_id==0:
        deleted = Appointment.query.delete()#Bulk delete
        db.session.commit()
        
        if deleted == 0:
            return jsonify({"message": "No appointments found to delete."}), 200
        
        return jsonify({"message": f"All {deleted} appointments deleted successfully."}), 200
    else:
        try:
            appointment_id = int(appointment_id)
        except ValueError:
            return jsonify({"error": "Invalid appointment ID."}), 400
    
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return jsonify({"error": "Appointment not found."}), 404

        db.session.delete(appointment)
        db.session.commit()

        return jsonify({"message": "Appointment deleted successfully."}), 200
 
    

