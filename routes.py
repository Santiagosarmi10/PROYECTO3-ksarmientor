from flask import Blueprint, jsonify, request
from database import db
from models import Producto
from models import db
from decorators import admin_required, employee_required, customer_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([{"id": p.id, "nombre": p.nombre, "precio": p.precio} for p in productos])


@api_bp.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify({"id": producto.id, "nombre": producto.nombre, "precio": producto.precio})
    return jsonify({"error": "Producto no encontrado"}), 404

@api_bp.route('/productos/nombre/<string:nombre>', methods=['GET'])
def get_producto_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first()
    if producto:
        return jsonify({"id": producto.id, "nombre": producto.nombre, "precio": producto.precio})
    return jsonify({"error": "Producto no encontrado"}), 404


@api_bp.route('/productos/<int:id>/calorias', methods=['GET'])
def get_calorias(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify({"calorias": producto.calorias})
    return jsonify({"error": "Producto no encontrado"}), 404


@api_bp.route('/productos/<int:id>/rentabilidad', methods=['GET'])
def get_rentabilidad(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify({"rentabilidad": producto.rentabilidad()})
    return jsonify({"error": "Producto no encontrado"}), 404


@api_bp.route('/productos/<int:id>/vender', methods=['POST'])
def vender_producto(id):
    producto = Producto.query.get(id)
    if producto and producto.inventario > 0:
        producto.inventario -= 1
        db.session.commit()
        return jsonify({"message": "Producto vendido con éxito", "inventario_restante": producto.inventario})
    return jsonify({"error": "Producto no disponible"}), 400

def get_all_products():
    return jsonify({"message": "Lista de productos"}), 200

@api_bp.route("/productos/<int:producto_id>", methods=["GET"])
@customer_required
def get_product(current_user, producto_id):
    return jsonify({"message": f"Producto {producto_id}"}), 200

@api_bp.route("/productos/<int:producto_id>/calorias", methods=["GET"])
@customer_required
def get_calories(current_user, producto_id):
    return jsonify({"message": f"Calorías del producto {producto_id}"}), 200

@api_bp.route("/productos/<int:producto_id>/rentabilidad", methods=["GET"])
@admin_required
def get_rentabilidad(current_user, producto_id):
    return jsonify({"message": f"Rentabilidad del producto {producto_id}"}), 200
