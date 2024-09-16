from flask import Blueprint, jsonify, request
from ..models.recipe_model import Recipe
from .. import db

recipes_blueprint = Blueprint('recipes', __name__)

@recipes_blueprint.route('/', methods=['GET'])
def get_recipe():
    recipies = Recipe.query.all()
    recipe_data = [{'id': user.id, 'name': recipe.username, 'description': recipe.description} for recipe in recipies]
    return jsonify(recipe_data), 200

@recipes_blueprint.route('/', methods=['POST'])
def create_recipe():
    data = request.get_json()
    new_recipe = Recipe(name=data['name'], description=data['description'])
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe created'}), 201
