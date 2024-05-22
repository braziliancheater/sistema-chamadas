from flask import render_template, request

from . import presencas

@presencas.route('/presencas_iniciar', methods=['POST'])
def presencas_iniciar():
    if request.method == 'POST':
        