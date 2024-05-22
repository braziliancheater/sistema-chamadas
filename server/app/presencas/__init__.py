from flask import Blueprint

presencas = Blueprint('presencas', __name__)

from . import views