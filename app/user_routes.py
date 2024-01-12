from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.main import db
from app.models import User

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(users=[user.username for user in users])

@user_bp.route("/login_or_create", methods=["POST"])
def login_or_create_user():
    data = request.get_json()

    required_fields = ["username", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if user:
        # User exists, return data including is_admin
        access_token = create_access_token(identity=user.username)
        return jsonify({"user_id": user.user_id, "is_admin": user.is_admin, "access_token": access_token}), 200
    else:
        # User doesn't exist, create user and return data
        new_user = User(username=data["username"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.username)
        return (
            jsonify({"user_id": new_user.user_id, "is_admin": new_user.is_admin, "message": "User created successfully", "access_token": access_token}),
            201,
        )
