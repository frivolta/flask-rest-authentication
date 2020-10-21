from flask import Blueprint, render_template, request, redirect, url_for
from auth.models import User
from auth.extensions import db
from auth.forms import ProductForm

users = Blueprint('users', __name__)

