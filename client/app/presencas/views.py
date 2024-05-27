from . import presencas
from app import db, log
from ..tabelas import Presencas, Usuarios, Propriedades

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