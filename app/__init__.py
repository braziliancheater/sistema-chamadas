from flask import Flask
import sqlalchemy as db, 

def criar_sistema():
    app = Flask(__name__)
    
    engine = db.create_engine('sqlite:///banco_servidor.db')
    conn = engine.connect()

    from app import tabelas

    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    return app