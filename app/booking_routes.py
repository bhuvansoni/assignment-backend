from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.main import db
from app.models import Booking, User, Category

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.route("/", methods=["GET"])
def get_bookings():
    data = request.get_json()
   
    if "user_id" not in data:
        return jsonify({"error": "User ID is required in the request payload"}), 400

    user_id = data["user_id"]
    category_id = data.get("category_id")

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if category_id:
        bookings = Booking.query.filter_by(user_id=user_id, category_id=category_id).all()
    else:
        bookings = Booking.query.filter_by(user_id=user_id).all()

    response_data = []
    for booking in bookings:
        user_username = User.query.get(booking.user_id).username
        category_name = Category.query.get(booking.category_id).name

        response_data.append({
            "description": booking.description,
            "start_time": booking.start_time,
            "end_time": booking.end_time,
            "user_username": user_username,
            "category_name": category_name
        })

    return jsonify(bookings=response_data)

@booking_bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()
    required_fields = ["user_id", "category_id", "start_time", "end_time"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "User ID, category ID, start time, and end time are required"}), 400

    new_booking = Booking(
        user_id=data["user_id"],
        category_id=data["category_id"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        description=data.get("description", "")
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Booking created successfully"}), 201
