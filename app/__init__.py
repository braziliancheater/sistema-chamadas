from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils.utilidades import Logs, Utilidades

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_servidor.db'

# Inicialize o SQLAlchemy com a aplicação Flask
db = SQLAlchemy()

def criar_sistema():
    Utilidades.limpa()
    Utilidades.logo()
    Logs.msg_aviso(__name__, 'Iniciando cliente...')
    
    Logs.msg_aviso(__name__, 'Importando tabelas...')
    from app import tabelas
    
    Logs.msg_sucesso(__name__, 'Criando index...')
    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    Logs.msg_sucesso(__name__, 'Criando autenticação...')
    from .autenticacao import autenticacao as auth_blueprint
    app.register_blueprint(auth_blueprint)

    db.init_app(app)
    with app.app_context():
        if (db.create_all()):
            Logs.msg_aviso(__name__, "Criando tabelas...")
        else:
            Logs.msg_erro(__name__, "Tabelas ja criadas")
            
    return app
