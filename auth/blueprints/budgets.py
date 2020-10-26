from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from auth.models import Budget
from auth.extensions import db
from auth.helpers import token_required
from markupsafe import escape


budgets = Blueprint('budgets', __name__)

@budgets.route('/budgets', methods=['GET'])
@token_required
def get_budget(current_user):
  #Get budget from current_user.id
  try:
    budget = Budget.query.filter_by(user_id=current_user.id).first()
    return jsonify({'id':budget.id,'wants:': budget.wants,'needs':budget.needs,'savings': budget.savings}), 200
  except:
    return jsonify(errors=[dict(message="not found")]), 400

@budgets.route('/budgets', methods=['PUT'])
@token_required
def edit_budget(current_user):
  errors = []
  data = request.form
  needs = data.get('needs')
  savings = data.get('savings')
  wants = data.get('wants')
  
  # Validation
  if not needs or not savings or not wants:
    errors.append(dict({'message': 'Parameter/s missing (needs, savings, wants)'}))
  elif int(wants) + int(needs) + int(savings) > 100:
    errors.append(dict({'message': 'Sum of budgets must be below 100'}))
  
  if not errors:

    try:
      budget = Budget.query.filter_by(user_id=current_user.id).first()
      budget.wants = wants
      budget.savings = savings
      budget.needs = needs
      db.session.commit()
      return jsonify({'id':budget.id,'wants:': budget.wants,'needs':budget.needs,'savings': budget.savings}), 200
    except:
      return jsonify(errors=[dict(message="not found")]), 400

  else: 
    return jsonify(errors=errors), 400