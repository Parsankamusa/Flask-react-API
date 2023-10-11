from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db' 
app.config['JWT_SECRET_KEY'] = 'my_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=18)
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
#@jwt_required
def signup():
    data = request.get_json()  # get data from POST request
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Must provide username and password'}), 400

    # Here you should add a function to save the user in your database
    # For example, using Flask-SQLAlchemy:
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
@app.route('/login', methods=['POST'])
#@jwt_required
def login():
    data = request.get_json()  # get data from POST request
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Must provide username and password'}), 400

    # a function to verify the user in your database
    # For example, using Flask-SQLAlchemy:
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'username': user.username, 'password_hash': user.password_hash})



accounts = {
        'user1': 5000,  # initial balance
        'user2': 3000,
        'user3': 4000,
        'user4': 6000,
        'user5': 7000,
        'user6': 8000,
    }


@app.route('/balance/<username>', methods=['GET'])
#@jwt_required
def balance(username):
        if username in accounts:
            return jsonify({ 'balance': accounts[username] })
            
        else:
            return jsonify({ 'error': 'User not found' }), 404
    
@app.route('/transfer', methods=['POST'])
#@jwt_required
def transfer():
        data = request.get_json()
        from_user = data.get('from')
        to_user = data.get('to')
        amount = data.get('amount')
        if from_user  in accounts or to_user  in accounts or amount >= 0:
              return jsonify({'message': 'Transfer successful'})
        # Validate users and amount
        if from_user not in accounts or to_user not in accounts or amount <= 0:
            return jsonify({ 'error': 'Invalid request' }), 400

        # Validate sufficient funds
        if accounts[from_user] < amount:
            return jsonify({ 'error': 'Insufficient funds' }), 400

        # Perform the transfer
        accounts[from_user] -= amount
        accounts[to_user] += amount

        return jsonify({ 'success': True })
    
@app.errorhandler(500)
def internal_server_error(e):
     return "An error occurred: " + str(e), 500