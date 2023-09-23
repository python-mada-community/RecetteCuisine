from flask import Flask, jsonify, request, render_template, Response

from BaseDonnee import CreerBaseDonne, Session, Recipe

app = Flask(__name__)

# Data base
# Liste de recettes (en mémoire, remplacez-la par une base de données en production)


# Fonction pour communiquer:
def tout_recette():
    session = Session()
    data = session.query(Recipe).all()
    session.close()
    return data


def prendre_recette(recipe_id):
    session = Session()
    data = session.query(Recipe).filter_by(id=recipe_id).first()
    session.close()
    return data


def creer_recette(recette):
    session = Session()
    session.add(recette)
    session.commit()
    session.close()


def supprimer_recette(recipe_id):
    session = Session()
    data = session.query(Recipe).filter_by(id=recipe_id).first()
    session.delete(data)
    session.commit()
    session.close()
# Endpoint
# Ajout du préfixe "api" à toutes les routes
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify(tout_recette())


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = prendre_recette(recipe_id)
    if recipe is None:
        return jsonify({"error": "Recette non trouvée"}), 404
    return jsonify(recipe)


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    if 'name' not in data or 'instructions' not in data:
        return jsonify({"error": "Le nom et les instructions de la recette sont nécessaires"}), 400

    new_recipe = Recipe(
        name=data['name'],
        instructions=data['instructions']
    )
    creer_recette(new_recipe)
    return Response(status=201)


@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    session = Session()
    # Recherchez la recette dans la base de données par son ID
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()

    if recipe is None:
        return jsonify({"error": "Recette non trouvée"}), 404

    # Mettez à jour les propriétés de la recette en fonction des données reçues
    if 'name' in data:
        recipe.name = data['name']
    if 'instructions' in data:
        recipe.instructions = data['instructions']

    # Committez les modifications dans la base de données
    session.commit()

    # Convertissez la recette mise à jour en un dictionnaire JSON
    updated_recipe = {
        "id": recipe.id,
        "name": recipe.name,
        "instructions": recipe.instructions
    }

    return jsonify(updated_recipe)


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    supprimer_recette(recipe_id)
    return jsonify({"message": "Recette supprimée"})

# Endpoint pour les pages
@app.route("/")
def hello_world():
    return render_template("index.html", recipes=tout_recette())


@app.route("/recipe/<int:recipe_id>")
def page_recipe(recipe_id):
    return render_template("recette.html", recipe=prendre_recette(recipe_id))


@app.route("/recipe/new")
def new_recipe():
    return render_template("formulaire-recette.html")

if __name__ == "__main__":
    # CreerBaseDonne()

    app.run()
