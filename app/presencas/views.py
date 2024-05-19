from flask import render_template

from . import presencas

@presencas.route('/presencas')
def presencas_home():
    return render_template('presencas/presencas.html')

@presencas.route('/presencas_confirmar/<int:id>', methods=['POST'])
def efetuar_presenca(id):
    return render_template('presencas/efetuar_presenca.html', id=id)