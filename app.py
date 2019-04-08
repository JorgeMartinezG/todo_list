from flask import (
    Flask,
    abort,
    render_template,
    request)

from models import User

from functools import wraps

from mongoengine import connect

app = Flask(__name__)

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
               abort(401)

            user = 'jorge'
            password = 'martinez'

            # Check database connection
            test = User.objects(mail='jorge@gmail.com')
            return f(user, *args, **kws)            
    return decorated_function


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    # Render template.
    if request.method == 'GET':
        return render_template('register.html')
    # Insert user into database.
    if request.method == 'POST':
        email = request.values.get('email')
        pw = request.values.get('password')

        user = User(email, password)
        user.save()

# @app.route('/get')
# def get():

if __name__ == '__main__':
    connect('todo-list')
    app.run()