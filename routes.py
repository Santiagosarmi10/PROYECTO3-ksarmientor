from flask import request, jsonify
from flask_jwt_extended import create_access_token
from configuracion import app, db
from models import User

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Usuario ya existe"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.authenticate(username, password)

    if not user:
        return jsonify({"message": "Credenciales incorrectas"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
