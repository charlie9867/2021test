from db_init import db
from sqlalchemy import func

from models.person import Person

class VisitOccurrence(db.Model):
    __tablename__ = 'visit_occurrence'

    visit_occurrence_id = db.Column(db.BigInteger, primary_key=True)
    person_id = db.Column(db.BigInteger)
    visit_concept_id = db.Column(db.Integer)
    visit_start_datetime = db.Column(db.DateTime())
    visit_end_datetime = db.Column(db.DateTime())


    def __init__(self, visit_occurrence_id, person_id, visit_concept_id, visit_start_datetime, visit_end_datetime):
        self.visit_occurrence_id = visit_occurrence_id
        self.person_idperson_id = person_id
        self.visit_concept_id = visit_concept_id
        self.visit_start_datetime = visit_start_datetime
        self.visit_end_datetime = visit_end_datetime


    @classmethod
    def concept_visit_statistics(self):
        # 방문 유형 별 방문 수
        data =  db.session.query(self.visit_concept_id, func.count(self.visit_concept_id).label('cnt')).group_by(self.visit_concept_id).all()
        return data

    @classmethod
    def gender_visit_statistics(self):
        # 성별 방문 수
        data =  db.session.query(Person.gender_concept_id, func.count(Person.gender_concept_id).label('cnt')).join(self, self.person_id==Person.person_id).group_by(Person.gender_concept_id).all()
        return data

    @classmethod
    def race_visit_statistics(self):
        # 인종별 방문 수
        data =  db.session.query(Person.race_concept_id, func.count(Person.race_concept_id).label('cnt')).join(self, self.person_id==Person.person_id).group_by(Person.race_concept_id).all()
        return data

    @classmethod
    def ethnicity_visit_statistics(self):
        # 민족 방문 수
        data =  db.session.query(Person.ethnicity_concept_id, func.count(Person.ethnicity_concept_id).label('cnt')).join(self, self.person_id==Person.person_id).group_by(Person.ethnicity_concept_id).all()
        return data

    @classmethod
    def age_visit_statistics(self):
        # 방문시 연령대(10세 단위)별 방문 수
        query = "SELECT (FLOOR(age / 10) * 10     ) ||  ' ~ ' || (FLOOR(age / 10) * 10 + 10)  AS age_av" \
            "     , COUNT(*) cnt                                                                       " \
            "  FROM (select EXTRACT(YEAR FROM age(cast(birth_datetime as DATE))) AS age from person ) a" \
            " GROUP BY FLOOR(age / 10)                                                                 " \

        data = db.session.execute(query).fetchall()
        return data

    @classmethod
    def visit_search(self, type, value, start, limit):
        # concept을 포함한 visit 데이터 반환
        if start is None:
            start = 0

        if limit is None:
            limit = 10

        query = "SELECT v.visit_occurrence_id, v.person_id, v.visit_concept_id,  a.concept_name as visit_concept_name" \
            "     , v.visit_start_datetime, v.visit_end_datetime" \
            "    FROM visit_occurrence v                                                                 " \
            "  INNER JOIN  concept a  ON v.visit_concept_id = a.concept_id                         "

        if type == "person_id":
            query += "  WHERE v.person_id ={}".format(value)
        elif type == "visit_occurrence_id":
            query += "  WHERE v.visit_occurrence_id ={}".format(value)
        elif type == "concpet_name":
            query += "  WHERE a.concept_name LIKE '%{}%'".format(value)

        query += " LIMIT {} OFFSET {}".format(limit, start)

        data = db.session.execute(query).fetchall()

        return data
