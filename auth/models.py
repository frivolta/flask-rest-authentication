from sqlalchemy.orm import validates
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

"""" Improve Verification """
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))

    budget = db.relationship("Budget", uselist=False, back_populates='user')
    
    def __repr__(self):
        return '<User {}>'.format(self.body)
    

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    needs = db.Column(db.Integer,nullable=False, default=70)
    wants = db.Column(db.Integer,nullable=False, default=30)
    savings = db.Column(db.Integer,nullable=False, default=20)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", uselist=False, back_populates="budget")

    
    def __repr__(self):
        return '<Budget {}>'.format(self.body)


