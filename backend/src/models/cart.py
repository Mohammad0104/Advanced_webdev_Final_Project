from . import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subtotal = db.Column(db.Float)
    
    # items = db.relationship('CartItem', back_populates='cart')
    user = db.relationship('User', backref='cart')