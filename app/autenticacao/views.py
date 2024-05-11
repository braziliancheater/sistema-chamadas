from flask import render_template, request

from . import autenticacao
from .. import db
from ..tabelas import Usuarios, Imagens
import base64

import base64

@autenticacao.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        ra = request.form['ra']
        base64_image = request.form['base64']  # Get the base64 encoded image
        print(nome, email, ra, base64_image)

        # Decode base64 image data
        image_data = base64.b64decode(base64_image.split(',')[1])
        
        # Store image data in the database or process it as needed
        
        new_entry = Usuarios(nome=nome, email=email, ra=ra, imagem=image_data)
        all_users = Usuarios.query.filter_by(email=email).first()
        if all_users:
            print(all_users)
            # return render_template('register.html',  Email='already exist')
        else:   
            db.session.add(new_entry)
            db.session.commit()
            db.session.close()
        return render_template('autenticacao/registrar.html', nome=nome, email=email, ra=ra)
    return render_template('autenticacao/registrar.html')
