# models/user.py
from models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_pic_url = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        """Serialize the User object into a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile_pic_url': self.profile_pic_url,
            'admin': self.admin
        }

    # Ensure that serialize method is added
    def serialize(self):
        return self.to_dict()
