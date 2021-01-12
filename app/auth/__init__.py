from flask import Blueprint

#Create a blueprint with a prefix, that means all the routes that begins 
# with /auth will be redirect to this prefix
auth = Blueprint('auth',__name__, url_prefix='/auth')

#Import the views
from . import views 