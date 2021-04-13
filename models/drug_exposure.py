from db_init import db
from sqlalchemy import func

class DrugExposure(db.Model):
    __tablename__ = 'drug_exposure'

    drug_exposure_id = db.Column(db.BigInteger, primary_key=True)
    drug_concept_id = db.Column(db.BigInteger)
    person_id = db.Column(db.BigInteger)
    visit_occurrence_id = db.Column(db.Integer)
    drug_exposure_start_datetime = db.Column(db.DateTime())
    drug_exposure_end_datetime = db.Column(db.DateTime())


    def __init__(self, drug_concept_id, person_id, visit_occurrence_id, drug_exposure_start_datetime, drug_exposure_end_datetime):
        self.drug_concept_id = drug_concept_id
        self.person_idperson_id = person_id
        self.visit_occurrence_id = visit_occurrence_id
        self.drug_exposure_start_datetime = drug_exposure_start_datetime
        self.drug_exposure_end_datetime = drug_exposure_end_datetime


    @classmethod
    def drug_search(self, type, value, start, limit):
        # concept을 포함한 condition 데이터 반환
        if start is None:
            start = 0

        if limit is None:
            limit = 10

        query = "SELECT d.drug_concept_id, d.person_id, d.visit_occurrence_id, a.concept_name as drug_concept_name" \
            "     , d.drug_exposure_start_datetime, d.drug_exposure_end_datetime" \
            "    FROM drug_exposure d                                                                 " \
            "  INNER JOIN  concept a  ON d.drug_concept_id = a.concept_id                         "

        if type == "person_id":
            query += "  WHERE d.person_id ={}".format(value)
        elif type == "visit_occurrence_id":
            query += "  WHERE d.visit_occurrence_id ={}".format(value)
        elif type == "concpet_name":
            query += "  WHERE a.concept_name LIKE '%{}%'".format(value)

        query += " LIMIT {} OFFSET {}".format(limit, start)

        data = db.session.execute(query).fetchall()

        return data
