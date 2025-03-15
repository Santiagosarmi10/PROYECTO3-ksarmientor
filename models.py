from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heladeria.db'
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    es_empleado = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Puede ser 'admin', 'empleado' o 'cliente'

    def check_password(self, password):
        return self.password == password

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity={'id': user.id, 'es_admin': user.es_admin, 'es_empleado': user.es_empleado})
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    current_user = get_jwt_identity()
    if not current_user.get('es_admin'):
        return render_template('401.html'), 401
    return jsonify({'message': 'Bienvenido Admin'})

@app.route('/empleado', methods=['GET'])
@jwt_required()
def empleado():
    current_user = get_jwt_identity()
    if not current_user.get('es_empleado'):
        return render_template('401.html'), 401
    return jsonify({'message': 'Bienvenido Empleado'})

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
