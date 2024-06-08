from flask import render_template

from . import index
from ..tabelas import Usuarios, Presencas

@index.route('/')
def index():
    return render_template('index/index.html')