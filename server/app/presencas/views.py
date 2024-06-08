from flask import render_template, flash, redirect, url_for
import requests
from app import db

from . import presencas
from ..tabelas import Presencas, Usuarios

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

@presencas.route('/presencas_apagar/<int:id>', methods=['POST'])
def apagar_presenca(id):
    try:
        presenca = Presencas.query.get_or_404(id)
        db.session.delete(presenca)
        db.session.commit()
        flash('Presença apagada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao apagar a presença: {e}', 'danger')
    return redirect(url_for('presencas.historico'))

@presencas.route('/historico')
def historico():
    try:
        presencas = Presencas.query.all()
        for presenca in presencas:
            usuario = Usuarios.query.get(presenca.id_usuario)
            presenca.nome = usuario.nome
            presenca.ra = usuario.ra
        return render_template('presencas/historico.html', presencas=presencas)
    except Exception as e:
        return render_template('presencas/historico.html', presencas=[], erro=str(e))