from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .utils.utilidades import Logger, Utilidades

app = Flask(__name__)

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
    Logger.log_aviso('server', 'iniciando cliente')
    
    Logger.log_aviso('server', 'importando tabelas')
    from app import tabelas
    
    Logger.log_sucesso('server', 'criando blueprint index')
    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    Logger.log_sucesso('server', 'criando blueprint autenticação')
    from .autenticacao import autenticacao as auth_blueprint
    app.register_blueprint(auth_blueprint)

    Logger.log_sucesso('server', 'criando blueprint presenças')
    from .presencas import presencas as presencas_blueprint
    app.register_blueprint(presencas_blueprint)

    db.init_app(app)
    with app.app_context():
        if (db.create_all()):
            Logger.log_aviso('server', "criando tabelas")
        else:
            Logger.log_erro('server', "tabelas ja criadas, continuando")
            
    return app
