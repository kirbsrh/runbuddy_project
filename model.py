import datetime
import geocoder
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from faker import Faker
#myGenerator = Faker()
#myGenerator.random.seed(5467)

db = SQLAlchemy()


class User(db.Model):

    """User model."""

    __tablename__ = "users"


    user_id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True,
            )
    name = db.Column(db.String(200), 
            nullable=False, 
            unique=True,
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
    state = db.Column(db.String(100),
            nullable=False,
            unique=False,
            )
    zipcode = db.Column(db.Integer,
            nullable=False,
            unique=False,
            )
    # address = db.Column(db.String(300),
    #         nullable=False,
    #         unique=True,
    #         )
    # #lat = db.Column(db.Float, 
    #         nullable=True,
    #         unique=False,
    #         )
    # lng = db.Column(db.Float,
    #         nullable=True,
    #         unique=False,
    #         )
    pace = db.Column(db.String,
            nullable=True,
            unique=False,
            )
    run_type = db.Column(db.String(50),
            nullable=True,
            unique=False,
            )

    def __repr__(self):
        """Show info about the user."""

        return "<user_id={} name={} email={} zipcode={}".format(
        self.user_id, self.name, self.email, self.zipcode)



    @classmethod
    def seed(cls, fake):
        """function to seed the database with fake users"""

        #create list of real addresses from addresses scraped and stored
        #move addresses from text file into list

        address_list = []

        address_file = open('test_data.txt')

        for line in address_file:
            address_list.append(line)

        print(address_list)
        address_file.close()
        return address_list


        #list of paces to randomly assign to fake users

        pace_list = ["6:00", "6:15", "6:30", "6:45",
         "7:00", "7:15", "7:30", "7:45", "8:00", 
         "8:15", "8:30", "8:45", "9:00", "9:15", "9:30", "9:45", "10:00",
        "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00"]

        # list of run types to randomly assign to fake users

        run_type_list = ["road", "trail", "both"]

        #lat = 

        user = cls(
            name = fake.name(),
            email = fake.email(),
            password = fake.password(),
            street_address = fake.street_address(),
            city = fake.city(),
            state = fake.state(),
            zipcode = fake.zipcode(),
            #address = random.choice(address_list),
            pace = random.choice(pace_list),
            run_type = random.choice(run_type_list),
        )
        user.save()


    def save(self):
        db.session.add(self)
        db.session.commit()    

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
    sender = db.relationship('User',
            foreign_keys = 'Message.sender_id',
            backref = ('sender_messages') 
            )
    receiver = db.relationship('User',
            foreign_keys = 'Message.receiver_id',
            backref = db.backref('receiver_messages'))

    def __repr__(self):
        """Show info about the message."""

        return "<msg_id={} sender_id={} receiver_id={}>".format(
        self.msg_id, self.sender_id, self.receiver_id)


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
