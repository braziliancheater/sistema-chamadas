from app import db

class Usuarios(db.Model):
    """
    Criação da Tabela de Usuarios
    """
    __tablename__ = "usuarios"

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    ra = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    #imagens = db.relationship('Imagens', backref='usuario', lazy='dynamic')
    #logs = db.relationship('Logs', backref='usuario', lazy='dynamic')

    def __repr__(self):
        return "<usuarios: {}>".format(self.nome)

class Imagens(db.Model):
    """
    Criação da Tabela de Imagens
    """
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    imagem = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<imagens: {}>".format(self.imagem)

class Logs(db.Model):
    """
    Criação da Tabela de Logs
    """
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    evento = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<logs: {}>".format(self.evento)
