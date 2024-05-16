from flask import render_template, request

from . import autenticacao
from .. import db
from ..tabelas import Usuarios, Imagens

@autenticacao.route('/registrar', methods=['GET'])
def registrar():
    return render_template('autenticacao/registrar.html')

@autenticacao.route('/verificacao_facial')
def verificacao_facial():
    return render_template('autenticacao/verificacao_facial.html')

@autenticacao.route('/criar_conta', methods=['GET', 'POST'])
def efetuar_registro():
    if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            ra = request.form['ra']
            perfil = request.form['foto']
            
            print(f"[{__name__}] Criando Usuaurio: \nNome: {nome}\nEmail: {email} \nRA: {ra}")
            usuario = Usuarios(nome=nome, email=email, ra=ra)
            usuario_verifica = Usuarios.query.filter_by(email=email).first()
            if usuario_verifica:
                print(f"[{__name__}] Usuário já existe")
                return render_template('autenticacao/registrar.html',  Email='Email já cadastrado!')
            else:   
                print(f"{__name__}] Criando Usuario")
                db.session.add(usuario)
                db.session.commit()
                try :
                    print(f"[{__name__}] Criando Imagem")
                    imagem = Imagens(id_usuario=usuario.id, imagem=perfil)
                    db.session.add(imagem)
                    db.session.commit()
                except Exception as e:
                    print(f"[{__name__}] Erro ao criar imagem: {e}")
                    return "Erro ao cadastrar usuário!", 500

            return render_template('autenticacao/registro_sucesso.html')
    else:
         return "Erro ao cadastrar usuário!", 500