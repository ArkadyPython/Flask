import pydantic
from flask import Flask, jsonify
from flask import request
from flask.views import MethodView
from models import Advertisement, Session
from sqlalchemy.exc import IntegrityError
from schema import CreateAdvertisement

app = Flask("app")

def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise HttpError(400, error)


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response


def get_advertisement_by_id(advertisement_id: int):
    advertisement = request.session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError(status_code=404, description="advertisement not found")
    return advertisement

def add_advertisement(advertisement: Advertisement):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(status_code=409, description="advertisement already exist")
    return advertisement


class AdvertisementView(MethodView):
    def get(self, advertisement_id: int):
        advertisement = get_advertisement_by_id(advertisement_id)
        return jsonify(advertisement.json)

    def post(self):
        json_data = validate(CreateAdvertisement, request.json)
        advertisement = Advertisement(**json_data)
        add_advertisement(advertisement)
        response = jsonify(advertisement.json)
        response.status_code = 201
        return response

    def delete(self, advertisement_id: int):
        advertisement = get_advertisement_by_id(advertisement_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({"status": "success"})

advertisement_view = AdvertisementView.as_view("advertisement_view")

app.add_url_rule(rule="/advertisement", view_func=advertisement_view, methods=['POST'])
app.add_url_rule(rule="/advertisement/<int:advertisement_id>", view_func=advertisement_view,
                 methods=['GET', 'DELETE'])

app.run()