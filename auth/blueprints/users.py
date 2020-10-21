from flask import Blueprint, request, make_response,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import User
from auth.extensions import db
from auth.forms import ProductForm
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps

users = Blueprint('users', __name__)

@users.route('/signup', methods=['POST'])
def signup():
  data = request.args
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
