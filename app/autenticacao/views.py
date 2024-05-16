from flask import render_template, request

from . import autenticacao
from .. import db
from ..tabelas import Usuarios, Imagens
import base64

import base64

@autenticacao.route('/registrar', methods=['GET'])
def registrar():
    return render_template('autenticacao/registrar.html')


@autenticacao.route('/verificacao_facial')
def verificacao_facial():
    return render_template('autenticacao/verificacao_facial.html')

@autenticacao.route('/registrar3', methods=['GET', 'POST'])
def efetuar_registro():
    if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            ra = request.form['ra']
            perfil = request.form['foto']
            
            #print(f"nome do cabra: {nome}\n email: {email} \n ra: {ra} \n imagem: {base64_image}")
            new_entry = Usuarios(nome=nome, email=email, ra=ra, imagem=perfil)
            all_users = Usuarios.query.filter_by(email=email).first()
            if all_users:
                print(all_users)
                # return render_template('register.html',  Email='already exist')
            else:   
                db.session.add(new_entry)
                db.session.commit()
                db.session.close()

            return "marcha";
    else:
         return "nem"