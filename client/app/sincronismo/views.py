from . import sincronismo
from app import db, log
from ..tabelas import Usuarios, Imagens
import requests
from ..index import views

@sincronismo.route('/sincronismo/usuarios')
def sincronizar_usuarios():
    # faz o sincronismo de usuarios
    log.log_sucesso(__name__, "iniciando sincronismo de usuários")
    response = requests.get('http://localhost:5000/sincronismo/usuarios')
    if response.status_code == 200:
        log.log_sucesso(__name__, "sincronizando usuários...")
        usuarios = response.json()
        for user_data in usuarios:
            usuario = Usuarios.query.filter_by(id=user_data['id']).first()
            if usuario:
                # Atualiza usuário existente
                log.log_sucesso(__name__, f"atualizando usuário {usuario.nome}")
                usuario.nome = user_data['nome']
                usuario.ra = user_data['ra']
                usuario.email = user_data['email']
                usuario.senha = user_data['senha']
                usuario.professor = user_data['professor']
            else:
                # Adiciona novo usuário
                log.log_sucesso(__name__, f"adicionando usuário {user_data['nome']}")
                novo_usuario = Usuarios(
                    id=user_data['id'],
                    nome=user_data['nome'],
                    ra=user_data['ra'],
                    email=user_data['email'],
                    senha=user_data['senha'],
                    professor=user_data['professor']
                )
                db.session.add(novo_usuario)
        db.session.commit()
    
        # sincroniza as imagens
        sincronizar_imagens()

        # sincroniza as faces
        log.log_aviso(__name__, "iniciando sincronização de faces")
        try:
            views.init_known_faces()
            log.log_sucesso(__name__, "sincronização de faces concluída com sucesso.")
        except Exception as e:
            log.log_erro(__name__, f"erro ao sincronizar faces: {e}")

        return "Sincronização de usuários e imagens concluída com sucesso.", 200
    else:
        return "Erro ao sincronizar usuários.", 500

@sincronismo.route('/sincronismo/imagens')
def sincronizar_imagens():
    log.log_sucesso(__name__, "iniciando sincronismo de imagens")
    response = requests.get('http://localhost:5000/sincronismo/imagens')
    if response.status_code == 200:
        log.log_sucesso(__name__, "sincronizando imagens...")
        imagens = response.json()
        for imagem_data in imagens:
            imagem = Imagens.query.filter_by(id=imagem_data['id']).first()
            if not imagem:
                log.log_sucesso(__name__, f"adicionando imagem {imagem_data['id']}")
                novo_imagem = Imagens(
                    id=imagem_data['id'],
                    id_usuario=imagem_data['id_usuario'],
                    imagem=imagem_data['imagem']
                )
                db.session.add(novo_imagem)
        db.session.commit()

@sincronismo.route('/sincronismo/forcar/usuarios', methods=['GET'])
def sinc_usuarios_forc():
    # forca o sincronismo de usuarios
    sincronizar_usuarios()
    return "sincronização de usuários concluída com sucesso.", 200

@sincronismo.route('/sincronismo/forcar/imagens')
def sinc_imagens_forc():
    # forca o sincronismo de imagens
    sincronizar_imagens()
    return "sincronização de imagens concluída com sucesso.", 200

@sincronismo.route('/sincronismo/forcar')
def sinc_forc():
    # forca o sincronismo de usuarios e imagens
    sincronizar_usuarios()
    sincronizar_imagens()
    return "sincronização de usuários e imagens concluída com sucesso.", 200