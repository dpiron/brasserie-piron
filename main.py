import os
from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import AddBeerForm, ReviewForm, RegisterForm, LoginForm, CommentForm
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
bootstrap = Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///brasserie-piron.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(250))
    name = db.Column(db.String(250))

    # This will act like a List of Comment objects attached to each User.
    # The "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")

    # This will act like a List of Review objects attached to each User.
    # The "review_author" refers to the review_author property in the Review class.
    reviews = relationship("Review", back_populates="review_author")


class Beer(db.Model):
    __tablename__ = "beers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    type = db.Column(db.String(100))
    version = db.Column(db.Integer)
    description = db.Column(db.String(1000))

    mousse = db.Column(db.Float)
    couleur = db.Column(db.Float)
    transparence = db.Column(db.Float)
    douceur = db.Column(db.Float)
    amertume = db.Column(db.Float)
    acidite = db.Column(db.Float)
    rondeur = db.Column(db.Float)
    gushing = db.Column(db.Float)

    alcoolique = db.Column(db.Float)
    ethere = db.Column(db.Float)
    fruite = db.Column(db.Float)
    floral = db.Column(db.Float)
    houblonne = db.Column(db.Float)
    resineux = db.Column(db.Float)
    noix = db.Column(db.Float)
    herbeux = db.Column(db.Float)
    cereales = db.Column(db.Float)
    caramel = db.Column(db.Float)
    brule = db.Column(db.Float)

    score = db.Column(db.Float)

    # This will act like a List of Review objects attached to each Beer.
    # The "reviews_beer" refers to the reviews_beer property in the Review class.
    reviews = relationship("Review", back_populates="reviews_beer")

    # This will act like a List of Comment objects attached to each Beer.
    # The "comments_beer" refers to the comments_beer property in the Comment class.
    comments = relationship("Comment", back_populates="comments_beer")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    mousse = db.Column(db.Integer)
    couleur = db.Column(db.Integer)
    transparence = db.Column(db.Integer)
    douceur = db.Column(db.Integer)
    amertume = db.Column(db.Integer)
    acidite = db.Column(db.Integer)
    rondeur = db.Column(db.Integer)
    gushing = db.Column(db.Integer)

    alcoolique = db.Column(db.Integer)
    ethere = db.Column(db.Integer)
    fruite = db.Column(db.Integer)
    floral = db.Column(db.Integer)
    houblonne = db.Column(db.Integer)
    resineux = db.Column(db.Integer)
    noix = db.Column(db.Integer)
    herbeux = db.Column(db.Integer)
    cereales = db.Column(db.Integer)
    caramel = db.Column(db.Integer)
    brule = db.Column(db.Integer)

    score = db.Column(db.Integer)

    # Create Foreign Key, "beers.id" the users refers to the tablename of Beer.
    beer_id = db.Column(db.Integer, db.ForeignKey("beers.id"))
    # Create reference to the Beer object, the "reviews" refers to the reviews property in the Beer class.
    reviews_beer = relationship("Beer", back_populates="reviews")

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "reviews" refers to the reviews property in the User class.
    review_author = relationship("User", back_populates="reviews")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "comments" refers to the comments property in the User class.
    comment_author = relationship("User", back_populates="comments")

    # Create Foreign Key, "beers.id" the beers refers to the tablename of Beer.
    beer_id = db.Column(db.Integer, db.ForeignKey("beers.id"))
    # Create reference to the Beer object, the "comments" refers to the comments property in the Beer class.
    comments_beer = relationship("Beer", back_populates="comments")

    text = db.Column(db.String(1000))


db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Please register first!")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password, password):
            flash("Wrong password!")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    home_beer_list = []
    beer_name_list = [beer.name for beer in Beer.query.filter_by(version=1)]
    for name in beer_name_list:
        versioned_beers = Beer.query.filter_by(name=name)
        versions_list = [beer.version for beer in versioned_beers]
        max_version = max(versions_list)
        final_beer = [beer for beer in versioned_beers if beer.version == max_version][0]
        home_beer_list.append(final_beer)

    return render_template("index.html", beers=home_beer_list)


