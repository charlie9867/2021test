import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import configparser

from resources.person import Statistics, PersonConcept
from resources.concept import Concept
from resources.visit_occurrence import VisitOccurrenceConcept
from resources.condition_occurrence import ConditionOccurrenceConcept
from resources.drug_exposure import DrugExposureConcept

config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
swagger = Swagger(app, parse=True)

api.add_resource(Statistics, '/statistics')
api.add_resource(Concept, '/concept/<concept_name>')
api.add_resource(PersonConcept, '/person/<type>/<value>')
api.add_resource(VisitOccurrenceConcept, '/visit_occurrence/<type>/<value>')
api.add_resource(ConditionOccurrenceConcept, '/condition_occurrence/<type>/<value>')
api.add_resource(DrugExposureConcept, '/drug_exposure/<type>/<value>')

if __name__ == "__main__":
    from db_init import db
    db.init_app(app)
    app.run()
