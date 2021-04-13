from flask_restful import Resource, reqparse
from flask import jsonify
from flasgger import swag_from

from models.drug_exposure import DrugExposure

from flask_marshmallow import Marshmallow

ma = Marshmallow()

class DurgSearchSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('visit_occurrence_id', 'person_id', 'drug_concept_id', 'drug_concept_name', 'visit_start_datetime', 'visit_end_datetime')

drug_search_schema = DurgSearchSchema(many=True)

class DrugExposureConcept(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('start',
        type=int,
        required=False
    )

    parser.add_argument('limit',
        type=int,
        required=False
    )

    @swag_from('docs\\drug_exposure.yml')
    def get(self, type, value):
        file: docs/drug_exposure.yml
        param = DrugExposureConcept.parser.parse_args()

        data = {}

        data['drug_concept'] = drug_search_schema.dump(DrugExposure.drug_search(type, value, param['start'], param['limit']))

        return jsonify(data)
