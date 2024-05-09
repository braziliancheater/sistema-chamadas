from flask import Flask
import sqlalchemy as db
from flask_sqlalchemy import SQLAlchemy
from utils import utils

db = SQLAlchemy()

def criar_sistema():
    utils.utils.limpa()
    utils.utils.logo()
    utils.logs.aviso('iniciando cliente...')
    
    app = Flask(__name__)
    
    engine = db.create_engine('sqlite:///banco_servidor.db')
    conn = engine.connect()

    utils.logs.aviso('importando tabelas...')
    try:
        from app import tabelas
    except Exception as e:
        utils.logs.erro(f'falha ao criar tabelas: {e}')
        return

    utils.logs.sucesso('criando index...')
    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    utils.logs.sucesso('criando autenticacao...')
    from .autenticacao import autenticacao as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app