@app.route('/beer/<int:beer_id>')
def beer(beer_id):
    selected_beer = Beer.query.get(beer_id)
    all_versions = Beer.query.filter_by(name=selected_beer.name)
    versions_list = [item for item in all_versions]
    n_versions = len(versions_list)
    review_list = [item for item in selected_beer.reviews]
    n_reviews = len(review_list)
    if current_user.is_authenticated:
        users_list = [review.review_author for review in review_list]
        is_reviewed = current_user in users_list
    else:
        is_reviewed = False
    if is_reviewed:
        selected_review = [review for review in review_list if review.review_author == current_user]
        review_id = selected_review[0].id
    else:
        review_id = 0
    comments = Comment.query.filter_by(comments_beer=selected_beer)
    return render_template("beer.html", beer=selected_beer, all_versions=all_versions, n_reviews=n_reviews,
                           is_reviewed=is_reviewed, review_id=review_id, comments=comments, n_versions=n_versions)


# ADMIN ZONE
@app.route('/admin')
@admin_only
def admin():
    return render_template("admin.html")


@app.route('/admin-add-beer-page')
@admin_only
def admin_add_beer_page():
    beers = Beer.query.all()
    return render_template("admin-add-beer-page.html", beers=beers)


@app.route('/admin-add-beer', methods=['GET', 'POST'])
@admin_only
def admin_add_beer():
    form = AddBeerForm()
    if form.validate_on_submit():
        new_beer = Beer(
            name=form.name.data,
            type=form.type.data,
            version=form.version.data,
            description=form.description.data
        )
        db.session.add(new_beer)
        db.session.commit()
        return redirect(url_for("admin_add_beer_page"))
    return render_template("admin-form.html", form=form)


@app.route('/admin-edit-beer-page')
@admin_only
def admin_edit_beer_page():
    beers = Beer.query.all()
    return render_template("admin-edit-beer-page.html", beers=beers)


@app.route("/admin-edit-beer/<int:beer_id>", methods=['GET', 'POST'])
@admin_only
def admin_edit_beer(beer_id):
    beer_to_edit = Beer.query.get(beer_id)
    edit_form = AddBeerForm(
        name=beer_to_edit.name,
        type=beer_to_edit.type,
        version=beer_to_edit.version,
        description=beer_to_edit.description
    )
    if edit_form.validate_on_submit():
        beer_to_edit.name = edit_form.name.data
        beer_to_edit.type = edit_form.type.data
        beer_to_edit.version = edit_form.version.data
        beer_to_edit.description = edit_form.description.data
        db.session.commit()
        return redirect(url_for("admin_edit_beer_page"))

    return render_template("admin-form.html", form=edit_form)


@app.route('/admin-delete-beer-page')
@admin_only
def admin_delete_beer_page():
    beers = Beer.query.all()
    return render_template("admin-delete-beer-page.html", beers=beers)


@app.route("/admin-delete-beer/<int:beer_id>")
@admin_only
def admin_delete_beer(beer_id):
    beer_to_delete = Beer.query.get(beer_id)
    db.session.delete(beer_to_delete)
    db.session.commit()
    return redirect(url_for('admin_delete_beer_page'))


@app.route('/admin-edit-review-page')
@admin_only
def admin_edit_review_page():
    reviews = Review.query.all()
    return render_template("admin-edit-review-page.html", reviews=reviews)


