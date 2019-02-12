from faker import Faker
from model import User
fake = Faker()

class TestUser(db.Model):
    def setUp(self):
        self.fake = Faker()
        self.user = User(
            fname = self.fake.first_name(),
            lname = self.fake.last_name(),
            email = self.fake.email(),
            address = self.fake.address(),
            )
