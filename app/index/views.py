from . import index
from .. import db

@index.route('/')
def index():
    return "<b>hello world</b>"