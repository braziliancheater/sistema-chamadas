from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils.utilidades import Logger, Utilidades

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_cliente.db'

log = Logger()

# inicialize o SQLAlchemy com a aplicação Flask
db = SQLAlchemy()

def criar_cliente():
    Utilidades.limpar_tela()
    Utilidades.mostar_logo()
    log.log_aviso('cliente', 'iniciando cliente')
    
    try:
        log.log_sucesso('cliente', 'importando tabelas')
        from app import tabelas
        log.log_sucesso('cliente', 'importando tabelas')
    except Exception as e:
        log.log_erro('cliente', f'erro ao importar tabelas: {e}')
    
    log.log_sucesso('cliente', 'criando blueprint index')
    try:
        from .index import index as index_blueprint
        app.register_blueprint(index_blueprint)
        log.log_sucesso('cliente', 'blueprint index criado com sucesso')
    except Exception as e:
        log.log_erro('cliente', f'erro ao criar blueprint index: {e}')

    log.log_sucesso('cliente', 'criando blueprint presenças')
    try:
        from .presencas import presencas as presencas_blueprint
        app.register_blueprint(presencas_blueprint)
        log.log_sucesso('cliente', 'blueprint presenças criado com sucesso')
    except Exception as e:
        log.log_erro('cliente', f'erro ao criar blueprint presenças: {e}')

    db.init_app(app)
    with app.app_context():
        if (db.create_all()):
            log.log_sucesso('cliente', "criando tabelas")
        else:
            log.log_aviso('cliente', "tabelas ja criadas, continuando")
            
    return app