#Flask libraries
from flask import Flask, request, make_response, redirect, render_template, session, url_for
from flask_login import login_required, current_user

#Flash libraries
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
import unittest

#import classes and functions
from app.forms import loginForm
from app import create_app
from app.firestore_service import get_users, get_todos

#Gets the app from the __ini__ file
app = create_app()

#Make flask testing
@app.cli.command()
def test():
    #Tests are inside the folder tests 
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

#Error when the server fails
@app.errorhandler(500)
def server_problem(error):
    return render_template('500.html', error=error)

#Error when page doesn't exist
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def index():
    #Get the user ip
    user_ip = request.remote_addr

    #redirect to another route
    response = make_response(redirect('/hi'))
    #Save the cookie with the name user_ip
    session['user_ip'] = user_ip

    return response

#Create a function that return hello world, and a decorator with the function route that specify the route
#where the app will run
@app.route('/hi', methods=['GET'])

#Protect the route
@login_required
def hello():
    #Get the Cookie from the browser
    user_ip = session.get('user_ip')
    username = current_user.id

    #Save all the parameters
    parameter = {
        'user_ip':user_ip,
        'todos':get_todos(username),
        'username': username
    }

    return render_template('hello.html', **parameter)

