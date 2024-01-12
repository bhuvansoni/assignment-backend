from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.main import db
from app.models import Booking, User, Category
import uuid
from datetime import datetime

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.route("/", methods=["GET"])
def get_bookings():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id:
        return jsonify({"error": "User ID is required as a query parameter"}), 400

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

@booking_bp.route("/", methods=["PUT"])
def update_booking():
    data = request.get_json()
    booking_id = data.get("booking_id")

    if not booking_id:
        return jsonify({"error": "Booking ID is required"}), 400

    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # Update fields if provided
    if "user_id" in data:
        booking.user_id = data["user_id"]
    if "category_id" in data:
        booking.category_id = data["category_id"]
    if "start_time" in data:
        booking.start_time = data["start_time"]
    if "end_time" in data:
        booking.end_time = data["end_time"]
    if "description" in data:
        booking.description = data["description"]

    db.session.commit()

    return jsonify({"message": "Booking updated successfully"}), 200

@booking_bp.route("/", methods=["DELETE"])
def delete_booking():
    data = request.get_json()
    booking_id = data.get("booking_id")

    if not booking_id:
        return jsonify({"error": "Booking ID is required"}), 400

    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    db.session.delete(booking)
    db.session.commit()

    return jsonify({"message": "Booking deleted successfully"}), 200
