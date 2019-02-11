from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.dialects import postgresql
db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = "users"


    user_id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True,
            )
    fname = db.Column(db.String(50), 
            nullable=False, 
            unique=False,
            )
    lname = db.Column(db.String(50),
            nullable=True,
            unique=False,
            )
    email = db.Column(db.String(250),
            nullable=False,
            unique=True,
            )
    password = db.Column(db.String(50),
            nullable=False,
            unique=False,
            )
    street_address = db.Column(db.String(250),
            nullable=False,
            unique=False,
            )
    city = db.Column(db.String(250),
            nullable=False,
            unique=False,
            )
    state = db.Column(db.String(2),
            nullable=False,
            unique=False,
            )
    zipcode = db.Column(db.Integer,
            nullable=False,
            unique=False,
            )
    pace = db.Column(db.Float,
            nullable=False,
            unique=False,
            )
    run_type = db.Column(postgresql.ENUM('road', 'trail', 'both'),
            nullable=False,
            unique=False,
            )
