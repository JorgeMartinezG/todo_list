from flask import Flask
from models import User

from mongoengine import connect

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/register')
def register():
    user = User('jorge', 'martinez')
    user.save()

# @app.route('/get')
# def get():

if __name__ == '__main__':
    connect('testdb')
    app.run()