from flask import Blueprint, render_template, request, flash, redirect, url_for
from merchandise_inventory.forms import UserLoginForm, UserSigninForm
from merchandise_inventory.models import User, db, check_password_hash

# Imports for flask login
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth',__name__,template_folder='auth_templates')

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User( first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form Inputs')

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET','POST'])
def signin():
    form = UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first() 
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You have successfully logged in: via email/password', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    
    except:
        raise Exception('Invalid Form Data: Please Check Your Form!')
    return render_template('signin.html', form = form)    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))