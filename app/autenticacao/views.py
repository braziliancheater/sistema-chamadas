from flask import render_template

from . import autenticacao

@autenticacao.route('/registrar')
def registrar():
    return render_template('autenticacao/registrar.html')