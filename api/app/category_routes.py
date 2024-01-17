from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import  Category
from app.main import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/create-category', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    category_name = data.get('category_name')

    if not category_name:
        return jsonify({'message': 'Category name is required'}), 400

    new_category = Category(category_name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully'}), 201

@category_bp.route('/get-categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = [{'category_id': category.category_id, 'category_name': category.category_name}
                     for category in categories]

    return jsonify({'categories': category_list})
