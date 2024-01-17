from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Booking
from api.main import db
from datetime import datetime
from collections import defaultdict
from api.user_routes import create_user, User
from api.models import Category

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/bookings", methods=["GET"])
def get_bookings():
    user_id = request.args.get("user_id")

    if user_id is None:
        return jsonify({"message": "User ID is required in the payload"}), 400

    bookings = Booking.query.filter_by(created_by_user_id=user_id).all()
    bookings_by_date = defaultdict(list)

    for booking in bookings:
        start_datetime = booking.starttime.strftime("%d/%m/%Y")
        category = Category.query.get(booking.category_id)

        bookings_by_date[start_datetime].append(
            {
                "id": booking.booking_id,
                "title": booking.title,
                "created_by": booking.created_by_user.name,
                "email": booking.created_by_user.email,
                "startDate": booking.starttime.strftime("%d/%m/%Y %H:%M"),
                "endDate": booking.endtime.strftime("%d/%m/%Y %H:%M"),
                "category_id": category.category_id,
                "category_name": category.category_name,
            }
        )

    # Convert defaultdict to a regular dictionary
    result = dict(bookings_by_date)

    return jsonify({"bookings": result})


@booking_bp.route("/get-bookings-admin", methods=["GET"])
@jwt_required()  # You may want to add additional checks for admin role
def get_bookings_admin():
    try:
        # Get user ID from the JWT token
        user_id = get_jwt_identity()

        # Check if the user is an admin (you may have a different way to determine admin status)
        user = User.query.filter_by(user_id=user_id, is_admin=True).first()
        if not user:
            return jsonify({"message": "User is not an admin"}), 403

        # Fetch all bookings
        bookings = Booking.query.all()

        # Organize bookings by date
        bookings_by_date = defaultdict(list)

        for booking in bookings:
            start_datetime = booking.starttime.strftime("%d/%m/%Y")
            category = Category.query.get(booking.category_id)
            bookings_by_date[start_datetime].append(
                {
                    "id": booking.booking_id,
                    "title": booking.title,
                    "created_by": booking.created_by_user.name,
                    "email": booking.created_by_user.email,
                    "startDate": booking.starttime.strftime("%d/%m/%Y %H:%M"),
                    "endDate": booking.endtime.strftime("%d/%m/%Y %H:%M"),
                    "category_id": category.category_id,
                    "category_name": category.category_name,
                }
            )

        # Convert defaultdict to a regular dictionary
        result = dict(bookings_by_date)

        return jsonify({"bookings": result}), 200

    except Exception as e:
        return (
            jsonify(
                {"message": "Error occurred while fetching bookings", "error": str(e)}
            ),
            500,
        )


@booking_bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    user_id = create_user(data["name"], data["email"])
    start_time = datetime.strptime(data["startTime"], "%Y-%m-%dT%H:%M")
    end_time = datetime.strptime(data["endTime"], "%Y-%m-%dT%H:%M")

    new_booking = Booking(
        title=data["title"],
        created_by_user_id=user_id,
        category_id=data["category_id"],
        starttime=start_time,
        endtime=end_time,
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Booking created successfully", "user_id": user_id}), 201


@booking_bp.route("/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def delete_booking(booking_id):
    user_id = get_jwt_identity()
    booking = Booking.query.filter_by(booking_id=booking_id).first()

    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking deleted successfully"})
    else:
        return (
            jsonify(
                {"message": "Booking not found or you do not have permission to delete"}
            ),
            404,
        )


@booking_bp.route("/<int:booking_id>", methods=["PUT"])
@jwt_required()
def update_booking(booking_id):
    try:
        user_id = get_jwt_identity()

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        if not user.is_admin:
            booking = Booking.query.filter_by(booking_id=booking_id, created_by_user_id=user_id).first()
            if not booking:
                return jsonify({"message": "Booking not found or you do not have permission to update"}), 404

        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"message": "Booking not found"}), 404


        data = request.get_json()
        booking.title = data.get("title", booking.title)
        booking.category_id = data.get("category_id", booking.category_id)
        booking.starttime = data.get("startTime", booking.starttime)
        booking.endtime = data.get("endTime", booking.endtime)

        db.session.commit()

        return jsonify({"message": "Booking updated successfully"}), 200

    except Exception as e:
        return jsonify({"message": f"Error occurred while updating booking: {str(e)}"}), 500
