from flask_restful import Resource, reqparse
from flask import jsonify
from flasgger import swag_from

from models.concept import ConceptTable

from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ConceptSearchSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('concept_id', 'concept_name', 'domain_id')

concept_search_schema = ConceptSearchSchema(many=True)

class Concept(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('start',
        type=int,
        required=False
    )

    parser.add_argument('limit',
        type=int,
        required=False
    )

    @swag_from('docs\\concept.yml')
    def get(self, concept_name):

        param = Concept.parser.parse_args()
        data = {}
        data["search_concept"] = concept_search_schema.dump(ConceptTable.search_concept(concept_name, param['start'], param['limit']))

        return jsonify(data)
