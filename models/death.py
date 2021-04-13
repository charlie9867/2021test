from db_init import db
from sqlalchemy import func


class Death(db.Model):
    __tablename__ = 'death'

    person_id = db.Column(db.BigInteger, primary_key=True)
    death_date = db.Column(db.DateTime())

    def __init__(self, person_id, death_date):
        self.person_id = person_id
        self.death_date = death_date
