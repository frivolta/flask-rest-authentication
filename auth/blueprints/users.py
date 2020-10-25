from flask import Blueprint, request, make_response,jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import User
from auth.extensions import db
from auth.forms import ProductForm
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps

users = Blueprint('users', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            response = jsonify({'code': 401, 'message': 'Token is missing'})
            return response

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            response = jsonify({'code': 401, 'message': 'Token is invalid'})
            return response
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated

@users.route('/private', methods=['GET'])
@token_required
def get_all_users(current_user):
    return jsonify({'private': "correctly logged in"})


@users.route('/signup', methods=['POST'])
def signup():
  data = request.form
  email, password = data.get('email'), data.get('password')
  user = User.query.filter_by(email=email).first()

  if not user:
    try:
        user = User(public_id=str(uuid.uuid4()),email=email,password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        response = jsonify({'public_id': user.public_id,'email': user.email})
        return make_response(response, 200)
    except:
        response = jsonify({'code': 400, 'message': 'Generic error'})
        return make_response(response)


  else:
      response = jsonify({'code': 400, 'message': 'email already exists'})
      return make_response(response)

@users.route('/login', methods=['POST'])
def login():
  data = request.form
  if not data or not data.get('email') or not data.get('password'):
    response = jsonify({'code': 400, 'message': 'Both email and password are required'})
    
  user = User.query.filter_by(email=data.get('email')).first()
  if not user:
    response = jsonify({'code': 400, 'message': 'Wrong email, please try again...'})
  
  if check_password_hash(user.password, data.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8'), 'exp': datetime.utcnow() + timedelta(minutes=30)}), 201)
  return make_response(jsonify({'code': 400, 'message': 'Wrong password, please try again'}))
  
