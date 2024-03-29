from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import User
from datetime import timedelta
from api.main import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, is_admin=True).first()

    if user and user.password == password:
        expiry_time = timedelta(days=1)
        access_token = create_access_token(identity=user.user_id, expires_delta=expiry_time)
        return (
            jsonify(
                {"access_token": access_token, "email": user.email, "name": user.name, "user_id": user.user_id}
            ),
            200,
        )
    else:
        return jsonify({"message": "Invalid credentials"}), 401



def create_user(name, email):

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return existing_user.user_id
    else:
        new_user = User(name=name, email=email)

        db.session.add(new_user)
        db.session.commit()
        return  new_user.user_id
