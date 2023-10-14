from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
#from flask_talisman import Talisman
from config import ApplicationConfig
from models import db, User
#from flask_cors import CORS

app = Flask(__name__)
#loading the application
app.config.from_object(ApplicationConfig)
#Talisman(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()




@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 

@app.route("/register", methods=["POST"])
def register_user():
    #getting the data from json file
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"
#homepage route
@app.route('/', methods = ['GET'])
def homepage():
     return jsonify({'MESSAGE':' HELLO THIS MY HOMEPAGE'})

# This is a simple in-memory storage for the accounts
accounts = {
    'account1': {'balance': 1000},
    'account2': {'balance': 2000},
    'account3': {'balance': 1000},
    'account4': {'balance': 2000},
}


@app.route('/account/<account_name>', methods=['GET'])
def get_account(account_name):
    if account_name not in accounts:
        response = jsonify({'error': 'Account not found'})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    response = jsonify(accounts[account_name])
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Bad Request'}), 400
    from_account = data.get('from')
    to_account = data.get('to')
    amount = float(data.get('amount'))

    if not from_account or not to_account or amount is None:
        return jsonify({'error': 'Bad Request'}), 400

    
    if from_account not in accounts or to_account not in accounts:
        response = jsonify({'error': 'Account not found'})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404

    if accounts[from_account]['balance'] < amount:
        response = jsonify({'error': 'Insufficient funds'})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400

    accounts[from_account]['balance'] -= amount
    accounts[to_account]['balance'] += amount

    response = jsonify({'message': 'Transfer successful'})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response, 200


if __name__ == '__main__':
    app.run(debug=True)
