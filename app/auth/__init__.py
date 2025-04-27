from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from datetime import timedelta
from app.models import User, db



auth = Blueprint('auth',__name__,url_prefix="/auth")


@auth.route('/register', methods=['POST'])
def  register():
    data = request.get_json()
    
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'patient')
    
    if not full_name or not email or not password:
        return jsonify({'error': 'Full name, email, and password are required'}),400
    
    existing_user= User.query.filter_by(email=email).first()
    
    if existing_user:
         return jsonify({'error': 'Email already registered'}), 409
    
    user = User(full_name=full_name, email=email, role=role)
    
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

    
    
@auth.route('/login',methods=['POST'])  
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password :
        return jsonify({'error': 'Email and password are required'}), 400
        
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    additional_claims ={
        'email': user.email,
        'role': user.role
    }
    
    access_Token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=1))
    
    return jsonify({
        "access_token": access_Token,
        "email": email,
        "role": user.role
        
        }),200
    
        

@auth.route('/profile', methods=['GET'])
@jwt_required()
def get_current_user():
  
    identity=get_jwt_identity()
    claims=get_jwt()
    
    return jsonify({
        "id": identity,
        "email": claims.get('email'),
        "role": claims.get('role')
    }), 200

    
@auth.route('/profile', methods=['PUT'])
@jwt_required()
def update_user():
    


    current_user_id =get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    full_name = data.get('full_name')
    email = data.get('email')
    
    if full_name:
        user.full_name = full_name
    if email:
        user.email=email
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }
    }), 200