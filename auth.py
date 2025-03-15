from flask import Blueprint, request, jsonify
import jwt
import datetime
from functools import wraps
from models import db, User

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "supersecretkey"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token es requerido"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["user_id"]).first()
        except:
            return jsonify({"message": "Token inválido"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Credenciales inválidas"}), 401

    token = jwt.encode(
        {"user_id": user.id, "role": user.role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify({"token": token})
