from flask_restful import Resource, reqparse
from flask import jsonify
from flasgger import swag_from

from models.person import Person
from models.visit_occurrence import VisitOccurrence

from flask_marshmallow import Marshmallow

ma = Marshmallow()


class Statistics(Resource):
    @swag_from('docs\\person.yml')
    def get(self):
        # 통계 데이터
        data = {}
        person = {}
        visit = {}

        person["person_statistics"] = Person.person_statistics()

        person["gender_person_statistics"] = []
        for i in Person.gender_person_statistics() :
            person["gender_person_statistics"].append(i._asdict())

        person["race_person_statistics"] = []
        for i in Person.race_person_statistics() :
            person["race_person_statistics"].append(i._asdict())

        person["ethnicity_person_statistics"] = []
        for i in Person.ethnicity_person_statistics() :
            person["ethnicity_person_statistics"].append(i._asdict())

        person["death_person_statistics"] = Person.death_person_statistics()

        data["pserson"] = person

        visit["concept_visit_statistics"] = []
        for i in VisitOccurrence.concept_visit_statistics() :
            visit["concept_visit_statistics"].append(i._asdict())

        visit["gender_visit_statistics"] = []
        for i in VisitOccurrence.gender_visit_statistics() :
            visit["gender_visit_statistics"].append(i._asdict())

        visit["race_visit_statistics"] = []
        for i in VisitOccurrence.race_visit_statistics() :
            visit["race_visit_statistics"].append(i._asdict())

        visit["ethnicity_visit_statistics"] = []
        for i in VisitOccurrence.ethnicity_visit_statistics() :
            visit["ethnicity_visit_statistics"].append(i._asdict())

        visit["age_visit_statistics"] = []
        for i in VisitOccurrence.age_visit_statistics() :
            visit["age_visit_statistics"].append(i._asdict())

        data['visit'] = visit

        return jsonify(data)

class PersonSearchSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('person_id', 'gender_concept_id', 'birth_datetime', 'race_concept_id', 'ethnicity_concept_id', 'gender_concept_name', 'race_concept_name', 'ethnicity_concept_name')

person_search_schema = PersonSearchSchema(many=True)

class PersonConcept(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('start',
        type=int,
        required=False
    )

    parser.add_argument('limit',
        type=int,
        required=False
    )

    @swag_from('docs\\person_search.yml')
    def get(self, type, value):

        param = PersonConcept.parser.parse_args()
        data = {}

        data['person_concept'] = person_search_schema.dump(Person.search_person(type, value, param['start'], param['limit']))
        return jsonify(data)
