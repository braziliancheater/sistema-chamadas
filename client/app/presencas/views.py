from . import presencas
from app import db, log
from ..tabelas import Presencas, Usuarios, Propriedades
from datetime import datetime

@presencas.route('/presencas/iniciar', methods=['GET'])
def iniciar_presencas():
    propriedade = Propriedades.query.filter_by(prop_nome='status').first()
    if propriedade.prop_valor is None:
        return "Propriedade status não encontrada.", 404
    
    if propriedade.prop_valor == '0':
        propriedade.prop_valor = '1'
        db.session.commit()
        return "Presenças iniciadas.", 200
    else:
        return "Presenças já iniciadas.", 200
    
@presencas.route('/presencas/parar', methods=['GET'])
def parar_presencas():
    propriedade = Propriedades.query.filter_by(prop_nome='status').first()
    if propriedade.prop_valor is None:
        return "Propriedade status não encontrada.", 404
    
    if propriedade.prop_valor == '1':
        propriedade.prop_valor = '0'
        db.session.commit()
        return "Presenças finalizadas.", 200
    else:
        return "Presenças já finalizadas.", 200
    
@presencas.route('/presencas/registrar/<string:nome>')
def presencas_registrar(nome):
    log.log_aviso(__name__, f"Iniciando processo de presença: {nome}")
    propriedades = Propriedades.query.all()
    if propriedades.prop_valor == '1':
        try:
            usuario = Usuarios.query.filter_by(nome=nome).first()
            if usuario is None:
                return "Usuário não encontrado.", 404
            
            data = datetime.now().strftime("%d/%m/%Y")
            hora = datetime.now().strftime("%H:%M:%S")
            presenca = Presencas(id_usuario=usuario.id, data=data, hora=hora)
            db.session.add(presenca)
            db.session.commit()
            log.log_sucesso(__name__, f"Presença registrada: {nome}")
            return "Presença registrada.", 200
        except Exception as e:
            log.log_erro(__name__, f"Erro ao registrar presença: {str(e)}")
            return "Erro ao registrar presença.", 500
    else:
        return "O sistema de presenças não foi iniciado.", 200
    