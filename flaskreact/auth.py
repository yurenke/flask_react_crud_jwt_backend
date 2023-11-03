from flaskreact.extensions import bcrypt
from flask import Blueprint
from flask import request
from flask import jsonify
from flaskreact.models import db, Account
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

bp = Blueprint("auth", __name__, url_prefix="/v1/auth")

@bp.route("/signup", methods=["POST"])
def signup():
    name = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    error = None

    if not name:
        error = "username is required"
    elif not email:
        error = "email is required"
    elif not password:
        error = "password is required"

    if error:
        return jsonify({"message": f"{error}"}), 400
   
    user_exists = Account.query.filter_by(email=email).first() is not None
   
    if user_exists:
        return jsonify({"message": "Email already exists"}), 409
       
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Account(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
   
    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "message": "User registered successfully!!"
    })

@bp.route('/signin', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400
  
    user = Account.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"message": "No such user"}), 401
      
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401
      
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
  
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.name,
        "accessToken": access_token,
        "refreshToken": refresh_token
    })

@bp.route("/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(accessToken=access_token)
