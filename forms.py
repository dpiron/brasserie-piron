from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, FloatField, DecimalField, \
    HiddenField, DateTimeField
from wtforms.validators import DataRequired, URL, optional, NumberRange, Email
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    name = StringField("Prénom", validators=[DataRequired()])
    surname = StringField("Nom", validators=[DataRequired()])
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
    date = DateTimeField("Date (mm/yy) (Exemple : 06/22)", format='%m/%y', validators=[DataRequired()])
    # version = IntegerField("Version", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    malt = StringField('Malt (séparé par des virgules) (Exemple : "Pils, Munich II, Vienna, Froment blanc"')
    houblon = StringField('Houblon (séparé par des virgules) (Exemple : "Tettnang, Goldings, Styrian Goldings"')
    description = CKEditorField("Description")
    submit = SubmitField("OK")


class ReviewForm(FlaskForm):
    mousse = HiddenField("Mousse")
    couleur = HiddenField("Couleur")
    opacite = HiddenField("Opacité")
    petillant = HiddenField("Pétillant")
    douceur = HiddenField("Douceur")
    amertume = HiddenField("Amertume")
    acidite = HiddenField("Acidité")
    gushing = HiddenField("Surmoussage")

    alcooleux = HiddenField("Alcooleux")
    fruite = HiddenField("Fruité : agrumes, baies, melon, autres fruits")
    floral = HiddenField("Floral : fleurs, roses, parfum, vanille")
    houblonne = HiddenField("Houblonné")
    boise = HiddenField("Boisé : sciure, résine, pin, épicéa, bois sec")
    torrefie = HiddenField("Torréfié : ")
    herbeux = HiddenField("Herbeux : herbe fraichement coupée, paille")
    cereales = HiddenField("Céréales : céréales crues, balle du grain, gruau, farine")
    epice = HiddenField("Epicé")

    score = HiddenField("Note globale")

    submit = SubmitField("OK")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Commentaire", validators=[DataRequired()])
    submit = SubmitField("OK")
