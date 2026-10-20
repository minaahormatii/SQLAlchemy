from flask import jsonify, request

from db import db
from models.category import Categories


def add_category():
    post_data = request.form if request.form else request.json

    fields = ["category_name"]
    required_fields = ["category_name"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    new_category = Categories(category_name=values["category_name"])

    db.session.add(new_category)
    db.session.commit()

    query = db.session.query(Categories).filter(Categories.category_name == values["category_name"]).first()

    category = {
        "category_id": query.category_id,
        "category_name": query.category_name
    }

    return jsonify({"message": "category created", "result": category}), 201


def get_all_categories():
    query = db.session.query(Categories).all()

    category_list = []

    for category in query:
        category_dict = {
            "category_id": category.category_id,
            "category_name": category.category_name
        }
        category_list.append(category_dict)

    return jsonify({"message": "categories found", "results": category_list}), 200


def get_category_by_id(category_id):
    query = (
        db.session.query(Categories).filter(Categories.category_id == category_id).first()
    )

    if not query:
        return jsonify({"message": "category does not exist"}), 404

    category = {
        "category_id": query.category_id,
        "category_name": query.category_name
    }

    return jsonify({"message": "category found", "result": category}), 200

def update_category_by_id(category_id):
    post_data = request.form if request.form else request.json

    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category does not exist"}), 404

    query.category_name = post_data.get("category_name", query.category_name)

    db.session.commit()

    category = {
        "category_id": query.category_id,
        "category_name": query.category_name
    }

    return jsonify({"message": "category updated", "result": category}), 200

def delete_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()


    if not query:
        return jsonify({"message": f"category does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete category"}), 400

    return jsonify({"message": "category deleted"}), 200