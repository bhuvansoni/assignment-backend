from flask import Blueprint, jsonify, request
from app.main import db
from app.models import Category

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    response_data = [{"category": category.name, "category_id": category.category_id} for category in categories]
    return jsonify(categories=response_data)

@category_bp.route("/", methods=["POST"])
def create_category():
    data = request.get_json()

    required_fields = ["name"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Category name is required"}), 400

    existing_category = Category.query.filter_by(name=data["name"]).first()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 400

    new_category = Category(name=data["name"])
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category created successfully"}), 201
