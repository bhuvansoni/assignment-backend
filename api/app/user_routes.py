from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.main import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, is_admin=True).first()

    if user and user.password == password:
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({'message': 'User already exists'}), 200
    else:
        new_user = User(name=name, email=email)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
