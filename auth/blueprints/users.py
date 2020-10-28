from flask import Blueprint, request, make_response, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import User, Budget, Category
from auth.extensions import db
from auth.forms import ProductForm
import uuid
import jwt
from datetime import datetime, timedelta
from auth.helpers import token_required
from auth.seed.initial_data import initial_categories

users = Blueprint('users', __name__)


@users.route('/private', methods=['GET'])
@token_required
def get_all_users(current_user):
    return jsonify({'private': "correctly logged in"})


""" @ToDo: Extract in model methods """


@users.route('/signup', methods=['POST'])
def signup():
    data = request.form
    email, password = data.get('email'), data.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        try:
            public_user_id = str(uuid.uuid4())
            user = User(public_id=public_user_id, email=email,
                        password=generate_password_hash(password))
            db.session.add(user)
            budget = Budget(user_id=public_user_id)
            db.session.add(budget)

            for category in initial_categories:
                new_category = Category(category_id=category['id'], expense_type=category['expenseType'], budget_type=category[
                                        'budgetType'], value=category['value'], caption=category['caption'], color=category['color'], user_id=public_user_id)
                db.session.add(new_category)

            db.session.commit()
            response = jsonify(
                {'public_id': user.public_id, 'email': user.email})
            return make_response(response, 200)
        except AssertionError as err:
            response = jsonify({'code': 400, 'message': str(err)})
            return make_response(response)
    else:
        response = jsonify({'code': 400, 'message': 'email already exists'})
        return make_response(response)


@users.route('/login', methods=['POST'])
def login():
    data = request.form
    if not data or not data.get('email') or not data.get('password'):
        response = jsonify(
            {'code': 400, 'message': 'Both email and password are required'})

    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        response = jsonify(
            {'code': 400, 'message': 'Wrong email, please try again...'})

    if check_password_hash(user.password, data.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, current_app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8'), 'exp': datetime.utcnow() + timedelta(days=30)}), 201)
    return make_response(jsonify({'code': 400, 'message': 'Wrong password, please try again'}))
