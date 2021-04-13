from flask_restful import Resource, reqparse
from flask import jsonify
from flasgger import swag_from

from models.visit_occurrence import VisitOccurrence

from flask_marshmallow import Marshmallow

ma = Marshmallow()

class VisitSearchSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('visit_occurrence_id', 'person_id', 'visit_concept_id', 'visit_concept_name', 'visit_start_datetime', 'visit_end_datetime')

visit_search_schema = VisitSearchSchema(many=True)

class VisitOccurrenceConcept(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('start',
        type=int,
        required=False
    )

    parser.add_argument('limit',
        type=int,
        required=False
    )
    @swag_from('docs\\visit_occurrence.yml')
    def get(self, type, value):

        param = VisitOccurrenceConcept.parser.parse_args()
        data = {}

        data['visit_concept'] = visit_search_schema.dump(VisitOccurrence.visit_search(type, value, param['start'], param['limit']))

        return jsonify(data)
