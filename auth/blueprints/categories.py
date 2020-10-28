from flask import Blueprint, jsonify, request
from auth.models import Category
from auth.extensions import db
from auth.helpers import token_required

categories = Blueprint('categories', __name__)


def define_new_budget_type(category):
    if category['budgetType'] == 'needs':
        return "wants"
    if category['budgetType'] == 'wants':
        return "needs"
    return "savings"


@categories.route('/category', methods=['PUT'])
@token_required
def get_budget(current_user):
    data = request.form
    # get category id from form
    # get opposite budget type
    # update
    # return new category
    pass
