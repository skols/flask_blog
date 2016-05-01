from flask_blog import app
from flask import render_template, redirect, url_for, session, request, flash
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
    
    if form.validate_on_submit():
        # After password has been hashed, need to change the validation
        # filter_by is like a select with a where
        author = Author.query.filter_by(
            username = form.username.data
        ).first()
        if author:
            # Checking the hashed password
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                flash("User %s logged in" % form.username.data)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    # return redirect(url_for('login_success'))
                    return redirect(url_for('index'))
            else:
                error = "Incorrect username or password"
        else:
            error = "Incorrect username or password"
    return render_template('author/login.html', form=form, error=error)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)

@app.route('/success/')
def success():
    return "Author registered!"



# @app.route('/login_success/')
# @login_required
# def login_success():
#     return "Author logged in!"

@app.route('/logout/')
@login_required
def logout():
    session.pop('username')
    session.pop('is_author')
    flash("User logged out")
    return redirect(url_for('index'))
