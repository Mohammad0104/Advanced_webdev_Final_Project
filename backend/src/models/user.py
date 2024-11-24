from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    successful_sales = db.Column(db.Integer, default=0, nullable=False)
    profile_pic_url = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    
    def to_dict(self):
        """Serialize the User object into a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'successful_sales': self.successful_sales,
            'profile_pic_url': self.profile_pic_url,
            'admin': self.admin
        }