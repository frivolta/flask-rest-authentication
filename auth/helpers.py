from flask import request, make_response,jsonify, current_app
import jwt
from datetime import datetime, timedelta
from functools import wraps
from auth.models import User

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
