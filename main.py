from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_paginate import Pagination, get_page_args
from models.minalba import MsgMinalba, PlacasMinalba, Contato, Unidade
from models.vibra import Cliente, Viagens, Checkpoints
from db_config import db
from sqlalchemy import exc, event, case
import json


app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_vibra'
app.config['SQLALCHEMY_DATABASE_URI_2'] = 'sqlite:///db_minalba'
app.config['SQLALCHEMY_DATABASE_URI_3'] = 'sqlite:///BD01-VIBRA'
app.config['SQLALCHEMY_DATABASE_URI_4'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_BINDS'] = {
    'db_vibra': app.config['SQLALCHEMY_DATABASE_URI'],
    'db_minalba': app.config['SQLALCHEMY_DATABASE_URI_2'],
    'BD01-VIBRA': app.config['SQLALCHEMY_DATABASE_URI_3'],
    'test': app.config['SQLALCHEMY_DATABASE_URI_4']
}

app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
app.config['SQLALCHEMY_POOL_RECYCLE'] = 300

db.init_app(app=app)

with app.app_context():
    @event.listens_for(db.engine, "engine_connect")
    def on_connect(dbapi_connection, connection_record):
        if hasattr(dbapi_connection, 'ping'):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("SELECT 1")
            except:
                cursor.close()
                dbapi_connection.close()
                raise exc.DisconnectionError()
            cursor.close()


@app.route('/')
def init():
    return 'Online'


@app.route('/teste', methods=['GET'])
def viagens():
    operacao_expr = case(
        (Viagens.idPlanoViagem.like('4%'), 'OUTBOUND'),
        else_='INBOUND'
    )

    query = db.session.query(Checkpoints, Viagens.idPlanoViagem, operacao_expr.label('operacao')).join(Viagens, Checkpoints.uuidv == Viagens.uuidv).limit(100)
    data_list = []

    for checkpoint, idPlanoViagem, operacao in query:
        
        data = {
            'checkpoint_id': checkpoint.id,
            'checkpoint_uuid': checkpoint.uuidv,
            'idPlanoViagem': idPlanoViagem,
            'operacao': operacao
        }

        data_list.append(data)

    return jsonify(data_list)


@app.route('/clientes')
def table():
    search_term = request.args.get('search')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    if search_term:
        clientes = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).offset(offset).limit(per_page)
        total = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).count()
    else:
        clientes = db.session.query(Cliente).offset(offset).limit(per_page)
        total = db.session.query(Cliente).count()

    pagination = Pagination(page=page, total=total, record_name='clientes', per_page=per_page, css_framework='bootstrap4')

    return render_template('index.html', clientes=clientes, pagination=pagination)


@app.route('/clientes/edit/<codigo>', methods=['GET', 'POST'])
def edit(codigo):
    cliente = db.session.get(Cliente, codigo)
    if request.method == 'POST':
        cliente.modelo_de_negocio = request.form['modelo']
        cliente.tipo_de_cliente = request.form['tipo_cliente']
        db.session.commit()
        return redirect(url_for('table'))
    
    return render_template('edit.html', cliente=cliente)


@app.route('/placas-minalba')
def placas_minalba():
    search_term = request.args.get('search')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    if search_term:
        placas = db.session.query(PlacasMinalba).filter(PlacasMinalba.placa.ilike(f'%{search_term}%')).offset(offset).limit(per_page)
        total = db.session.query(PlacasMinalba).filter(PlacasMinalba.placa.ilike(f'%{search_term}%')).count()
    else:
        placas = db.session.query(PlacasMinalba).offset(offset).limit(per_page)
        total = db.session.query(PlacasMinalba).count()

    pagination = Pagination(page=page, total=total, record_name='placas', per_page=per_page, css_framework='bootstrap4')

    return render_template('placas-minalba.html', placas=placas, pagination=pagination)


