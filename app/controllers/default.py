from flask import render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, login_required, logout_user
from app import app, db, lm
from werkzeug.utils import secure_filename

from app.models.tables import Professor, Aluno, Sala
from app.models.forms import LoginForm, CriarSalaForm, EnvProvaForm

@app.route("/index",  methods=['GET','POST'])
@app.route("/")
def index():

    form = CriarSalaForm()
    if form.validate_on_submit():

        s = Sala.query.filter_by(cod_sala=form.cod_sala.data).first()
        #t = s.titulo
        #p = s.senha
        print(s)

    return render_template("index.html", form=form)

@lm.user_loader
def load_user(siape):
    return Professor.query.filter_by(siape=siape).first()

@app.route("/sair")
def sair():
    logout_user()
    session.pop('s', None)
    return redirect(url_for("index"))

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        p = Professor.query.filter_by(siape=form.siape.data).first()
        n = p.name
        if p and p.password == form.password.data:
            session['s'] = form.siape.data
            session['n'] = p.name
            login_user(p)
            print("maoe")
            flash("logged in")
            return redirect(url_for("portal"))
        else:
            flash("invalid login.")
    else:
        print(form.errors)
    return render_template("login.html", form=form)

@app.before_request
def before_request():

    if 's' in session:
        g.siape = session['s']
        g.name = session['n']

@app.route("/portal", methods=['GET','POST'])
def portal():
    form = CriarSalaForm()
    if g.siape:
        print(g.siape)
        print(g.name)
        s = Sala.query.filter_by().all()
        return render_template("portal.html", siape=g.siape, name=g.name, form=form, s=s)
    else:
        return render_template("login")

"""@app.route("/ler")
def ler():
    for i in s:
        print("linha "+str(i))
    return ok"""

@app.route("/result", methods=['GET','POST'])
def result():

    form = CriarSalaForm()
    s = Sala.query.filter_by(cod_sala=g.sala).all()
    return render_template("result.html", form=form, s=s)

@app.route("/resultAluno", methods=['GET','POST'])
def resultAluno():

    form = CriarSalaForm()
    s = Sala.query.filter_by().all()

    return render_template("resultAluno.html", form=form)

@app.route("/criarSala", methods=['GET','POST'])
def criarSala():
    form = CriarSalaForm()
    if form.validate_on_submit():
        cod = form.cod_sala.data
        tit = form.titulo.data
        senha = form.senha.data
        sala = Sala(tit, cod, senha)
        db.session.add(sala)
        db.session.commit()
        print("maoe")
        s = Sala.query.filter_by().all()
        return render_template("portal.html", siape=g.siape, name=g.name, form=form, s=s)
    else:
        print(form.errors)
        return render_template("criarSala.html", form=form)

@app.route("/sala", methods=['GET','POST'])
def sala():
    form = CriarSalaForm()
    s =  Aluno.query.filter_by().all()
    return render_template("sala.html", siape=g.siape, name=g.name, form=form, s=s)

@app.route("/salaAluno", methods=['GET','POST'])
def salaAluno():
    form = CriarSalaForm()
    s =  Aluno.query.filter_by().all()
    return render_template("salaAluno.html", form=form, s=s)

@app.route("/upProva", methods=['GET','POST'])
def upProva():
    form = EnvProvaForm()
    if form.validate_on_submit():
        p = form.prova.data
        filename = secure_filename(p.filename)
        p.save(os.path.join(
            app.instance_path, 'provas', filename
        ))
        return redirect(url_for(''))

    return render_template("upProva.html", siape=g.siape, name=g.name, form=form)


@app.route("/teste/<info>")
def teste(info):
    """i = Professor("19909090902", "maria", "1234")
    db.session.add(i)
    db.session.commit()"""
    s = Sala("abc", "1", "1234")
    db.session.add(s)
    db.session.commit()
    s2 = Sala("abcd", "2", "1234")
    db.session.add(s2)
    db.session.commit()
    s3 = Sala("abcde", "3", "1234")
    db.session.add(s3)
    db.session.commit()


    return "ok"

@app.route("/contato")
def echo():

    return render_template("contato.html")
