from flask import Blueprint

sincronismo = Blueprint('sincronismo', __name__)

from . import views