"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, jsonify
from api.models import db, User, Favorites, Character, Planets, Starships
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

# 4 funciones genericas para el crud : 1 para post, 1 para el get, otra el delete, y put 

# ALL USERS

@api.route('/users/', methods=['GET'])
def users():
    users = User.query.filter(User.__tablename__ == "user").all()
    all_users = []

    for i in range(len(users)):
        all_users.append(users[i].serialize())

    if len(all_users) > 0:
        return jsonify({
            "All users":all_users
        })
    
    return jsonify({
        "msg":"No have any user"
    })

# EACH USER

@api.route('/users/<int:user>/', methods=['GET'])
def each_user(user):
    user = User.query.filter(User.id == user).first()

    if not user is None:
        
        return jsonify({
            "user":user.serialize()
        }), 200

    return jsonify({
                "msg":"user not found"
            })


# POST NEW USER

@api.route('/users/', methods=['POST'])
def post_user():
    email = request.json.get("email")
    password = request.json.get("password")
    is_active = request.json.get("is_active")
    post_user = User(email = email, password = password, is_active = is_active)
    users = User.query.filter(User.email == email).first()


    if not users is None:
        return jsonify({
            "msg":"The user already exist"
        }), 404
        
    db.session.add(post_user)
    db.session.commit()

    return jsonify({
        "msg":"User create succefully"
    }), 201

# PUT USER

@api.route('/users/<int:user_id>/', methods=['PUT'])
def put_user(user_id):
    email = request.json.get("email") # traemos todos los campos a actualizar 
    password = request.json.get("password")
    is_active = request.json.get("is_active")
    user = User.query.filter(User.id == user_id).all() # traemos el usuario como lista, esto para poder hacer la comparativa en caso tal que no exista

    if len(user) == 0: # si no existe entonces imprimimos el msj
        return jsonify({
            "msg":"User not avaliable to update"
        }), 404

    # de lo contrario entonces se actualizan los datos
    new_user = user[0]
    new_user.email = email
    new_user.password = password
    new_user.is_active = is_active
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg":"User update successfully"
    }), 201


# DELETE ALL USERS

@api.route('/users/', methods=['DELETE'])
def delete_all_users():
    users = User.query.filter(User.__tablename__ == "user").all()

    if len(users) == 0:

        return jsonify({
            "msg":"Not have any users to delete"
        }), 404

    for i in range(len(users)):
        db.session.delete(users[i])
        db.session.commit()

    return jsonify({
        "msg":"all users has been deleted"
    }), 201

# DELETE USER

@api.route('/users/<int:user>/', methods=['DELETE'])
def delete_user(user):
    users = User.query.filter(User.id == user).first()
    if users is None: # Si No existen usuario entonces imprime el msj que no hay
        return jsonify({
            "msg":"Not have users to delete"
            }), 404

    db.session.delete(users) # Si se salta la condición porque si hay usuarios entonces hace el delete y el commit
    db.session.commit()
    
    return jsonify({
        "msg":"User delete successfully"  # e imprime el msj
    }), 201

# ALL FAVORITES

@api.route('/favorites/', methods=['GET'])
def favorites():
    favorites = Favorites.query.filter(Favorites.__tablename__ == "favorites").all()
    all_favorites = []

    for i in range(len(favorites)):
        all_favorites.append(favorites[i].serialize())
        
    if len(all_favorites) > 0:

        return jsonify({
            "All favorites":all_favorites
        }), 200

    return jsonify({
        "msg":"No have any favorite"
    })
    



# EACH FAVORITES IN USERS

@api.route('/favorites/<int:user_param>/', methods=['GET'])
def get_user_favorite(user_param): 
    favorites = Favorites.query.filter(Favorites.user_id == user_param).all()
    favorite_list = []

    if favorites is None:
        return jsonify({
            "msg":"No have any favorite"
        }), 404

    
    for i in range(len(favorites)):

        
        if favorites[i].favorite_type == 'character':
            favorites_character = Character.query.get(favorites[i].element_id)
            if favorites_character != None:
                favorites[i].serialize()["data"] = favorites_character.serialize()
        
        if favorites[i].favorite_type == 'planets':
            favorites_planet = Planets.query.get(favorites[i].element_id)
            if favorites_planet != None:
                favorites[i].serialize()["data"] = favorites_planet.serialize()

                    
        if favorites[i].favorite_type == 'starships':
            favorites_starships = Starships.query.get(favorites[i].element_id)
            if favorites_starships != None:
                favorites[i].serialize()["data"] = favorites_starships.serialize()

        
        favorite_list.append(favorites[i].serialize())

    return jsonify({
        "favorites":favorite_list
        }), 201

