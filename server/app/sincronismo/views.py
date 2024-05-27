from . import sincronismo
from app import db, log
from ..tabelas import Usuarios, Imagens
from flask import jsonify

@sincronismo.route('/sincronismo/usuarios', methods=['GET'])
def sinc_usuarios():
    # retorna os usuarios em formato json para o cliente
    usuarios = Usuarios.query.all()
    usuarios_json = [{"id": u.id, "nome": u.nome, "ra": u.ra, "email": u.email, "senha": u.senha, "professor": u.professor} for u in usuarios]
    return jsonify(usuarios_json)

@sincronismo.route('/sincronismo/imagens')
def sincronizar_imagens():
    imagens = Imagens.query.all()
    imagens_json = [{"id": i.id, "id_usuario": i.id_usuario, "imagem": i.imagem} for i in imagens]
    return jsonify(imagens_json)