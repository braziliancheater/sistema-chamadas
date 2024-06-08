from . import presencas
from app import db, log
from ..tabelas import Presencas, Usuarios, Propriedades
from datetime import datetime
import requests

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
        # Atualiza a propriedade status para '0'
        propriedade.prop_valor = '0'
        db.session.commit()

        # Obter os usuários com presença registrada
        try:
            response = requests.get('http://localhost:5001/obter_usuarios')
            if response.status_code == 200:
                presencas_registradas = response.json()
                if isinstance(presencas_registradas, dict):
                    # Formatar dados para envio ao servidor
                    presencas_data = []
                    for nome, status in presencas_registradas.items():
                        if status == "Presença registrada":
                            try:
                                usuario = Usuarios.query.filter_by(nome=nome).first()
                                if usuario is None:
                                    continue

                                data = datetime.now().strftime("%Y-%m-%d")
                                hora = datetime.now().strftime("%H:%M:%S")
                                presencas_data.append({
                                    'nome': nome,
                                    'data': data,
                                    'hora': hora
                                })
                            except Exception as e:
                                log.log_erro(__name__, f"Erro ao formatar presença para {nome}: {str(e)}")

                    # Enviar dados ao servidor
                    try:
                        server_response = requests.post('http://localhost:5000/sincronismo/presencas', json=presencas_data)
                        if server_response.status_code == 200:
                            return "Presenças finalizadas e registradas no banco de dados do servidor.", 200
                        else:
                            return "Erro ao sincronizar presenças com o servidor.", 500
                    except Exception as e:
                        log.log_erro(__name__, f"Erro ao sincronizar presenças com o servidor: {str(e)}")
                        return "Erro ao sincronizar presenças com o servidor.", 500
                else:
                    return "Nenhuma presença registrada.", 200
            else:
                return "Erro ao obter usuários.", 500
        except Exception as e:
            log.log_erro(__name__, f"Erro ao obter usuários: {str(e)}")
            return "Erro ao obter usuários.", 500
    else:
        return "Presenças já finalizadas.", 200

# nao em uso mais
@presencas.route('/presencas/registrar/<string:nome>')
def presencas_registrar(nome):
    log.log_aviso(__name__, f"Iniciando processo de presença: {nome}")
    propriedades = Propriedades.query.filter_by(prop_nome='status').first()
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
    