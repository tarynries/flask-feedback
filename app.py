"""Feedback app/routes"""

from flask import Flask, session, render_template, redirect, flash
from models import db, connect_db, User, Feedback
from werkzeug.exceptions import Unauthorized


from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()
connect_db(app)
db.create_all()

@app.route("/", methods=["GET"])
def home_page():

    return redirect ("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():

    # if "username" in session:
    #     return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.register(**data)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        #session["user_id"] = user.id
        

        #flash(f"{new_user.username} added")
        return redirect(f"/users/{user.username}")
       # return redirect ("register_user.html")

    else:
        return render_template("register_user.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    # if "username" in session:
    #     return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)

        #user = User.query.filter_by(username=name).first()

        if user:
            session['username'] = user.username
            #session["user_id"] = user.id
            return redirect(f"/users/{user.username}")

    else:
        form.username.errors = ["Bad name/password"]
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop('user_id', None)

    return redirect("/login")




@app.route("/users/<username>", methods=["GET"])
def show_user(username):


    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    print('username')

    return render_template("secret.html", user=user, form=form)



@app.route("/users/<username>/delete", methods=["GET", "POST"])
def remove_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()


    user = User.query.get(username)
    

    db.session.delete(user)
    db.session.commit()
    session.pop("username")

 

    return redirect("/register")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

  

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = form.username.data

        feedback = Feedback (title=title, content=content, username=username)

        print('feedback')

        db.session.add(feedback)
        db.session.commit()

        
        return redirect (f"/users/{feedback.username}")

    else:
        return render_template("feedback.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate.on.submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedback.html", form=form, feedback=feedback)

    


@app.route("/feedback/<int:feedback_id>/delete", methods=["GET", "POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate.on.submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")








