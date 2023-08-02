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