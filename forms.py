from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, FloatField, DecimalField
from wtforms.validators import DataRequired, URL, optional, NumberRange, Email
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    name = StringField("Nom", validators=[DataRequired()])
    submit = SubmitField("S'enregistrer")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("S'identifier")


class AddBeerForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    version = StringField("Version", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    description = CKEditorField("Description")
    submit = SubmitField("OK")


class ReviewForm(FlaskForm):
    mousse = IntegerField("Mousse (0 = Inexistante, 10 = Persistante)", validators=[optional(), NumberRange(min=0, max=10)])
    couleur = IntegerField("Couleur (0 = Foncée, 10 = Claire)", validators=[optional(), NumberRange(min=0, max=10)])
    transparence = IntegerField("Transparence (0 = Opaque, 10 = Transparente)", validators=[optional(), NumberRange(min=0, max=10)])
    douceur = IntegerField("Douceur (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    amertume = IntegerField("Amertume (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    acidite = IntegerField("Acidité (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    rondeur = IntegerField("Rondeur (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    gushing = IntegerField("Surmoussage (0 = Normal, 10 = Explosif)", validators=[optional(), NumberRange(min=0, max=10)])

    alcoolique = IntegerField("Alcoolique (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    ethere = IntegerField("Éthéré : banane, pomme (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    fruite = IntegerField("Fruité : agrumes, baies, melon, autres fruits (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    floral = IntegerField("Floral : fleurs, roses, parfum, vanille (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    houblonne = IntegerField("Houblonné (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    resineux = IntegerField("Résineux : sciure, résine, pin, épicéa, bois sec (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    noix = IntegerField("Noix (noix de cajou, noix, noisette, noix de coco (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    herbeux = IntegerField("Herbeux : (herbe fraichement coupée, paille) (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    cereales = IntegerField("Céréales : céréales crues, balle du grain, gruau, farine (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    caramel = IntegerField("Caramel (0-10)", validators=[optional(), NumberRange(min=0, max=10)])
    brule = IntegerField("Brulé (0-10)", validators=[optional(), NumberRange(min=0, max=10)])

    score = IntegerField("Note globale (0-10)", validators=[optional(), NumberRange(min=0, max=10)])

    submit = SubmitField("OK")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Commentaire", validators=[DataRequired()])
    submit = SubmitField("OK")
