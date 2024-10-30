from . import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subtotal_price = db.Column(db.Float)
    icon_urls = db.Column(db.String(500))
    
    user = db.relationship('User', backref='cart')