from db_init import db
from sqlalchemy import func
from sqlalchemy.orm import aliased


from models.death import Death
from models.concept import ConceptTable

class Person(db.Model):
    __tablename__ = 'person'

    person_id = db.Column(db.BigInteger, primary_key=True)
    gender_concept_id = db.Column(db.Integer)
    birth_datetime = db.Column(db.DateTime())
    race_concept_id = db.Column(db.Integer)
    ethnicity_concept_id = db.Column(db.Integer)

    def __init__(self, person_id, gender_concept_id, birth_datetime, race_concept_id, ethnicity_concept_id):
        self.person_id = person_id
        self.gender_concept_id = gender_concept_id
        self.birth_datetime = birth_datetime
        self.race_concept_id = race_concept_id
        self.ethnicity_concept_id = ethnicity_concept_id


    @classmethod
    def person_statistics(self):
        # 전체 환자 수
        data =  db.session.query(self).count()
        return data

    @classmethod
    def gender_person_statistics(self):
        # 성별 환자 수
        data =  db.session.query(self.gender_concept_id, func.count(self.gender_concept_id).label('cnt')).group_by(self.gender_concept_id).all()
        return data

    @classmethod
    def race_person_statistics(self):
        # 인종별 환자 수
        data =  db.session.query(self.race_concept_id, func.count(self.race_concept_id).label('cnt')).group_by(self.race_concept_id).all()
        return data

    @classmethod
    def ethnicity_person_statistics(self):
        # 민족 환자 수
        data =  db.session.query(self.ethnicity_concept_id, func.count(self.ethnicity_concept_id).label('cnt')).group_by(self.ethnicity_concept_id).all()
        return data

    @classmethod
    def death_person_statistics(self):
        # 사망 환자 수
        data =  db.session.query(self).join(Death, self.person_id==Death.person_id).count()
        return data

    @classmethod
    def search_person(self, type, value, start, limit):
        # concept을 포함한 person 데이터 반환
        if start is None:
            start = 0

        if limit is None:
            limit = 10

        query = "SELECT p.person_id, p.gender_concept_id, a.concept_name as gender_concept_name, p.birth_datetime" \
            "     , p.race_concept_id, b.concept_name as race_concept_name, p.ethnicity_concept_id, c.concept_name as ethnicity_concept_name" \
            "    FROM person p                                                                    " \
            "  INNER JOIN  concept a  ON p.gender_concept_id = a.concept_id                         " \
            "  INNER JOIN  concept b  ON p.race_concept_id = b.concept_id                         " \
            "  INNER JOIN  concept c  ON p.ethnicity_concept_id = c.concept_id "

        if type == "person_id":
            query += "  WHERE p.person_id ={}".format(value)
        elif type == "concpet_name":
            query += "  WHERE a.concept_name LIKE '%{}%' OR b.concept_name LIKE '%{}%' OR c.concept_name LIKE '%{}%'".format(value, value, value)

        query += " LIMIT {} OFFSET {}".format(limit, start)


        data = db.session.execute(query).fetchall()

        return data
