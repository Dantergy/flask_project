from flask import render_template, session, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import loginForm
#import from the present directory
from . import auth
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel

#Create the views
@auth.route('/login', methods=['GET','POST'])
def login():

    login_form = loginForm()

    parameter = {
        'login_form': loginForm()
    }

    #If the user is logged in, they won't have access to the login page 
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    #Add the username to the session, we use validate on submit, that function validates the form 
    if login_form.validate_on_submit():
        #Get username
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            #Get the user password
            password_db = user_doc.to_dict()['password']

            #If the password coincides with the ones in the DB
            if check_password_hash(password_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash('Nice to see you!')
                redirect(url_for('hello'))
            else:
                flash('Wrong username/password')
        else:
            flash('The user does not exists')
    
        return redirect(url_for('index'))

    return render_template('login.html', **parameter)

#Sign up route
@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = loginForm()
    parameter = {
        'signup_form': signup_form
    }

    #Validate the form
    if signup_form.validate_on_submit():
        #Get the data
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        #If the user does not exists
        if user_doc.to_dict() is None:
            #Hash the password
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)

            flash('Welcome!')

            return redirect(url_for('index'))
            
        else:
            flash('The user already exists.')

    return render_template('signup.html', **parameter)


#The decorator login required checks if there is a user logged in 
@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('We will miss you...')

    return redirect(url_for('auth.login'))




