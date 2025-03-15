from functools import wraps
from flask import request, jsonify
import jwt
from models import User

SECRET_KEY = "supersecretkey"

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"message": "Token requerido"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_user = User.query.filter_by(id=data["user_id"]).first()
                if current_user.role not in roles:
                    return jsonify({"message": "No autorizado"}), 403
            except:
                return jsonify({"message": "Token inválido"}), 401

            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

admin_required = role_required(["admin"])
employee_required = role_required(["admin", "empleado"])
customer_required = role_required(["admin", "empleado", "cliente"])
