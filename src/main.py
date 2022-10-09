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
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/example'
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


@app.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters)

@app.route("/character/<int:id>", methods=['GET'])
def get_single_character(id):
    """
    Single person
    """
    single_character = Character.query.get(id)
    if not single_character: return jsonify({ "msg": "Character doesn't exist!"}), 404

    return jsonify(single_character.serialize()), 200

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets)

@app.route("/planet/<int:id>", methods=['GET'])
def get_single_planet(id):
    single_planet = Planet.query.get(id)
    if not single_planet: return jsonify({ "msg": "Planet doesn't exist!"}), 404
    return jsonify(single_planet)
############ adicionales ###################

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users)


@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_users(id):
    users = User.query.get(id)
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users)



@app.route("/favorite/planet/<int:planets_id>", methods=['POST'])
def store_fav_planet(planets_id):
    users_id =  request.json.get('users_id')
    favorite_planet = FavoritePlanet.query.get(planets_id)
    favorite_planet.users_id = users_id
    favorite_planet.save()

    return jsonify(favorite_planet.serialize()), 200
   
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=False)
