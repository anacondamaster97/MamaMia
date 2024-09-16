from .. import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    recipe = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Recipe {self.name}>'
