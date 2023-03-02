from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }



class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250), nullable = False)
    height = db.Column(db.Integer, nullable = False)
    skin_color = db.Column(db.String(250), nullable = False)
    eyes_color = db.Column(db.String(250), nullable = False)
    birth_year = db.Column(db.String(250), nullable = False)

    def __repr__(self):
        return f'<Character {self.id}>'

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eyes_color": self.eyes_color,
            "birth_year": self.birth_year,
            
        }

class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    diameter = db.Column(db.Integer, nullable = False)
    gravity = db.Column(db.String(50), nullable = False)
    population = db.Column(db.Integer, nullable = False)
    terrain = db.Column(db.String(50), nullable = False)
    climate = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Planets {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            
        }
        


class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key = True)
    model = db.Column(db.String(50), nullable = False)
    manufacturer = db.Column(db.String(100), nullable = False)
    lenght = db.Column(db.Integer, nullable = False)
    cargo_capacity = db.Column(db.Integer, nullable = False)
    consumables = db.Column(db.String(100), nullable = False)
    max_atmosphering_speed = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<Starships {self.id}>'

    def serialize(self):
        return {
            "id":self.id,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "lenght": self.lenght,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            
        }


    
class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key = True)
    favorite_type = db.Column(db.String(50), nullable = False)
    element_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    def __repr__(self):
        return f'<Favorites {self.id}>'

    def serialize(self):

        #Esta parte me muestra la info de el elemento que se encuentre marcado como favorito

        if self.favorite_type == "character": 
            elements = Character.query.filter(Character.id == self.element_id).first()

        elif self.favorite_type == "planets": 
            elements = Planets.query.filter(Planets.id == self.element_id).first()
                
        elif self.favorite_type == "starships": 
            elements = Starships.query.filter(Starships.id == self.element_id).first()

     
        return {
            "id": self.id,
            "favorite_type": self.favorite_type,
            "user":self.user.email,
            "user_id":self.user.id,
            "element": elements.serialize()
        }