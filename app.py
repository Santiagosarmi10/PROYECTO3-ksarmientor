from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heladeria.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'clave_secreta' 

db = SQLAlchemy(app)
jwt = JWTManager(app)

# MODELOS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) 

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)

# CREAR BASE DE DATOS
with app.app_context():
    db.create_all()

# RUTA LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    
    if not user or user.password != password:
        return jsonify({'msg': 'Usuario o contraseña incorrectos'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# RUTA PARA OBTENER PRODUCTOS
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'calorias': p.calorias} for p in productos])

# RUTA PARA AGREGAR UN PRODUCTO (PROTEGIDA CON JWT)
@app.route('/productos', methods=['POST'])
@jwt_required()
def add_producto():
    current_user = get_jwt_identity()
    data = request.get_json()
    nuevo_producto = Producto(nombre=data['nombre'], precio=data['precio'], calorias=data['calorias'])
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'msg': f'Producto agregado por {current_user}'})

if __name__ == '__main__':
    app.run(debug=True)
