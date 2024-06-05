from flask import render_template
import requests

from . import presencas

@presencas.route('/presencas')
def presencas_home():
    status = requests.get('http://localhost:5001/obter_status')
    if status.status_code != 200:
        return render_template('autenticacao/presencas.html', status='Serviço indisponível')
    
    if status.text == '0':
        status = 'Presença não iniciada'
    elif status.text == '1':
        status = 'Presença em andamento'
    else:
        status = 'Erro ao obter status da presença'

    return render_template('autenticacao/presencas.html', status=status)

@presencas.route('/presencas_confirmar/<int:id>', methods=['POST'])
def efetuar_presenca(id):
    return render_template('presencas/efetuar_presenca.html', id=id)