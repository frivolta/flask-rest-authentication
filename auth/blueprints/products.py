from flask import Blueprint, render_template, request, redirect, url_for
from auth.models import Product
from auth.extensions import db
from auth.forms import ProductForm

products = Blueprint('products', __name__)


@products.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)


@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/details.html', product=product)


@products.route('/create', methods=['GET', 'POST'])
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                          description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.details', product_id=product.id))
    return render_template('products/create.html', form=form)


@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404