# POST NEW FAVORITE

@api.route('/favorites/', methods=['POST'])
def post_favorite():
    favorite_type = request.json.get("favorite_type")
    element_id = request.json.get("element_id")
    post_favorite = Favorites(favorite_type = favorite_type, element_id = element_id)
    favorites = Favorites.query.filter(Favorites.favorite_type == favorite_type and Favorites.element_id == element_id).first()

    if not favorites is None:
        return jsonify({
            "msg":"Favorite already exist"
        }), 404

    db.session.add(post_favorite)
    db.session.commit()

    return jsonify({
        "msg":"Favorite created successfully"
    })


# DELETE ALL FAVORITES

@api.route('/favorites/', methods=['DELETE'])
def delete_all_favorites():
    favorites = Favorites.query.filter(Favorites.__tablename__ == "favorites").all()

    if len(favorites) == 0:

        return jsonify({
            "msg":"Not have any favorites to delete"
        }), 404

    for i in range(len(favorites)):
        db.session.delete(favorites[i])
        db.session.commit()

    return jsonify({
        "msg":"all favorites has been deleted"
    }), 201


# DELETE FAVORITE

@api.route('/favorites/<int:favorite>/', methods=['DELETE'])
def delete_favorite(favorite):
    favorites = Favorites.query.filter(Favorites.id == favorite).first()
    if favorites is None:
        return jsonify({
            "msg":"Not have favorites to delete"
            }), 404

    db.session.delete(favorites)
    db.session.commit()
    
    return jsonify({
        "msg":"Favorite delete successfully" 
    }), 201



# ALL CHARACTER

@api.route('/character/')
def character():
    character = Character.query.filter(Character.__tablename__ == "character").all()
    all_character = []

    for i in range(len(character)):
        all_character.append(character[i].serialize())

    if len(all_character) > 0:
        return jsonify({
            "All character":all_character
        }), 200

    return jsonify({
        "msg":"No have any character"
    })


# EACH CHARACTER

@api.route('/character/<int:peop>/', methods=['GET'])
def each_character(char):
    character = Character.query.filter(Character.id == char).first()

    if not character is None:

        return jsonify({
                "character":character.serialize()
            }), 201

    return jsonify({
        "msg":"character not found"
    }), 404


# POST NEW CHARACTER

@api.route('/character/', methods=['POST'])
def post_character():
    name = request.json.get("name")
    gender = request.json.get("gender")
    height = request.json.get("height")
    skin_color = request.json.get("skin_color")
    eyes_color = request.json.get("eyes_color")
    birth_year = request.json.get("birth_year")
    post_character = Character(name = name, gender = gender, height = height, skin_color = skin_color, eyes_color = eyes_color, birth_year = birth_year)
    character = Character.query.filter(Character.name == name and Character.gender == gender and Character.height == height and Character.skin_color == skin_color and Character.eyes_color == eyes_color and Character.birth_year == birth_year).first()

    if not character is None:
        return jsonify({
            "msg":"Character already exist"
        }), 404

    db.session.add(post_character)
    db.session.commit()

    return jsonify({
        "msg":"Character created successfully"
    }), 201

# PUT CHARACTER

