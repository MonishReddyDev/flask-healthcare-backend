# where we define and register routes


from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return {'message': 'Healthcare API is running'}
