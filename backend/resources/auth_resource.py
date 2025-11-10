"/login"
"/register"

from flask import Blueprint, jsonify, request
from flask_security.utils import verify_password, hash_password

from models import User, db

from flask import current_app

auth_bp = Blueprint("auth",__name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    if (not email or not password):
        return jsonify({"message": "invalid input"}), 400
    
    user = User.query.filter_by(email = email).first_or_404()

    if not verify_password(password, user.password):
        return jsonify({'message': 'wrong password'}), 400
    
    return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "token": user.get_auth_token(),
            "role": user.roles[0].name,
        }), 200


@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    role = data['role']

    active = True

    if not name or not email or not password or not role in ["manager", "customer"]:
        return jsonify({"message": "invalid inputs"})
    
    if role == "manager":
        active = False


    datastore = current_app.datastore

    if User.query.filter_by(email = email).first():
        return {"message": "user already exists"}, 400

    datastore.create_user(name = name, email = email, password = hash_password(password), active = active)
    try:
        db.session.commit()
    except:
        return {"message" : "error"}, 400
    
    role = datastore.find_role(role)
    user = datastore.find_user(email = email)
    datastore.add_role_to_user(user, role)
    try:
        db.session.commit()
    except:
        return {"message" : "error"}, 400
    

    
    return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }), 201
