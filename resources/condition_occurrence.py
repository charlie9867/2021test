from flask_restful import Resource, reqparse
from flask import jsonify
from flasgger import swag_from

from models.condition_occurrence import ConditionOccurrence

from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ConditionSearchSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('person_id', 'condition_concept_id', 'condition_concept_name', 'condition_start_datetime', 'condition_end_datetime', 'visit_occurrence_id')

condition_search_schema = ConditionSearchSchema(many=True)

class ConditionOccurrenceConcept(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('start',
        type=int,
        required=False
    )

    parser.add_argument('limit',
        type=int,
        required=False
    )

    @swag_from('docs\\condition_occurrence.yml')
    def get(self, type, value):

        param = ConditionOccurrenceConcept.parser.parse_args()
        data = {}

        data['condition_concept'] = condition_search_schema.dump(ConditionOccurrence.condition_search(type, value, param['start'], param['limit']))

        return jsonify(data)
