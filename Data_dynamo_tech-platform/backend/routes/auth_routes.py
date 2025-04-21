from flask import Blueprint, request, jsonify
from models.user_model import User
from utils.auth import generate_token
from app import db

auth_bp = Blueprint('auth', __name__)
user_model = User(db)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if user_model.find_user(data['email']):
        return jsonify({'msg': 'User already exists'}), 400
    user_model.create_user(data['email'], data['password'])
    return jsonify({'msg': 'User created successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = user_model.find_user(data['email'])
    if user and user_model.check_password(user['password'], data['password']):
        token = generate_token(user['email'])
        return jsonify({'token': token})
    return jsonify({'msg': 'Invalid credentials'}), 401
