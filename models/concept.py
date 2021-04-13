from db_init import db
from sqlalchemy import func



class ConceptTable(db.Model):
    __tablename__ = 'concept'

    concept_id = db.Column(db.Integer, primary_key=True)
    concept_name = db.Column(db.String(255))
    domain_id = db.Column(db.String(20))

    def __init__(self, concept_id, concept_name, domain_id):
        self.concept_id = concept_id
        self.concept_name = concept_name
        self.domain_id = domain_id


    @classmethod
    def search_concept(self, concept_name, start, limit):
        # concept_id 반환
        if start is None:
            start = 0

        if limit is None:
            limit = 10
        data =  db.session.query(self).filter(self.concept_name.ilike(f'%{concept_name}%'))[start:limit+start]

        return data
