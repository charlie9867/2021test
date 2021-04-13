from db_init import db
from sqlalchemy import func

class ConditionOccurrence(db.Model):
    __tablename__ = 'condition_occurrence'

    condition_occurrence_id = db.Column(db.BigInteger, primary_key=True)
    condition_concept_id = db.Column(db.BigInteger)
    person_id = db.Column(db.BigInteger)
    visit_occurrence_id = db.Column(db.Integer)
    condition_start_datetime = db.Column(db.DateTime())
    condition_end_datetime = db.Column(db.DateTime())


    def __init__(self, condition_concept_id, person_id, visit_occurrence_id, condition_start_datetime, condition_end_datetime):
        self.condition_concept_id = condition_concept_id
        self.person_idperson_id = person_id
        self.visit_occurrence_id = visit_occurrence_id
        self.condition_start_datetime = condition_start_datetime
        self.condition_end_datetime = condition_end_datetime


    @classmethod
    def condition_search(self, type, value, start, limit):
        # concept을 포함한 condition 데이터 반환
        if start is None:
            start = 0

        if limit is None:
            limit = 10

        query = "SELECT c.condition_concept_id, c.person_id, c.visit_occurrence_id, a.concept_name as condition_concept_name" \
            "     , c.condition_start_datetime, c.condition_end_datetime" \
            "    FROM condition_occurrence c                                                                 " \
            "  INNER JOIN  concept a  ON c.condition_concept_id = a.concept_id                         "

        if type == "person_id":
            query += "  WHERE c.person_id ={}".format(value)
        elif type == "visit_occurrence_id":
            query += "  WHERE c.visit_occurrence_id ={}".format(value)
        elif type == "concpet_name":
            query += "  WHERE a.concept_name LIKE '%{}%'".format(value)

        query += " LIMIT {} OFFSET {}".format(limit, start)

        data = db.session.execute(query).fetchall()

        return data
