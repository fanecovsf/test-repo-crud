from db_config import db

#Vibra
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Cliente(db.Model):
    __tablename__ = 'tb_clientes'
    __table_args__ = {'schema': 'sc_sap'}

    codigo = db.Column(db.String(), primary_key=True)
    nome = db.Column(db.String())
    modelo_de_negocio = db.Column(db.String())
    tipo_de_cliente = db.Column(db.String())

    def __init__(self, codigo, nome, modelo_de_negocio, tipo_cliente):
        self.codigo = codigo
        self.nome = nome
        self.modelo_de_negocio = modelo_de_negocio
        self.tipo_cliente = tipo_cliente


#Vibra Mongo
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Viagens(db.Model):
    __tablename__ = 'Viagens'
    __table_args__ = {'schema':'public'}
    __bind_key__ = 'BD01-VIBRA'

    id = db.Column(db.String(50), primary_key=True)
    uuidv = db.Column(db.String(50))
    idPlanoViagem = db.Column(db.String(50)) #documento_de_transporte

    def __init__(self, id, uuidv, idPlanoViagem):
        self.id = id
        self.uuidv = uuidv
        self.idPlanoViagem = idPlanoViagem



class Checkpoints(db.Model):
    __tablename__ = 'CheckPoints'
    __table_args__ = {'schema':'public'}
    __bind_key__ = 'BD01-VIBRA'

    id = db.Column(db.String(50), primary_key=True)
    uuidv = db.Column(db.String(50), db.ForeignKey('"Viagens".uuidv')) #index_checkpoint

    def __init__(self, id, uuidv):
        self.id = id
        self.uuidv = uuidv