from flask import render_template
from random import randint

from . import index

def viadagem():
    lista_palavras = ["hello world!", "olá mundo!"]
    return lista_palavras[randint(0, len(lista_palavras)-1)]

@index.route('/')
def index():
    return render_template('index/index.html', title=viadagem())