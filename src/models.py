from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True,default=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer(), unique=True, nullable=False)
    
    products =db.relationship('Product',lazy=True) #hijo
    

    def __repr__(self):
        return '<Category %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            # do not serialize the password, its a security breach
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer(), unique=True, nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey(Category.id)) #padre

    def __repr__(self):
        return '<Product %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            # do not serialize the password, its a security breach
        }