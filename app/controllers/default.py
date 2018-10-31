from flask import render_template, request, redirect, url_for, flash, session, g, current_app
from flask_login import login_user, login_required, logout_user
from app import app, db, lm
from werkzeug import secure_filename
import requests
from app.models.tables import Professor, Aluno, Sala, relSalaEAluno, Pedido
from app.models.forms import LoginForm, CriarSalaForm, EnvProvaForm, PedidoForm
import os

@app.route("/index",  methods=['GET','POST'])
@app.route("/")
def index():

    form = CriarSalaForm()
    if request.method == 'POST':
        lab = request.form
        k = lab['cod_sala']
        session['cod'] = k
        u = Sala.query.filter_by(cod_sala=k).first()
        v = Professor.query.filter_by(siape=u.siape).first()
        session['n'] = v.name
        return redirect(url_for('resultAluno'))

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
        g.cod = session['cod']
    if 'cod' in session:
        g.cod = session['cod']
        g.name = session['n']

@app.route("/portal", methods=['GET','POST'])
def portal():

    form = CriarSalaForm()
    if g.siape:
        print(g.siape)
        print(g.name)
        s = Sala.query.filter_by().all()
        if request.method == 'POST':
            return redirect(url_for('criarSala'))
    return render_template("portal.html", siape=g.siape, name=g.name, form=form, s=s)\

@app.route("/resultAluno", methods=['GET','POST'])
def resultAluno():

    form = CriarSalaForm
    if request.method == 'POST':
        return redirect(url_for('validSalaAluno', cod2=g.cod))
    s = Sala.query.filter_by(cod_sala=g.cod).first()
    return render_template("resultAluno.html", form=form, s=s)

@app.route("/criarSala", methods=['GET','POST'])
def criarSala():

    form = CriarSalaForm()
    if form.validate_on_submit():
        cod = form.cod_sala.data
        tit = form.titulo.data
        senha = form.senha.data
        sala = Sala(g.siape, tit, cod, senha)
        db.session.add(sala)
        db.session.commit()
        s = Sala.query.filter_by().all()
        return redirect(url_for('portal'))
    else:
        print(form.errors)
    return render_template("criarSala.html", form=form)

@app.route("/cod/<cod>", methods=['GET','POST'])
def cod(cod):
    session['cod'] = cod
    return redirect(url_for('sala'))

@app.route("/sala", methods=['GET','POST'])
def sala():

    rel = request.args.get("rel")
    form = CriarSalaForm()
    if g.cod:
        t = Sala.query.filter_by(cod_sala=g.cod).first()
    s = relSalaEAluno.query.filter_by(cod_sala=g.cod).all()
    if request.method == 'POST':
        return redirect(url_for('upProva'))
    return render_template("sala.html", siape=g.siape, name=g.name, form=form, s=s, t=t)

@app.route("/aluno/<dre>", methods=['GET','POST'])
def aluno(dre):

    t = Sala.query.filter_by(cod_sala=g.cod).first()
    s = relSalaEAluno.query.filter_by(cod_sala=g.cod)
    a = Aluno.query.filter_by(dre=dre).first()
    return render_template("aluno.html", a=a, name=g.name, s=s, t=t)

@app.route("/pedido/<dre>", methods=['GET','POST'])
def pedido(dre):

    form = PedidoForm()
    t = Sala.query.filter_by(cod_sala=g.cod).first()
    s = relSalaEAluno.query.filter_by(cod_sala=g.cod)
    a = Aluno.query.filter_by(dre=dre).first()
    if request.method == 'POST':
        p = form.pedido.data
        ped = Pedido(dre, p)
        db.session.add(ped)
        db.session.commit()
        return redirect(url_for('salaAluno'))
    return render_template("pedido.html", t=t, s=s, a=a, form=form, name=g.name, dre=dre)

@app.route("/pedidosProf", methods=['GET','POST'])
def pedidosProf():

    t = Sala.query.filter_by(cod_sala=g.cod).first()
    c = relSalaEAluno.query.filter_by(cod_sala=g.cod).all()
    p = Pedido.query.filter_by().all()
    return render_template("pedidosProf.html", t=t, c=c, p=p, name=g.name)

@app.route("/excluirAluno/<dre>", methods=['GET','POST'])
@app.route("/excluirAluno", methods=['GET','POST'])
def excluirAluno(dre):

    a = relSalaEAluno.query.filter_by(dre=dre).first()
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('sala'))

@app.route("/revisado/<ped>", methods=['GET','POST'])
def revisado(ped):

    p = Pedido.query.filter_by(pedido=ped).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("pedidosProf"))

@app.route("/excluirSala/<cod_sala>", methods=['GET','POST'])
@app.route("/excluirSala", methods=['GET','POST'])
def excluirSala(cod_sala):

    s = Sala.query.filter_by(cod_sala=cod_sala).first()
    db.session.delete(s)
    a = relSalaEAluno.query.filter_by(cod_sala=cod_sala)
    for c in a:
        db.session.delete(c)
    db.session.commit()
    return redirect(url_for('portal'))

@app.route("/validSalaAluno", methods=['GET','POST'])
def validSalaAluno():

    form = CriarSalaForm()
    if request.method == 'POST':
        lab = request.form
        print(lab)
        k = lab['senha']
        r = Sala.query.filter_by(cod_sala=g.cod).first()
        if r and r.senha == k:
            return redirect(url_for('salaAluno'))
    return render_template("validSalaAluno.html", form=form)

@app.route("/salaAluno", methods=['GET','POST'])
def salaAluno():

    form = CriarSalaForm()
    t = Sala.query.filter_by(cod_sala=g.cod).first()
    s = relSalaEAluno.query.filter_by(cod_sala=g.cod)
    return render_template("salaAluno.html",name=g.name, form=form, s=s, t=t)

@app.route("/upProva", methods=['GET','POST'])
def upProva():

    form = EnvProvaForm()
    print(g.cod)
    p = form.prova.data
    d = form.dre.data
    if request.method == 'POST':
        if p:
            filename = secure_filename(p.filename)
            path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
            p.save(path)
            image = Aluno(d, filename)
            db.session.add(image)
            db.session.commit()
            rel = relSalaEAluno(d, g.cod)
            db.session.add(rel)
            db.session.commit()
        return redirect(url_for('sala'))

    return render_template("upProva.html", siape=g.siape, name=g.name, form=form)

#  adciona dados na lista. é necessário quando o bd é excluido.
@app.route("/teste/<info>")
def teste(info):
    i = Professor("19909090902", "maria", "1234")
    db.session.add(i)
    db.session.commit()
    return "ok"
