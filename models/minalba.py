from db_config import db

#Minalba
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PlacasMinalba(db.Model):
    __tablename__ = 'tb_placas'
    __table_args__ = {'schema': 'sc_placa'}
    __bind_key__ = 'db_minalba'

    placa = db.Column(db.String(255), primary_key=True)
    classificacao = db.Column(db.String(255))

    def __init__(self, placa, classificacao):
        self.placa = placa
        self.classificacao = classificacao


class MsgMinalba(db.Model):
    __tablename__ = 'tb_macro_dimensao'
    __table_args__ = {'schema': 'sc_macros'}
    __bind_key__ = 'db_minalba'

    msg_original = db.Column(db.String(500), primary_key=True)
    msg_corrigida = db.Column(db.String(500))

    def __init__(self, msg_original, msg_corrigida):
        self.msg_original = msg_original
        self.msg_corrigida = msg_corrigida


#Escalation list
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Unidade(db.Model):
    __tablename__ = 'tb_unidades'
    __bind_key__ = 'test'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unidade = db.Column(db.String(500), nullable=False)

    def __init__(self, id, unidade):
        self.id = id
        self.unidade = unidade


class Contato(db.Model):
    __tablename__ = 'tb_contatos'
    __bind_key__ = 'test'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(500), nullable=False)
    cargo = db.Column(db.String(500), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    turno = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500))
    telefone = db.Column(db.String(500))

    unidade_id = db.Column(db.Integer, db.ForeignKey('tb_unidades.id'), nullable=False)
    unidade = db.relationship('Unidade', backref=db.backref('contatos', lazy=True))

    def __init__(self, id, nome, cargo, nivel, turno, email, telefone, unidade):
        self.id = id
        self.nome = nome
        self.cargo = cargo
        self.nivel = nivel
        self.turno = turno
        self.email = email
        self.telefone = telefone
        self.unidade = unidade
