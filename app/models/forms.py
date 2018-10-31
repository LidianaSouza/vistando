from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, TextAreaField
from flask_wtf.file import  FileRequired
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):


    siape = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class CriarSalaForm(FlaskForm):


    titulo = StringField("Nome da sala", validators=[DataRequired()])
    cod_sala = StringField("Código da sala", validators=[DataRequired()])
    senha = PasswordField("Senha da sala", validators=[DataRequired()])

class EnvProvaForm(FlaskForm):


    dre = StringField("Nome da sala", validators=[DataRequired()])
    prova = FileField(validators=[FileRequired()])

class PedidoForm(FlaskForm):


    dre = StringField("Nome da sala", validators=[DataRequired()])
    pedido = TextAreaField("Pedido", validators=[DataRequired()])
