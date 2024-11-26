from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    profile_pic_url = db.Column(db.String(256), nullable=True)
    admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        """Password should never be accessed directly."""
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password):
        """Set the hashed password."""
        self.password_hash = generate_password_hash(raw_password)

    def verify_password(self, raw_password):
        """Verify if a raw password matches the stored hash."""
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        """Serialize the User model to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_pic_url": self.profile_pic_url,
            "admin": self.admin
        }
