from flask import render_template, Response
from . import sincronismo
from app import db, log
from ..tabelas import Usuarios, Imagens, Propriedades
import requests

@sincronismo.route('/sincronismo/usuarios')
def sinc_usuarios():
    # faz o sincronismo de usuarios
    usuarios = request.get('http://localhost:5000/usuarios')

@sincronismo.route('/sincronismo/forcar/usuarios')
def sinc_usuarios_forc():
    # forca o sincronismo de usuarios
    pass

@sincronismo.route('/sincronismo/forcar/imagens')
def sinc_imagens_forc():
    # forca o sincronismo de imagens
    pass