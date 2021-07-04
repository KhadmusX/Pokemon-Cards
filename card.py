import sqlalchemy
from sqlalchemy.sql.elements import Null
from helpers import object_to_dict
from flask import Blueprint, request, abort, jsonify
from db import Base, Session
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime

session = Session()
session.expire_on_commit = False

public = Blueprint("public", __name__)

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    hp = Column(Integer)
    first_edition = Column(Boolean)
    expansion = Column(String(100))
    card_type = Column(String(50))
    rarity = Column(String(50))
    price = Column(Float)
    image_url = Column(String(500))
    creation_date = Column(DateTime)
    enabled = Column(Boolean, default=True)

    def __init__(self, name, hp, first_edition, expansion, card_type, rarity, price, image_url, creation_date):
        self.name = name
        self.hp = hp
        self.first_edition = first_edition
        self.expansion = expansion
        self.card_type = card_type
        self.rarity = rarity
        self.price = price
        self.image_url = image_url
        self.creation_date = creation_date
    
    def update(self, json_body):
        if json_body["hp"] % 10 != 0:
            raise Exception("Hp is not multiple of 10")
        self.name = json_body["name"]
        self.hp = json_body["hp"]
        self.first_edition = json_body["first_edition"]
        self.expansion = json_body["expansion"]
        self.card_type = json_body["card_type"]
        self.rarity = json_body["rarity"]
        self.price = json_body["price"]
        self.image_url = json_body["image_url"]
        self.creation_date = json_body["creation_date"]

    def create(json_body):
        if json_body["hp"] % 10 != 0:
            raise Exception("Hp is not multiple of 10")
        return Card(
            json_body["name"],
            json_body["hp"],
            json_body["first_edition"],
            json_body["expansion"],
            json_body["card_type"],
            json_body["rarity"],
            json_body["price"],
            json_body["image_url"],
            json_body["creation_date"]
        )

        

@public.route("/cards", methods=['GET'])
def get_cards():
    page = request.args.get('page', 1, type = int)
    entries_per_page = request.args.get('entries', 10, type = int)
    price_floor = request.args.get('price_floor', 0, type = float)
    price_limit = request.args.get('price_limit', 999999, type = float)

    dictionary_cards = object_to_dict(session.query(Card).filter(Card.enabled == True, Card.price >= price_floor, Card.price <= price_limit).limit(entries_per_page).offset((page - 1) * entries_per_page).all())

    return jsonify(dictionary_cards)


@public.route("/card/<int:card_id>", methods=["GET","PUT", "DELETE"])
def get_card(card_id):
    if request.method == "GET":
        card = session.query(Card).filter(Card.id == card_id,Card.enabled == True).first()
        if card == None:
            abort(404)
        dictionary_card = object_to_dict(card)
        return jsonify(dictionary_card)

    elif request.method == "PUT":
        #dictionary_card = object_to_dict(session.query(Card).filter(Card.id == card_id).first())
        card = session.query(Card).filter(Card.id == card_id).first()
        json_body = request.get_json()
        if card == None:
            abort(404)

        try:
            card.update(json_body)
            session.commit()
            dictionary_card = object_to_dict(card)
            return jsonify(dictionary_card)
        except:
            abort(400)

    elif request.method == "DELETE":
        card = session.query(Card).filter(Card.id == card_id).first()
        if card == None:
            abort(404)
        card.enabled = False
        session.commit()
        return "Card Deleted", 200

@public.route("/card", methods=["POST"])
def post_card():
    if request.method == "POST":
        json_body = request.get_json()

        try:
            card = Card.create(json_body)
            session.add(card)
            session.commit()
            dictionary_card = object_to_dict(card)
            return jsonify(dictionary_card)
        except:
            abort(400)
