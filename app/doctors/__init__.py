from flask import Blueprint,jsonify
from app.models import Doctor


doctors_blueprint = Blueprint('doctors',__name__,url_prefix='/doctors')


@doctors_blueprint.route("/",methods=['GET'])
def get_all_doctors():
    doctors = Doctor.query.all()
    doctors_list =[]
    
    for doctor in doctors:
        doctors_list.append({
            'id': doctor.id,
            'name': doctor.name,
            'specialization': doctor.specialization,
            'experience': doctor.experience,
            'availability': doctor.availability,
            'rating': doctor.rating
        })   
    return jsonify(doctors_list),200