
from sqlalchemy.orm import validates
from datetime import date
from auth.extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError("Needs to have a real name")
        return name

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))

    budget = db.relationship("Budget", uselist=False, back_populates='user')
    categories = db.relationship("Category", uselist=False, back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.body)
    

class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean,nullable=False, default=False)
    needs = db.Column(db.Integer,nullable=False, default=70)
    wants = db.Column(db.Integer,nullable=False, default=30)
    savings = db.Column(db.Integer,nullable=False, default=20)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))

    user = db.relationship("User", uselist=False)

    
    def __repr__(self):
        return '<Budget {}>'.format(self.body)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    expense_type = db.Column(db.String(32),nullable=False)
    budget_type = db.Column(db.String(32),nullable=False)
    value = db.Column(db.String(32),nullable=False)
    caption = db.Column(db.String(32),nullable=False)
    color = db.Column(db.String(32),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))

    user = db.relationship("User", uselist=False)
    
    def __repr__(self):
        return '<Category {}>'.format(self.body)

    @validates('expense_type')
    def validate_expense_type(self, key, expense_type):
        if not (expense_type == 'income' or expense_type == 'expense'):
            print("=====inside validate_expense_type=======")
            raise AssertionError("Not valid expense type: use 'income' or 'expense'")
        return expense_type

    @validates('budget_type')
    def validate_budget_type(self, key, budget_type):
        if not (budget_type == 'wants' or budget_type == 'needs' or budget_type == 'savings'):
            print("=====inside validates_budget_type=======")
            raise AssertionError("Not valid budget type: use 'savings' or 'wants' or 'needs'")
        return budget_type


class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(32),nullable=False)
    expense_type = db.Column(db.String(32),nullable=False)
    budget_type = db.Column(db.String(32),nullable=False)
    description = db.Column(db.String(120),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    date = db.Column(db.Date, nullable=False,default=date)
    
    user = db.relationship("User", uselist=False)
    category = db.relationship("Category", uselist=False)

    def __repr__(self):
        return '<Expense {}>'.format(self.body)