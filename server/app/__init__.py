from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .utils.utilidades import Logger, Utilidades

app = Flask(__name__)
log = Logger()

# Configurações do banco de dados
app.config['SECRET_KEY'] = 'chave_Secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_servidor.db'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'autenticacao.login'
login_manager.login_message_category = 'info'

# inicialize o SQLAlchemy com a aplicação Flask
db = SQLAlchemy()

def criar_sistema():
    Utilidades.limpar_tela()
    Utilidades.mostar_logo()
    log.log_aviso('server', 'iniciando cliente')
    
    log.log_aviso('server', 'importando tabelas')
    from app import tabelas
    
    Logger.log_aviso('server', 'criando blueprint index')
    try:
        from .index import index as index_blueprint
        app.register_blueprint(index_blueprint)
        log.log_sucesso('server', 'blueprint index criado com sucesso')
    except Exception as e:
        log.log_erro('server', f'erro ao criar blueprint index: {e}')

    log.log_aviso('server', 'criando blueprint autenticação')
    try:
        from .autenticacao import autenticacao as auth_blueprint
        app.register_blueprint(auth_blueprint)
        log.log_sucesso('server', 'blueprint autenticação criado com sucesso')
    except Exception as e:
        log.log_erro('server', f'erro ao criar blueprint autenticação: {e}')

    log.log_aviso('server', 'criando blueprint presenças')
    try:
        from .presencas import presencas as presencas_blueprint
        app.register_blueprint(presencas_blueprint)
        log.log_sucesso('server', 'blueprint presenças criado com sucesso')
    except Exception as e:
        log.log_erro('server', f'erro ao criar blueprint presenças: {e}')

    log.log_aviso('server', 'criando blueprint sincronismo')
    try:
        from .sincronismo import sincronismo as sincronismo_blueprint
        app.register_blueprint(sincronismo_blueprint)
        log.log_sucesso('server', 'blueprint sincronismo criado com sucesso')
    except Exception as e:
        log.log_erro('server', f'erro ao criar blueprint sincronismo: {e}')

    db.init_app(app)
    with app.app_context():
        if (db.create_all()):
            log.log_aviso('server', "criando tabelas")
        else:
            log.log_erro('server', "tabelas ja criadas, continuando")
            
    return app