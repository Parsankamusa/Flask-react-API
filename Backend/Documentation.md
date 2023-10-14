# My documentation on the http security
* https security is very crucial from external attack
* Bellow are some featured I have implemented to ensure that my endpoint in the flask api are secure

# 1. Flask-Talisman 
* Flask extension that helps you to add HTTP security headers to your Flask application. These headers tell the browser how to behave when interacting with your site. For example, some headers can prevent the browser from running any JavaScript that didn't originate from your site, which can help prevent Cross-Site Scripting (XSS) attacks.

# Installing SSL certificate
* For talisman to you should have an SSL certificate. here is the command to install the certificate:
 ```bash
   # Generate a self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run Flask app over HTTPS
flask run --cert=cert.pem --key=key.pem
   ```
# 2. CORS (Cross-Origin Resource Sharing).
* It's a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin. A web application executes a cross-origin HTTP request when it requests a resource from a different domain, protocol, or port than the one from which the current document originated.
* CORS adds another layer of security to help ensure that only trusted domains can access your site's resources. 
# 3. Using bcrypt for password hashing
* It is an adaptive hash function, which means that it can be configured to use more computational resources (in terms of time and memory) as technology progresses

# 4. Using session for server-side session management
* Flask-Session is a Flask extension that adds support for server-side session to your application. It uses the Werkzeug user session object as a base and extends it with server-side session support

# 5. Using dotenv for environment variable management
* python-dotenv is a Python library that allows you to specify environment variables in a .env file. This is useful for managing sensitive data such as API keys and database URIs, which should not be hard-coded into your application

## Prerequisites
Before getting started, ensure you have the following installed on your system:
- The latest python version
- An editor such as Vs code or Pycharm

## Installation
Follow these steps to set up and run the project:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Parsankamusa/Flask-react-API.git
   ```
   
2. Navigate to the project directory 
   ```bash
   cd Flask-react-API
   ```
3. Run the following command to set up virtual environment:
   ```bash
   python -m venv env
   ```
   ```bash
   env/Scripts/activate
   ```
4. Run the following command to install dependencies:
   ```bash
   pip install flask_sqlalchemy
   ```
   ```bash
   pip install request
   ```
   ```
   ```bash
  from flask_cors import CORS, cross_origin
   ```
   ```
   ```bash
  from flask_session import Session
   ```
    ```bash
  from flask_talisman import Talisman
   ```
5. Create a app.py  file in the project root and configure your SQLAIchemy:
   ```bash
   from flask import Flask, request, jsonify
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
   db = SQLAlchemy(app)
   ```
   ```
6. Creating a database model:
   ```bash
   db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
   ```
   ```
7. creating a route to login:
   ```bash
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
   ```

8. creating a route to register:
   ```bash
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
   ```

   9 creating a route to check balance:
   ```bash
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
   ```
10. Run the following command to start the server:
   ```bash
   python app.py or flask run
   ```

Your Flask server should now be running at http://localhost:5000.

 ## Documentation
* The documentation include test  using postman or curl to verify the API's functionality.
    https://www.baeldung.com/curl-rest
  here is a link  for post documentation [postman](https://documenter.getpostman.com/view/24185831/2s9YC2zZAG)
  
## Testing 
  * CURL TESTING
 * Run the following commands to query your api:
     1. POST
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"email": "john@gmail.com", "password":"your_password"}' http://127.0.0.1:5000/register
   Musa@DESKTOP-RPBI479 MINGW64 ~/Desktop/Flask-react/Backend
   $ curl -X POST -H "Content-Type: application/json" -d '{"email": "john@gmail.com", "password":"john123"}' http://127.0.0.1:5000/api
   {
   "message": "user created successfully"
   }
   ```

   # Frondend Part
   # setting up proxy
    ```bash
   {
  "name": "front-react",
  "version": "0.1.0",
  "private": true,
  "proxy": "http://localhost:5000",
  }
   ```
# Installing and setting up axios
 ```bash
import axios from "axios";

export default axios.create({
  withCredentials: true,
});
   ```
# setting up checkbalance Page
```bash
import React, { useState } from "react";
import httpClient from "./httpClient";

// BalancePage component
const BalancePage = () => {
  const [username, setUsername] = useState("");
  const [balance, setBalance] = useState("");

  const fetchBalance = async () => {
    try {
      const resp = await httpClient.get(`//localhost:5000/account/${username}`);
      setBalance(resp.data.balance);
    } catch (error) {
      alert("Error fetching balance");
    }
  };

  return (
    <div>
      <h1>Check Balance</h1>
      <label>Username: </label>
      <input 
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button type="button" onClick={fetchBalance}>
        Fetch Balance
      </button>
      {balance && <p>Balance: {balance}</p>}
    </div>
  );
};

export default BalancePage;
   ``