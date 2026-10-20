from flask import jsonify, request

from db import db
from models import warranty
from models.warranty import Warranties


def add_warranty():
    post_data = request.form if request.form else request.json

    fields = ["product_id", "warranty_months"]
    required_fields = ["product_id", "warranty_months"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    new_warranty = Warranties(
        product_id=values["product_id"],
        warranty_months=values["warranty_months"],
    )

    db.session.add(new_warranty)
    db.session.commit()

    query = db.session.query(Warranties).filter(Warranties.product_id == values["product_id"]).first()

    warranty = {
        "warranty_id": query.warranty_id,
        "product_id": query.product_id,
        "warranty_months": query.warranty_months
    }

    return jsonify({"message": "warranty created", "result": warranty}), 201


def get_all_warranties():
    query = db.session.query(Warranties).all()

    warranty_list = []

    for warranty in query:
        warranty_dict = {
            "warranty_id": warranty.warranty_id,
            "product_id": warranty.product_id,
            "warranty_months": warranty.warranty_months
        }
        warranty_list.append(warranty_dict)

    return jsonify({"message": "warranties found", "results": warranty_list}), 200


def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty does not exist"}), 404

    warranty = {
        "warranty_id": query.warranty_id,
        "product_id": query.product_id,
        "warranty_months": query.warranty_months
    }

    return jsonify({"message": "warranty found", "result": warranty}), 200


def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json

    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty does not exist"}), 404

    query.warranty_months = post_data.get("warranty_months", query.warranty_months)
    db.session.commit()

    warranty = {
        "warranty_id": query.warranty_id,
        "product_id": query.product_id,
        "warranty_months": query.warranty_months
    }

    return jsonify({"message": "warranty updated", "result": warranty}), 200

def delete_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": f"warranty does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete warranty"}), 400

    return jsonify({"message": "warranty deleted"}), 200
