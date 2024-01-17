from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import  Booking
from main import db
from datetime import datetime
from collections import defaultdict

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/bookings', methods=['GET'])
def get_bookings():
    data = request.get_json()
    user_id = data.get('user_id')

    if user_id is None:
        return jsonify({'message': 'User ID is required in the payload'}), 400

    bookings = Booking.query.filter_by(created_by_user_id=user_id).all()

    # Organize bookings by date
    bookings_by_date = defaultdict(list)

    for booking in bookings:
        start_datetime = booking.starttime.strftime('%d/%m/%Y')
        bookings_by_date[start_datetime].append({
            'id': f'booking_{booking.booking_id}',
            'title': booking.title,
            'created_by': booking.created_by_user.name, 
            'email': booking.created_by_user.email, 
            'startDate': booking.starttime.strftime('%d/%m/%Y %H:%M'),
            'endDate': booking.endtime.strftime('%d/%m/%Y %H:%M'),
        })

    # Convert defaultdict to a regular dictionary
    result = dict(bookings_by_date)

    return jsonify({'bookings': result})

@booking_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_booking = Booking(
        title=data['title'],
        created_by_user_id=user_id,
        category_id=data['category_id'],
        startTime=data['startTime'],
        endTime=data['endTime']
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully'}), 201

@booking_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    user_id = get_jwt_identity()
    booking = Booking.query.filter_by(booking_id=booking_id, created_by_user_id=user_id).first()

    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted successfully'})
    else:
        return jsonify({'message': 'Booking not found or you do not have permission to delete'}), 404