@app.route("/admin-edit-review/<int:review_id>", methods=['GET', 'POST'])
@admin_only
def admin_edit_review(review_id):
    review_to_edit = Review.query.get(review_id)
    edit_form = ReviewForm(
        mousse=review_to_edit.mousse,
        couleur=review_to_edit.couleur,
        transparence=review_to_edit.transparence,
        douceur=review_to_edit.douceur,
        amertume=review_to_edit.amertume,
        acidite=review_to_edit.acidite,
        rondeur=review_to_edit.rondeur,
        gushing=review_to_edit.gushing,
        alcoolique=review_to_edit.alcoolique,
        ethere=review_to_edit.ethere,
        fruite=review_to_edit.fruite,
        floral=review_to_edit.floral,
        houblonne=review_to_edit.houblonne,
        resineux=review_to_edit.resineux,
        noix=review_to_edit.noix,
        herbeux=review_to_edit.herbeux,
        cereales=review_to_edit.cereales,
        caramel=review_to_edit.caramel,
        brule=review_to_edit.brule,
        score=review_to_edit.score
    )
    if edit_form.validate_on_submit():
        review_to_edit.mousse = edit_form.mousse.data
        review_to_edit.couleur = edit_form.couleur.data
        review_to_edit.transparence = edit_form.transparence.data
        review_to_edit.douceur = edit_form.douceur.data
        review_to_edit.amertume = edit_form.amertume.data
        review_to_edit.acidite = edit_form.acidite.data
        review_to_edit.rondeur = edit_form.rondeur.data
        review_to_edit.gushing = edit_form.gushing.data
        review_to_edit.alcoolique = edit_form.alcoolique.data
        review_to_edit.ethere = edit_form.ethere.data
        review_to_edit.fruite = edit_form.fruite.data
        review_to_edit.floral = edit_form.floral.data
        review_to_edit.houblonne = edit_form.houblonne.data
        review_to_edit.resineux = edit_form.resineux.data
        review_to_edit.noix = edit_form.noix.data
        review_to_edit.herbeux = edit_form.herbeux.data
        review_to_edit.cereales = edit_form.cereales.data
        review_to_edit.caramel = edit_form.caramel.data
        review_to_edit.brule = edit_form.brule.data
        review_to_edit.score = edit_form.score.data

        beer_id = review_to_edit.reviews_beer.id
        beer_to_update = Beer.query.get(beer_id)
        all_reviews = beer_to_update.reviews
        recalculate_beer(beer_to_update, all_reviews)

        db.session.commit()
        return redirect(url_for("admin_edit_review_page"))

    return render_template("admin-form.html", form=edit_form)


@app.route('/admin-delete-review-page')
@admin_only
def admin_delete_review_page():
    reviews = Review.query.all()
    return render_template("admin-delete-review-page.html", reviews=reviews)


@app.route("/admin-delete-review/<int:review_id>")
@admin_only
def admin_delete_review(review_id):
    review_to_delete = Review.query.get(review_id)
    db.session.delete(review_to_delete)
    db.session.commit()
    beer_id = review_to_delete.reviews_beer.id
    beer_to_update = Beer.query.get(beer_id)
    all_reviews = beer_to_update.reviews
    recalculate_beer(beer_to_update, all_reviews)
    return redirect(url_for('admin_delete_review_page'))


# REVIEWS
def get_avg(list):
    sum = 0
    i = 0
    for item in list:
        try:
            sum += item
        except TypeError:
            pass
        else:
            i += 1
    if i == 0:
        avg = 0
    else:
        avg = sum / i
    return avg


