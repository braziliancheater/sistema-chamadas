import os
import sqlalchemy as db
import utils.utils as utils
from flask import Flask, render_template, request, redirect, url_for

# inicializa a conexão com o banco de dados
engine = db.create_engine('sqlite:///banco_servidor.db')
conn = engine.connect()
app = Flask(__name__)

def setup_tabelas():
    metadata = db.MetaData()

    # cria a tabela de usuarios caso não exista
    tb_usuarios = db.Table('usuarios', metadata,
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('nome', db.String(255), nullable=False),
        db.Column('idade', db.Integer(), nullable=False),
        db.Column('email', db.String(255), nullable=False),
    )

    # cria a tabela de imagens de usuario
    tb_imagens = db.Table('imagens', metadata,
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('id_usuario', db.Integer(), db.ForeignKey('usuarios.id'), nullable=False),
        db.Column('imagem', db.String(max), nullable=False),
    )
    
    # tabela de logs de acesso
    tb_logs = db.Table('logs', metadata,
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('id_usuario', db.Integer(), db.ForeignKey('usuarios.id'), nullable=False),
        db.Column('evento', db.String(255), nullable=False),   
    )

    # efetiva a criação das tabelas
    metadata.create_all(engine)

def main(): 
    utils.utils.limpa()
    utils.utils.logo()
    utils.logs.aviso('iniciando backend...')
    utils.logs.aviso('criando tabelas...')
    try:
        setup_tabelas()
        utils.logs.sucesso('tabelas criadas com sucesso')
    except Exception as e:
        utils.logs.erro(f'falha ao criar tabelas: {e}')
        return

from endpoints.crud import crud

if __name__ == '__main__':
    main()
    app.run(debug=False, port=1337) # iniciando em modo de debug