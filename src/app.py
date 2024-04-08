"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()

    response_body = [user.serialize() for user in users]

    return jsonify(response_body), 200


@app.route('/personaje', methods=['GET'])
def get_personajes():
  
    personajes = Personaje.query.all()

    # Serializar los personajes y crear una lista de diccionarios
    serialized_personajes = [personaje.serialize() for personaje in personajes]

    # Devolver la lista de personajes como una respuesta JSON
    return jsonify(serialized_personajes), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_Onepersonaje(people_id):

    personaje = Personaje.query.get(people_id)
    
    if personaje: 
        serialized_personaje = personaje.serialize()
        return jsonify(serialized_personaje), 200
    else:
        return jsonify({'message': 'Personaje no encontrado'}), 404


@app.route('/planets', methods =['GET'])
def get_planeta():
    planets = Planeta.query.all()

    response_body = [planet.serialize() for planet in planets]

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_Oneplaneta(planet_id):

    planeta = Planeta.query.get(planet_id)
    
    if planeta: 
        serialized_planeta = planeta.serialize()
        return jsonify(serialized_planeta), 200
    else:
        return jsonify({'message': 'Planeta no encontrado'}), 404
    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
