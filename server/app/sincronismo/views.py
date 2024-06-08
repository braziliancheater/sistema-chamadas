from . import sincronismo
from app import db, log
from ..tabelas import Usuarios, Imagens, Presencas
from flask import jsonify, request

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

@sincronismo.route('/sincronismo/presencas', methods=['POST'])
def sincronizar_presencas():
    presencas = request.json
    if not presencas:
        log.log_erro(__name__, "Nenhuma presença recebida.")
        return jsonify("Nenhuma presença recebida."), 400

    try:
        for presenca in presencas:
            try:
                usuario = Usuarios.query.filter_by(nome=presenca['nome']).first()
                if usuario is None:
                    log.log_erro(__name__, f"Usuário não encontrado: {presenca['nome']}")
                    continue

                data = presenca['data']
                hora = presenca['hora']
                nova_presenca = Presencas(id_usuario=usuario.id, data=data, hora=hora)
                db.session.add(nova_presenca)
                log.log_sucesso(__name__, f"Presença adicionada para {presenca['nome']} em {data} às {hora}")
            except Exception as e:
                log.log_erro(__name__, f"Erro ao registrar presença para {presenca['nome']}: {str(e)}")

        db.session.commit()
        log.log_sucesso(__name__, "Todas as presenças foram registradas no banco de dados.")
        return jsonify("Presenças registradas no banco de dados."), 200
    except Exception as e:
        db.session.rollback()
        log.log_erro(__name__, f"Erro ao registrar presenças: {str(e)}")
        return jsonify(f"Erro ao registrar presenças: {str(e)}"), 500