def recalculate_beer(beer_to_be_reviewed, all_reviews):
    mousse_list = [review.mousse for review in all_reviews]
    mousse_avg = get_avg(mousse_list)
    beer_to_be_reviewed.mousse = mousse_avg

    couleur_list = [review.couleur for review in all_reviews]
    couleur_avg = get_avg(couleur_list)
    beer_to_be_reviewed.couleur = couleur_avg
    print(couleur_avg)

    transparence_list = [review.transparence for review in all_reviews]
    transparence_avg = get_avg(transparence_list)
    beer_to_be_reviewed.transparence = transparence_avg

    douceur_list = [review.douceur for review in all_reviews]
    douceur_avg = get_avg(douceur_list)
    beer_to_be_reviewed.douceur = douceur_avg

    amertume_list = [review.amertume for review in all_reviews]
    amertume_avg = get_avg(amertume_list)
    beer_to_be_reviewed.amertume = amertume_avg

    acidite_list = [review.acidite for review in all_reviews]
    acidite_avg = get_avg(acidite_list)
    beer_to_be_reviewed.acidite = acidite_avg

    rondeur_list = [review.rondeur for review in all_reviews]
    rondeur_avg = get_avg(rondeur_list)
    beer_to_be_reviewed.rondeur = rondeur_avg

    gushing_list = [review.gushing for review in all_reviews]
    gushing_avg = get_avg(gushing_list)
    beer_to_be_reviewed.gushing = gushing_avg

    alcoolique_list = [review.alcoolique for review in all_reviews]
    alcoolique_avg = get_avg(alcoolique_list)
    beer_to_be_reviewed.alcoolique = alcoolique_avg

    ethere_list = [review.ethere for review in all_reviews]
    ethere_avg = get_avg(ethere_list)
    beer_to_be_reviewed.ethere = ethere_avg

    fruite_list = [review.fruite for review in all_reviews]
    fruite_avg = get_avg(fruite_list)
    beer_to_be_reviewed.fruite = fruite_avg

    floral_list = [review.floral for review in all_reviews]
    floral_avg = get_avg(floral_list)
    beer_to_be_reviewed.floral = floral_avg

    houblonne_list = [review.houblonne for review in all_reviews]
    houblonne_avg = get_avg(houblonne_list)
    beer_to_be_reviewed.houblonne = houblonne_avg

    resineux_list = [review.resineux for review in all_reviews]
    resineux_avg = get_avg(resineux_list)
    beer_to_be_reviewed.resineux = resineux_avg

    noix_list = [review.noix for review in all_reviews]
    noix_avg = get_avg(noix_list)
    beer_to_be_reviewed.noix = noix_avg

    herbeux_list = [review.herbeux for review in all_reviews]
    herbeux_avg = get_avg(herbeux_list)
    beer_to_be_reviewed.herbeux = herbeux_avg

    cereales_list = [review.cereales for review in all_reviews]
    cereales_avg = get_avg(cereales_list)
    beer_to_be_reviewed.cereales = cereales_avg

    caramel_list = [review.caramel for review in all_reviews]
    caramel_avg = get_avg(caramel_list)
    beer_to_be_reviewed.caramel = caramel_avg

    brule_list = [review.brule for review in all_reviews]
    brule_avg = get_avg(brule_list)
    beer_to_be_reviewed.brule = brule_avg

    score_list = [review.score for review in all_reviews]
    score_avg = get_avg(score_list)
    beer_to_be_reviewed.score = round(score_avg, 1)

    db.session.commit()


@app.route("/review/<int:beer_id>", methods=['GET', 'POST'])
def review(beer_id):
    if not current_user.is_authenticated:
        flash("Vous devez vous identifier pour remplir une fiche de dégustation.")
        return redirect(url_for("login"))
    beer_to_be_reviewed = Beer.query.get(beer_id)
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(

            reviews_beer=beer_to_be_reviewed,
            review_author=current_user,

            mousse=form.mousse.data,
            couleur=form.couleur.data,
            transparence=form.transparence.data,
            douceur=form.douceur.data,
            amertume=form.amertume.data,
            acidite=form.acidite.data,
            rondeur=form.rondeur.data,
            gushing=form.gushing.data,

            alcoolique=form.alcoolique.data,
            ethere=form.ethere.data,
            fruite=form.fruite.data,
            floral=form.floral.data,
            houblonne=form.houblonne.data,
            resineux=form.resineux.data,
            noix=form.noix.data,
            herbeux=form.herbeux.data,
            cereales=form.cereales.data,
            caramel=form.caramel.data,
            brule=form.brule.data,

            score=form.score.data
        )

        db.session.add(new_review)
        db.session.commit()

        beer_to_be_reviewed = Beer.query.get(beer_id)
        all_reviews = beer_to_be_reviewed.reviews

        recalculate_beer(beer_to_be_reviewed, all_reviews)

        return redirect(url_for("beer", beer_id=beer_id))
    return render_template("review-beer.html", form=form, beer=beer_to_be_reviewed)


