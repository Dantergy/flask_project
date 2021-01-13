import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Create a credential to set the Aplication default
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    """ This function get all the users
    in firestore
    """
    return db.collection('users').get()

def get_user(user_id):
    """ This function get one user
    in firestore
    """
    return db.collection('users').document(user_id).get()

def get_todos(user_id):
    """ 
    This function gets the users todo
     """
    return db.collection('users').document(user_id).collection('todos').get()

def user_put(user_data):
    """ 
    This function creates a new user in the DB
     """
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({
        'password': user_data.password
    })

def todo_put(user_id, description):
    """ 
    This function creates todo list for the user, requires the user id due 
    the todo collections are inside the user's document
     """
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    todos_collection_ref.add({
        'description': description,
        'done': False
    })

def delete_todo(user_id, todo_id):
    """ 
    This function deletes the todos for a user based on the todo id
     """
    todo_ref = db.document(f'users/{user_id}/todos/{todo_id}')
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    """ 
    This function changes the state of the task
     """
    #Parse done to boolean
    todo_done = not bool(done)
    todo_ref = db.document(f'users/{user_id}/todos/{todo_id}')
    todo_ref.update({'done': todo_done})

