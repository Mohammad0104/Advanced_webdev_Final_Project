from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    
    user = db.relationship('User', backref='orders')