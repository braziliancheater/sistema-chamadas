from app import db

class Usuarios(db.Model):
    """
        Criação da Tabela de Usuarios
    """
    __nome_tabela__ = "usuarios"

    id = db.Column(db.Integer(), primary_key=True),
    nome = db.Column(db.String(255), nullable=False),
    idade = db.Column(db.Integer(), nullable=False),
    email = db.Column(db.String(255), nullable=False),

    def __repr__(self):
        return "<usuarios: {}>".format(self.name)

class Imagens(db.Model):
    """
        Criação da Tabela de Imagens
    """
    id = db.Column(db.Integer(), primary_key=True),
    id_usuario = db.relationship('Usuarios', backref='imagens', lazy='dynamic', nullable=False),
    imagem = db.Column(db.String(max), nullable=False),

    def __repr__(self):
        return "<imagens: {}>".format(self.name)

class Logs(db.Model):
    """
        Criação da Tabela de Logs
    """
    id = db.Column(db.Integer(), primary_key=True),
    id_usuario = db.relationship('Usuarios', backref='logs', lazy='dynamic', nullable=False),
    evento = db.Column(db.String(255), nullable=False),

    def __repr__(self):
        return "<logs: {}>".format(self.name)