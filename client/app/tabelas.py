from app import db

class Usuarios(db.Model):
    """
        Criação da Tabela de Usuários
    """

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    ra = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    professor = db.Column(db.String(255), nullable=True)
    imagens = db.relationship('Imagens', backref='usuario', lazy=True)

    def __repr__(self):
        return "<usuarios: {}>".format(self.nome)

class Imagens(db.Model):
    __tablename__ = "imagens"

    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    imagem = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<imagens: {}>".format(self.imagem)
    
class Propriedades(db.Model):
    """
        Criação da Tabela de Propriedades
    """
    id = db.Column(db.Integer(), primary_key=True)
    prop_nome = db.Column(db.String(255), nullable=False)
    prop_valor = db.Column(db.String(255), nullable=False)
    
class Materias(db.Model):
    """
        Criação da Tabela de Matérias
    """
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<materias: {}>".format(self.nome)

class Presencas(db.Model):
    """
        Criação da Tabela de Presenças
    """
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    id_materia = db.Column(db.Integer(), db.ForeignKey('materias.id'), nullable=True)
    data = db.Column(db.String(255), nullable=False)
    hora = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<presencas: {}>".format(self.data)