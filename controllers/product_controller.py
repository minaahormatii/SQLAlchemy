from flask import jsonify, request

from db import db
from models import product
from models.category import Categories
from models.company import Companies
from models.product import Products


def add_product():
    post_data = request.form if request.form else request.json

    fields = ["company_id", "product_name", "description", "price"]
    required_fields = ["company_id", "product_name", "price"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    new_product = Products(
        company_id=values["company_id"],
        product_name=values["product_name"],
        description=values["description"],
        price=values["price"],
    )

    db.session.add(new_product)
    db.session.commit()

    product_query = db.session.query(Products).filter(Products.product_name == values["product_name"]).first()

    company_query = db.session.query(Companies).filter(Companies.company_id == values["company_id"]).first()

    company_dict = {
        "company_id": company_query.company_id,
        "company_name": company_query.company_name
    }

    product_dict = {
        "product_id": product_query.product_id,
        "company": company_dict,
        "product_name": product_query.product_name,
        "description": product_query.description,
        "price": product_query.price,
        "active": product_query.active
    }

    return jsonify({"message": "product created", "result": product_dict}), 201

def create_product_category():
    post_data = request.form if request.form else request.json

    fields = ["product_id", "category_id"]
    required_fields = ["product_id", "category_id"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    product_query = db.session.query(Products).filter(Products.product_id == values["product_id"]).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == values["category_id"]).first()

    if not product_query:
        return jsonify({"message": "Product does not exist"}), 404

    if not category_query:
        return jsonify({"message": "Category does not exist"}), 404

    product_query.categories.append(category_query)

    db.session.commit()

    category_list = []
    for category in product_query.categories:
        category_dict = {
            "category_id": category.category_id,
            "category_name": category.category_name
        }
        category_list.append(category_dict) 

    company_dict = {
        "company_id": product_query.company.company_id,
        "company_name": product_query.company.company_name
    }

    if product_query.warranty:
        warranty_dict = {
            "warranty_id": product_query.warranty.warranty_id,
            "warranty_months": product_query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product_dict = {
        "product_id": product_query.product_id,
        "product_name": product_query.product_name,
        "description": product_query.description,
        "price": product_query.price,
        "active": product_query.active,
        "company": company_dict,
        "categories": category_list,
        "warranty": warranty_dict
    }

    return jsonify({"message": "category added to product", "result": product_dict}), 200

def get_all_products():
    query = db.session.query(Products).all()

    product_list = []

    for product in query:
        company_dict = {
            "company_id": product.company.company_id,
            "company_name": product.company.company_name
        }

        category_list = []
        for category in product.categories:
            category_dict = {
                "category_id": category.category_id,
                "category_name": category.category_name
            }
            category_list.append(category_dict)

        if product.warranty:
            warranty_dict = {
                "warranty_id": product.warranty.warranty_id,
                "warranty_months": product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "description": product.description,
            "price": product.price,
            "active": product.active,
            "company": company_dict,
            "categories": category_list,
            "warranty": warranty_dict
        }

        product_list.append(product_dict)

    return jsonify({"message": "products found", "results": product_list}), 200

def get_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product does not exist"}), 404

    company_dict = {
        "company_id": query.company.company_id,
        "company_name": query.company.company_name
    }

    category_list = []
    for category in query.categories:
        category_dict = {
            "category_id": category.category_id,
            "category_name": category.category_name
        }
        category_list.append(category_dict)

    if query.warranty:
        warranty_dict = {
            "warranty_id": query.warranty.warranty_id,
            "warranty_months": query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product_dict = {
        "product_id": query.product_id,
        "product_name": query.product_name,
        "description": query.description,
        "price": query.price,
        "active": query.active,
        "company": company_dict,
        "categories": category_list,
        "warranty": warranty_dict
    }

    return jsonify({"message": "product found", "result": product_dict}), 200

def get_products_by_company_id(company_id):
    query = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not query:
        return jsonify({"message": "no products found for this company"}), 404

    product_list = []

    for product in query:
        company_dict = {
            "company_id": product.company.company_id,
            "company_name": product.company.company_name
        }

        category_list = []
        for category in product.categories:
            category_dict = {
                "category_id": category.category_id,
                "category_name": category.category_name
            }
            category_list.append(category_dict)

        if product.warranty:
            warranty_dict = {
                "warranty_id": product.warranty.warranty_id,
                "warranty_months": product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "description": product.description,
            "price": product.price,
            "active": product.active,
            "company": company_dict,
            "categories": category_list,
            "warranty": warranty_dict
        }

        product_list.append(product_dict)

    return jsonify({"message": "products found", "results": product_list}), 200

def get_active_products():
    query = db.session.query(Products).filter(Products.active == True).all()

    product_list = []

    for product in query:
        company_dict = {
            "company_id": product.company.company_id,
            "company_name": product.company.company_name
        }

        category_list = []
        for category in product.categories:
            category_dict = {
                "category_id": category.category_id,
                "category_name": category.category_name
            }
            category_list.append(category_dict)

        if product.warranty:
            warranty_dict = {
                "warranty_id": product.warranty.warranty_id,
                "warranty_months": product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "description": product.description,
            "price": product.price,
            "active": product.active,
            "company": company_dict,
            "categories": category_list,
            "warranty": warranty_dict
        }

        product_list.append(product_dict)

    return jsonify({"message": "active products found", "results": product_list}), 200

def update_product_by_id(product_id):
    post_data = request.form if request.form else request.json

    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product does not exist"}), 404

    query.company_id = post_data.get("company_id", query.company_id)
    query.product_name = post_data.get("product_name", query.product_name)
    query.description = post_data.get("description", query.description)
    query.price = post_data.get("price", query.price)
    query.active = post_data.get("active", query.active)

    db.session.commit()

    company_dict = {
        "company_id": query.company.company_id,
        "company_name": query.company.company_name
    }

    category_list = []
    for category in query.categories:
        category_dict = {
            "category_id": category.category_id,
            "category_name": category.category_name
        }
        category_list.append(category_dict)

    if query.warranty:
        warranty_dict = {
            "warranty_id": query.warranty.warranty_id,
            "warranty_months": query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product_dict = {
        "product_id": query.product_id,
        "product_name": query.product_name,
        "description": query.description,
        "price": query.price,
        "active": query.active,
        "company": company_dict,
        "categories": category_list,
        "warranty": warranty_dict
    }

    return jsonify({"message": "product updated", "result": product_dict}), 200

def delete_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete product"}), 400

    return jsonify({"message": "product deleted"}), 200