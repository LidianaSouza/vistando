from app import db

class Professor(db.Model):


    __tablename__ = "professores"

    siape = db.Column(db.String(11), primary_key=True, unique=True)
    name = db.Column(db.String)
    password = db.Column(db.String)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.siape

    def __init__(self, siape, name, password):

        self.siape = siape
        self.name = name
        self.password = password

    def __repr__(self):

        return self.siape # modo como sera a saida do bd

class Aluno(db.Model):


    __tablename__ = "alunos"

    dre = db.Column(db.String(7), primary_key=True, unique=True)
    name = db.Column(db.String)

    def __init__(self, dre, name):

        self.dre = dre
        self.name = name

    def __repr__(self):
        return self.dre

class Sala(db.Model):


    __tablename__ = "salas"
    siape = db.Column(db.String(11))
    titulo = db.Column(db.String)
    cod_sala = db.Column(db.String(5), primary_key=True, unique=True)
    senha = db.Column(db.String)

    def __init__(self, siape, titulo, cod_sala, senha):

        self.siape = siape
        self.titulo = titulo
        self.cod_sala = cod_sala
        self.senha = senha

    def __repr__(self):

        return self.titulo

class relSalaEAluno(db.Model):


    __tablename__ = "relSalaEAluno"
    dre = db.Column(db.String(7))
    cod_sala = db.Column(db.String(5))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, dre, cod_sala):

        self.dre = dre
        self.cod_sala = cod_sala


    def __repr__(self):

        return self.cod_sala

class Pedido(db.Model):


    __tablename__ = "pedido"
    dre = db.Column(db.String(7))
    pedido = db.Column(db.String, primary_key=True)

    def __init__(self, dre, pedido):

        self.dre = dre
        self.pedido = pedido

    def __repr__(self):

        return self.dre