@app.route("/review-edit/<int:beer_id>/<int:review_id>", methods=['GET', 'POST'])
def review_edit(beer_id, review_id):
    beer_to_be_reviewed = Beer.query.get(beer_id)
    review_to_edit = Review.query.get(review_id)
    form = ReviewForm(
        mousse=review_to_edit.mousse,
        couleur=review_to_edit.couleur,
        transparence=review_to_edit.transparence,
        douceur=review_to_edit.douceur,
        amertume=review_to_edit.amertume,
        acidite=review_to_edit.acidite,
        rondeur=review_to_edit.rondeur,
        gushing=review_to_edit.gushing,
        alcoolique=review_to_edit.alcoolique,
        ethere=review_to_edit.ethere,
        fruite=review_to_edit.fruite,
        floral=review_to_edit.floral,
        houblonne=review_to_edit.houblonne,
        resineux=review_to_edit.resineux,
        noix=review_to_edit.noix,
        herbeux=review_to_edit.herbeux,
        cereales=review_to_edit.cereales,
        caramel=review_to_edit.caramel,
        brule=review_to_edit.brule,
        score=review_to_edit.score
    )
    if form.validate_on_submit():
        review_to_edit.mousse = form.mousse.data
        review_to_edit.couleur = form.couleur.data
        review_to_edit.transparence = form.transparence.data
        review_to_edit.douceur = form.douceur.data
        review_to_edit.amertume = form.amertume.data
        review_to_edit.acidite = form.acidite.data
        review_to_edit.rondeur = form.rondeur.data
        review_to_edit.gushing = form.gushing.data

        review_to_edit.alcoolique = form.alcoolique.data
        review_to_edit.ethere = form.ethere.data
        review_to_edit.fruite = form.fruite.data
        review_to_edit.floral = form.floral.data
        review_to_edit.houblonne = form.houblonne.data
        review_to_edit.resineux = form.resineux.data
        review_to_edit.noix = form.noix.data
        review_to_edit.herbeux = form.herbeux.data
        review_to_edit.cereales = form.cereales.data
        review_to_edit.caramel = form.caramel.data
        review_to_edit.brule = form.brule.data

        review_to_edit.score = form.score.data

        db.session.commit()

        beer_to_be_reviewed = Beer.query.get(beer_id)
        all_reviews = beer_to_be_reviewed.reviews

        recalculate_beer(beer_to_be_reviewed, all_reviews)

        return redirect(url_for("beer", beer_id=beer_id))
    return render_template("review-beer.html", form=form, beer=beer_to_be_reviewed)


@app.route("/add-comment/<int:beer_id>", methods=['GET', 'POST'])
def add_comment(beer_id):
    if not current_user.is_authenticated:
        flash("Vous devez vous identifier pour commenter.")
        return redirect(url_for("login"))
    beer_to_be_commented = Beer.query.get(beer_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            comments_beer=beer_to_be_commented,
            comment_author=current_user,
            text=form.comment_text.data
        )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("beer", beer_id=beer_id))
    return render_template("comment-beer.html", form=form, beer=beer_to_be_commented)


@app.route("/edit-comment/<int:comment_id>", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment_to_edit = Comment.query.get(comment_id)
    comment_beer = comment_to_edit.comments_beer
    form = CommentForm(
        comment_text=comment_to_edit.text
    )
    if form.validate_on_submit():
        comment_to_edit.text = form.comment_text.data
        db.session.commit()
        return redirect(url_for("beer", beer_id=comment_beer.id))
    return render_template("comment-beer.html", form=form, beer=comment_beer)


@app.route("/delete-comment/<int:comment_id>", methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    comment_beer = comment_to_delete.comments_beer
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("beer", beer_id=comment_beer.id))


@app.route("/info", methods=['GET', 'POST'])
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)


# TODO : Ecrire page d'info, formulaire contact
# TODO : Commander : renvoie vers formulaire contact?
# TODO : Bouton faire un don sur toutes les pages (nav bar avec icone kdo) : renvoie vers page avec infos virement et QR code