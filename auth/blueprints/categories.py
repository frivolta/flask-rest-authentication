from flask import Blueprint, jsonify, request, make_response
from auth.models import Category
from auth.extensions import db
from auth.helpers import token_required

categories = Blueprint('categories', __name__)


def define_new_budget_type(category):
    if category.budget_type == 'needs':
        return "wants"
    if category.budget_type == 'wants':
        return "needs"
    return "savings"


@categories.route('/category', methods=['PUT'])
@token_required
def update_category(current_user):
    data = request.form
    category_id = data.get('id')
    category = Category.query.filter_by(id=category_id).first()

    if category == None:
        return make_response(
            jsonify(errors=[dict(message="Category not found")])), 400
    if not category.user_id == current_user.public_id:
        return make_response(
            jsonify(errors=[dict(message="User not authorized")])), 401

    updated_category_budget_type = define_new_budget_type(category)
    category.budget_type = updated_category_budget_type
    db.session.commit()

    return make_response(jsonify({"id": category.id, "category_id": category.category_id, "expense_type": category.expense_type, "budget_type": category.budget_type, "value": category.value, "caption": category.caption, "color": category.color}))


@categories.route('/category', methods=['GET'])
@token_required
def get_categories(current_user):
    categories = Category.query.filter_by(user_id=current_user.public_id)

    if categories == None:
        return make_response(
            jsonify(errors=[dict(message="Categories not found")])), 400

    all_categories = [{"id": Category.id, "category_id": Category.category_id, "expense_type": Category.expense_type,
                       "budget_type": Category.budget_type, "value": Category.value, "caption": Category.caption, "color": Category.color} for Category in categories]

    return make_response(jsonify(all_categories))
