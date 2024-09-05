#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)



# Root -  Flask API on localhost:5555
@app.route("/")
def index():
    return "<h1>Code challenge</h1>"



# GET /restaurants
# Need to add; "error": "Restaurant not found"
@app.route("/restaurants")
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name,
        }
        restaurants.append(restaurant_dict)
    
    response = make_response(
        restaurants,
        200,
        {"Content-Type": "application/json"}
    )

    return response



# GET /restaurants/int:id
# DELETE /restaurants/int:id
@app.route("/restaurants/<int:id>", methods=("GET", "DELETE"))
def restaurant_by_id(id):

    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    
    if request.method == "GET":

        if (not restaurant):
            response_dict = {
                "error": 'Restaurant not found'
            }
            response = make_response(
                response_dict,
                404)
            return response

        restaurant_dict = restaurant.to_dict()

        response = make_response(
            restaurant_dict,
            200
        )
        
        return response

    
    elif request.method == "DELETE":

        db.session.delete(restaurant)
        db.session.commit()

        return jsonify({}, 204)



# GET /pizzas
@app.route("/pizzas")
def pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict = {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name,
        }
        pizzas.append(pizza_dict)
    
    response = make_response(
        pizzas,
        200,
        {"Content-Type": "application/json"}
    )

    return response



# POST /restaurant_pizzas
# Need to add; "error": "validation errors"
@app.route("/restaurant_pizzas", methods=["POST"])
def restaurant_pizzas():

    q = request.get_json()

    restpizz = RestaurantPizza(price=q.get("price"), pizza_id=q.get("pizza_id"), restaurant_id=q.get("restaurant_id"))

    db.session.add(restpizz)
    db.session.commit()

    return jsonify({"message": "Restaurant pizza successfully added."}), 201



if __name__ == "__main__":
    app.run(port=5555, debug=True)
