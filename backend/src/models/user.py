from models import db


class User(db.Model):
    """Database model representing a user 

    Attributes:
        id (int): primary key for the user.
        name (str): user's name (full name).
        email (str): user's email.
        profile_pic_url (str): user's profile picture url.
        admin (bool): if the user is an admin or not
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_pic_url = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def to_dict(self) -> dict[str, any]:
        """Serialize user object into a dictionary

        Returns:
            dict: dict of the user object
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile_pic_url': self.profile_pic_url,
            'admin': self.admin,
        }


    def serialize(self):
        """Serialize the User object using to_dict.
        """
        return self.to_dict()