@app.route('/placas-minalba/edit/<placa>', methods=['GET', 'POST'])
def edit_placa(placa):
    placa = db.session.get(PlacasMinalba, placa)
    if request.method == 'POST':
        placa.classificacao = request.form['classificacao']
        db.session.commit()
        return redirect(url_for('placas_minalba'))
    
    return render_template('edit-placas-minalba.html', placa=placa)


@app.route('/macros-minalba')
def macros_minalba():
    search_term = request.args.get('search')

    if search_term:
        macros = db.session.query(MsgMinalba).filter(MsgMinalba.msg_original.ilike(f'%{search_term}%')).order_by(MsgMinalba.msg_original)
    else:
        macros = db.session.query(MsgMinalba).order_by(MsgMinalba.msg_original)

    return render_template('macros-minalba.html', macros=macros)


@app.route('/macros-minalba/edit/<msg>', methods=['GET', 'POST'])
def edit_macros(msg):
    if not db.session.get(MsgMinalba, msg):
        msg = str(msg).replace('-','/')
        macro = db.session.get(MsgMinalba, msg)
    else:
        macro = db.session.get(MsgMinalba, msg)

    msgs = [
        'NÃO INFORMADO',
        'CHEGADA CLIENTE/CD',
        'EMERGENCIA',
        'FIM DE CHECK LIST',
        'PARADA PARA REFEIÇÃO',
        'FIM DE JORNADA',
        'INICIO DE CHECK LIST',
        'CHEGADA NA FABRICA',
        'INICIO DE JORNADA',
        'ABASTECIMENTO',
        'INICIO DE VIAGEM',
        'FATURAMENTO',
        'PARADA PARA DESCANSO',
        'PERNOITE',
        'CHEGADA GARAGEM',
        'CHEGADA NA OFICINA',
        'REINICIO DE VIAGEM',
        'SCRIPT: MANUTENÇÃO - FADEL',
        'TROCA DE MOTORISTA',
    ]

    msgs.sort()

    if request.method == 'POST':
        macro.msg_corrigida = request.form['nova']
        db.session.commit()
        return redirect(url_for('macros_minalba'))
    
    return render_template('edit-macros-minalba.html', macro=macro, msgs=msgs)


@app.route('/minalba/contatos')
def contatos():
    contatos = db.session.query(Contato)

    data_list = []

    for contato in contatos:
        data = {
            'id':contato.id,
            'nome':contato.nome,
            'cargo':contato.cargo,
            'nivel':contato.nivel,
            'turno':contato.turno,
            'email':contato.email,
            'telefone':contato.telefone,
            'unidade': {
                'id': contato.unidade.id,
                'unidade': contato.unidade.unidade
            }
        }

        data_list.append(data)

    return Response(response=json.dumps(data_list, ensure_ascii=False), status=200, content_type="application/json")


@app.route('/minalba/contatos/<int:id>')
def contato(id):
    contato = db.session.get(Contato, id)

    data = {
        'id':contato.id,
        'nome':contato.nome,
        'cargo':contato.cargo,
        'nivel':contato.nivel,
        'turno':contato.turno,
        'email':contato.email,
        'telefone':contato.telefone,
        'unidade': {
            'id': contato.unidade.id,
            'unidade': contato.unidade.unidade
        }
    }

    return Response(response=json.dumps(data, ensure_ascii=False), status=200, content_type="application/json")


#@app.route('/minalba/contatos/add')



if __name__ == '__main__':
    with app.app_context():
        db.create_all('test')

        '''
        unidade1 = Unidade(None, 'Campos do Jordão')
        unidade2 = Unidade(None, 'Barra funda')
        
        db.session.add(unidade1)
        db.session.add(unidade2)

        contato1 = Contato(None, 'Luciano', 'Diretor', 4, 'ADM', None, None, unidade1)
        contato2 = Contato(None, 'Anderson', 'Supervisor', 2, 'B', None, None, unidade2)

        db.session.add(contato1)
        db.session.add(contato2)
        '''


        db.session.commit()

    app.run(debug=True, host='0.0.0.0', port=8080)
