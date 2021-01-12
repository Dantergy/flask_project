from flask_testing import TestCase
from flask import current_app, url_for

from main import app

class MainTest(TestCase):
    def create_app(self):
        #Setup the test
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        return app
    
    #Check if the app exists
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    #Check if the app is in testing mode
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])
    
    #Check if the index redirects to hello funcion
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('hello'))

    #Check if hello returns a 200
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)
    
    #Check hello POST petition
    def test_hello_post(self):
        response = self.client.post(url_for('hello'))
        self.assertTrue(response.status_code, 405)
    
    #Test Blueprint
    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)
    
    #Test Blueprint login
    def test_auth_login(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    #Test login is rendering
    def test_auth_login_rendered(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        test_form = {
            'username':'test',
            'password':'test'
        }
        response = self.client.post(url_for('auth.login'), data = test_form)
        self.assertRedirects(response, url_for('index'))