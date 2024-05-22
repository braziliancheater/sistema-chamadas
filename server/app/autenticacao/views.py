from flask import render_template, request, redirect, url_for, flash

from . import autenticacao
from .. import db, bcrypt
from ..tabelas import Usuarios, Imagens
from ..forms import FormularioLogin, FormularioRegistro
from flask_login import login_user, current_user, logout_user, login_required

"""
    Rotas para registro de usuários
"""
@autenticacao.route('/registrar', methods=['GET'])
def registrar():
    return render_template('autenticacao/registrar.html')

@autenticacao.route('/verificacao_facial')
def verificacao_facial():
    return render_template('autenticacao/verificacao_facial.html')

@autenticacao.route("/criar_conta", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('autenticacao.dashboard'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        ra = request.form['ra']
        senha = request.form['senha']
        perfil = request.form['foto']

        print(f"[{__name__}] Criando Usuaurio: \nNome: {nome}\nEmail: {email} \nRA: {ra}\nSenha: {senha}")
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')
        usuario = Usuarios(nome=nome, email=email, ra=ra, senha=hashed_password)
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
                flash("Erro ao cadastrar usuário!", 'error')
            
            flash('Sua conta foi criada com sucesso, faca login para acessar', 'success')
    return redirect(url_for('autenticacao.login'))

"""
    Rotas para login de usuários
"""
@autenticacao.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('autenticacao.dashboard'))
    form = FormularioLogin()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.password.data):
            login_user(user) # , remember=form.remember.data
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('autenticacao.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('autenticacao/login.html', title='Login', form=form)

@autenticacao.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('autenticacao.login'))

@autenticacao.route("/dashboard")
@login_required
def dashboard():
    return render_template('autenticacao/dashboard.html', title='Dashboard')

@autenticacao.route("/lista_usuarios")
@login_required
def lista_usuarios():
    usuarios = Usuarios.query.all()
    return render_template('autenticacao/lista_usuarios.html', title='Lista de Usuários', usuarios=usuarios)

@autenticacao.route("/deletar_usuario/<int:id>", methods=['POST'])
@login_required
def deletar_usuario(id):
    user = Usuarios.query.get_or_404(id)
    try:
        # Deleting the associated images first
        Imagens.query.filter_by(id_usuario=id).delete()
        db.session.delete(user)
        db.session.commit()
        flash('Usuario foi deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao apagar o usuario: {e}', 'danger')
    return redirect(url_for('autenticacao.lista_usuarios'))