import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


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
    run_type = db.Column(db.String(50),
            nullable=False,
            unique=False,
            )

    def __repr__(self):
        """Show info about the user."""

        return "<user_id={} fname={} lname={} email={} zipcode={} run_type={} pace ={}>".format(
        self.human_id, self.fname, self.lname, self.email, self.zipcode, self.run_type, self.pace)

class Message(db.Model):
    """Message model."""

    __tablename__ = "messages"

    msg_id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True,
            )
    sender_id = db.Column(db.Integer, 
            db.ForeignKey('users.user_id'),
            )
    receiver_id = db.Column(db.Integer,
            db.ForeignKey('users.user_id'),
            )
    message = db.Column(db.String(1000),
            nullable=False,
            unique=False,
            )
    time_created = Column(DateTime(timezone=True),
            server_default=func.now(),
            )
    time_updated = Column(DateTime(timezone=True),
            onupdate=func.now(),
            )

    def __repr__(self):
        """Show info about the message."""

        return "<msg_id={} sender_id={} receiver_id={} time_created={} time_updated={}>".format(
        self.msg_id, self.senderd_id, self.receiver_id, self.time_created, self.time_updated)


#################################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///runbuddy_development'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