@api.route('/character/<int:character_id>/', methods=['PUT'])
def put_character(character_id):
    name = request.json.get("name")
    gender = request.json.get("gender")
    height = request.json.get("height")
    skin_color = request.json.get("skin_color")
    eyes_color = request.json.get("eyes_color")
    birth_year = request.json.get("birth_year")
    character = Character.query.filter(Character.id == character_id).all()

    if len(character) == 0:
        return jsonify({
            "msg":"Character not avaliable to update"
        }), 404

    new_character = character[0]
    new_character.name = name
    new_character.gender = gender
    new_character.height = height
    new_character.skin_color = skin_color
    new_character.eyes_color = eyes_color
    new_character.birth_year = birth_year

    db.session.add(new_character)
    db.session.commit()

    return jsonify({
        "success":"Character update successfully"
    }), 201

# DELETE ALL CHARACTER

@api.route('/character/', methods=['DELETE'])
def delete_all_character():
    character = Character.query.filter(Character.__tablename__ == "character").all()

    if len(character) == 0:

        return jsonify({
            "msg":"Not have any character to delete"
        }), 404

    for i in range(len(character)):
        db.session.delete(character[i])
        db.session.commit()

    return jsonify({
        "msg":"all character has been deleted"
    }), 201

# DELETE CHARACTER

@api.route('/character/<int:peop>/', methods=['DELETE'])
def delete_character(char):
    character = Character.query.filter(Character.id == char).first()

    if character is None:

        return jsonify({
            "msg":"Not have character to delete"
        }), 404
    
    db.session.delete(character)
    db.session.commit()

    return jsonify({
        "msg":"character delete successfully"
    }), 201

# ALL PLANETS

@api.route('/planets/', methods=['GET'])
def planets():
    planets = Planets.query.filter(Planets.__tablename__ == "planets").all()
    all_planets = []

    for i in range(len(planets)):
        all_planets.append(planets[i].serialize())

    if len(all_planets) > 0:
        return jsonify({
            "All planets":all_planets
        }), 200
    return jsonify({
        "msg":"Not have any planet"
    })

# EACH PLANET

@api.route('/planets/<int:planet>/', methods=['GET'])
def each_planet(planet):
    planets = Planets.query.filter(Planets.id == planet).first()

    if not planets is None:

        return jsonify({
            "planet":planets.serialize()
        }), 200
    
    return jsonify({
        "msg":"planet not found"
    })

# POST NEW PLANET

@api.route('/planets/', methods=['POST'])
def post_planet():
    name = request.json.get("name")
    diameter = request.json.get("diameter")
    gravity = request.json.get("gravity")
    population = request.json.get("population")
    terrain = request.json.get("terrain")
    climate = request.json.get("climate")
    post_planet = Planets(name = name, diameter = diameter, gravity = gravity, population = population, terrain = terrain, climate = climate)
    planets = Planets.query.filter(Planets.name == name and Planets.diameter == diameter and Planets.population == population and Planets.terrain == terrain and Planets.climate == climate).first()

    if not planets is None:
        return jsonify({
            "msg":"Planet already exist"
        }), 404

    db.session.add(post_planet)
    db.session.commit()

    return jsonify({
        "msg":"Planet created successfully"
    }), 201

# PUT PLANET

@api.route('/planets/<int:planet_id>/', methods=['PUT'])
def put_planet(planet_id):
    name = request.json.get("name")
    diameter = request.json.get("diameter")
    gravity = request.json.get("gravity")
    population = request.json.get("population")
    terrain = request.json.get("terrain")
    climate = request.json.get("climate")
    planets = Planets.query.filter(Planets.id == planet_id).all()

    if len(planets) == 0:
        return jsonify({
            "msg":"Planet not avaliable to update"
        }), 404

    new_planet = planets[0]
    new_planet.name = name
    new_planet.diameter = diameter
    new_planet.gravity = gravity
    new_planet.population = population
    new_planet.terrain = terrain
    new_planet.climate = climate

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({
        "success":"Planet update successfully"
    }), 201



# DELETE PLANET

@api.route('/planets/<int:planet>/', methods=['DELETE'])
def delete_planet(planet):
    planets = Planets.query.filter(Planets.id == planet).first()

    if planets is None:

        return jsonify({
            "msg":"Not have planet to delete"
        }), 404

    db.session.delete(planets)
    db.session.commit()
    
    return jsonify({
        "msg":"planet delete successfully"
    }), 201

# DELETE ALL PLANETS

