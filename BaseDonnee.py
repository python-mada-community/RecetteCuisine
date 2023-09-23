from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Créez une instance de SQLAlchemy
# Créez une instance de base de données SQLAlchemy
Base = declarative_base()

# Définissez le modèle de base de données pour les recettes
class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    instructions = Column(Text, nullable=False)


# Créez une instance du moteur de base de données SQLite (vous pouvez utiliser un autre moteur de base de données si vous le souhaitez)
engine = create_engine('sqlite:///recipes.db')



# Créez une session SQLAlchemy pour interagir avec la base de données
Session = sessionmaker(bind=engine)

def CreerBaseDonne():
    # Créez les tables dans la base de données
    Base.metadata.create_all(engine)
    # Les données de recettes à ajouter
    recipes_data = [
        {"name": "Poulet rôti", "instructions": "Préchauffez le four à 180°C, enfournez le poulet pendant 1 heure."},
        {"name": "Pâtes à la carbonara",
         "instructions": "Faites cuire les pâtes, mélangez avec des œufs, du parmesan et du lard."},
        {"name": "Salade César",
         "instructions": "Mélangez de la laitue, du poulet grillé, des croûtons et de la sauce César."}
    ]
    session = Session()
    # Ajoutez les recettes à la base de données
    for recipe_data in recipes_data:
        recipe = Recipe(name=recipe_data['name'], instructions=recipe_data['instructions'])
        session.add(recipe)

    # Committez les changements pour les sauvegarder dans la base de données
    session.commit()
