from flask import Blueprint, jsonify, request, make_response
import datetime
from auth.models import Expense
from auth.extensions import db
from auth.helpers import token_required

expenses = Blueprint('expenses', __name__)


@expenses.route('/expenses', methods=['GET'])
@token_required
def get_expenses(current_user):
    if not request.form.get('expense_id'):
        all_expenses = Expense.query.filter_by(user_id=current_user.public_id)
        if all_expenses == None or all_expenses.count() == 0:
            return make_response(
                jsonify(errors=[dict(message="You have not expenses yet")])), 400

        all_expenses_response = [{"id": Expense.id}
                                 for Expense in all_expenses]
        return make_response(jsonify(all_expenses_response)), 200
    else:
        expense = Expense.query.filter_by(
            id=request.form.get('expense_id')).first()
        if expense == None:
            return make_response(
                jsonify(errors=[dict(message="Expense not found")])), 400
        if not expense.user_id == current_user.public_id:
            return make_response(
                jsonify(errors=[dict(message="Not authorized")])), 401
        return make_response(jsonify({"id": expense.id})), 200


@expenses.route('/expenses', methods=['POST'])
@token_required
def post_expense(current_user):
    data = request.form
    try:
        # expense_id=data.get('expense_id')
        expense = Expense(amount=data.get('amount'), expense_type=data.get('expense_type'), budget_type=data.get('budget_type'), description=data.get(
            'description'), user_id=current_user.public_id, date=datetime.date.fromisoformat((data.get('date'))),  category_id=data.get('category_id'))
        db.session.add(expense)
        db.session.commit()
        return make_response(jsonify({'id': expense.id}), 200)
    except AssertionError as err:
        response = jsonify({'code': 400, 'message': str(err)})
        return make_response(response)


@expenses.route('/expenses', methods=['DELETE'])
@token_required
def delete_expense(current_user):
    data = request.form
    expense_id = data.get('id')

    expense = Expense.query.filter_by(id=expense_id).first()
    if expense == None:
        return make_response(
            jsonify(errors=[dict(message="Expense not found")])), 400

    if not expense.user_id == current_user.public_id:
        return make_response(
            jsonify(errors=[dict(message="Not authorized")])), 401

    try:
        db.session.delete(expense)
        db.session.commit()
        return make_response(jsonify({'id': expense.id}), 200)
    except AssertionError as err:
        response = jsonify({'code': 400, 'message': str(err)})
        return make_response(response)