@api.route('/planets/', methods=['DELETE'])
def delete_all_planets():
    planets = Planets.query.filter(Planets.__tablename__ == "planets").all()

    if len(planets) == 0:

        return jsonify({
            "msg":"Not have any planets to delete"
        }), 404

    for i in range(len(planets)):
        db.session.delete(planets[i])
        db.session.commit()

    return jsonify({
        "msg":"all planets has been deleted"
    }), 201



# ALL STARSHIPS

@api.route('/starships/')
def starships():
    starships = Starships.query.filter(Starships.__tablename__ == "starships").all()
    all_starships = []

    for i in range(len(starships)):
        all_starships.append(starships[i].serialize())
    
    if len(all_starships) > 0:
        return jsonify({
            "All starships":all_starships
        }), 200
    return jsonify({
        "msg":"No have any starship"
    })

# EACH STARSHIP

@api.route('/starships/<int:starship>/')
def each_starship(starship):
    starships = Starships.query.filter(Starships.id == starship).first()

    if not starships is None:

        return jsonify({
            "starship":starships.serialize()
        }), 200
    
    return jsonify({
        "msg":"starship not found"
    })

# POST NEW STARSHIP

@api.route('/starships/', methods=['POST'])
def post_starship():
    model = request.json.get("model")
    manufacturer = request.json.get("manufacturer")
    lenght = request.json.get("lenght")
    cargo_capacity = request.json.get("cargo_capacity")
    consumables = request.json.get("consumables")
    max_atmosphering_speed = request.json.get("max_atmosphering_speed")
    post_starship = Starships(model = model, manufacturer = manufacturer, lenght = lenght, cargo_capacity = cargo_capacity, consumables = consumables, max_atmosphering_speed = max_atmosphering_speed)
    starships = Starships.query.filter(Starships.model == model and Starships.manufacturer == manufacturer and Starships.lenght == lenght and Starships.cargo_capacity == cargo_capacity and Starships.consumables == consumables and Starships.max_atmosphering_speed == max_atmosphering_speed).first()

    if not starships is None:
        return jsonify({
            "msg":"Starship already exist"
        }), 404

    db.session.add(post_starship)
    db.session.commit()

    return jsonify({
        "msg":"Starship created successfully"
    })

# PUT STARSHIPS

@api.route('/starships/<int:starship_id>/', methods=['PUT'])
def put_starship(starship_id):
    model = request.json.get("model")
    manufacturer = request.json.get("manufacturer")
    lenght = request.json.get("lenght")
    cargo_capacity = request.json.get("cargo_capacity")
    consumables = request.json.get("consumables")
    max_atmosphering_speed = request.json.get("max_atmosphering_speed")
    starships = Starships.query.filter(Starships.id == starship_id).all()

    if len(starships) == 0:
        return jsonify({
            "msg":"Starship not avaliable to update"
        }), 404

    new_starship = starships[0]
    new_starship.model = model
    new_starship.manufacturer = manufacturer
    new_starship.lenght = lenght
    new_starship.cargo_capacity = cargo_capacity
    new_starship.consumables = consumables
    new_starship.max_atmosphering_speed = max_atmosphering_speed

    db.session.add(new_starship)
    db.session.commit()

    return jsonify({
        "success":"Starship update successfully"
    }), 201


# DELETE ALL STARSHIPS

@api.route('/starships/', methods=['DELETE'])
def delete_all_starships():
    starships = Starships.query.filter(Starships.__tablename__ == "starships").all()

    if len(starships) == 0:

        return jsonify({
            "msg":"Not have any starships to delete"
        }), 404

    for i in range(len(starships)):
        db.session.delete(starships[i])
        db.session.commit()

    return jsonify({
        "msg":"all starships has been deleted"
    }), 201

# DELETE STARSHIP

@api.route('/starships/<int:starship>/', methods=['DELETE'])
def delte_starship(starship):
    starships = Starships.query.filter(Starships.id == starship).first()

    if starships is None:

        return jsonify({
            "msg":"Not have starship to delete"
        }), 404

    db.session.delete(starships)
    db.session.commit()
    
    return jsonify({
        "msg":"starship delete successfully"
    }), 201