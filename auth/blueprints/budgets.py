from flask import Blueprint, render_template, request, redirect, url_for
from auth.models import Budget
from auth.extensions import db

budgets = Blueprint('budgets', __name__)

# Get budget by user id

# Edit budget