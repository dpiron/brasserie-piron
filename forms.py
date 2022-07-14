from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, FloatField, DecimalField, HiddenField
from wtforms.validators import DataRequired, URL, optional, NumberRange, Email
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    name = StringField("Nom", validators=[DataRequired()])
    submit = SubmitField("S'inscrire")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("S'identifier")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Réinitialiser mot de passe")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Nouveau mot de passe", validators=[DataRequired()])
    submit = SubmitField("Modifier le mot de passe")


class AddBeerForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    # version = IntegerField("Version", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    description = CKEditorField("Description")
    submit = SubmitField("OK")


class ReviewForm(FlaskForm):
    mousse = HiddenField("Mousse")
    couleur = HiddenField("Couleur")
    opacite = HiddenField("Opacité")
    douceur = HiddenField("Douceur")
    amertume = HiddenField("Amertume")
    acidite = HiddenField("Acidité")
    gushing = HiddenField("Surmoussage")

    alcoolique = HiddenField("Alcoolique")
    ethere = HiddenField("Éthéré : banane, pomme")
    fruite = HiddenField("Fruité : agrumes, baies, melon, autres fruits")
    floral = HiddenField("Floral : fleurs, roses, parfum, vanille")
    houblonne = HiddenField("Houblonné")
    resineux = HiddenField("Résineux : sciure, résine, pin, épicéa, bois sec")
    chocolat = HiddenField()
    herbeux = HiddenField("Herbeux : herbe fraichement coupée, paille")
    cereales = HiddenField("Céréales : céréales crues, balle du grain, gruau, farine")
    caramel = HiddenField("Caramel")
    brule = HiddenField("Brulé")

    score = HiddenField("Note globale")

    submit = SubmitField("OK")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Commentaire", validators=[DataRequired()])
    submit = SubmitField("OK")
