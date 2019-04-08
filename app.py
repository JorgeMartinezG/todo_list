from flask import (
    Flask,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models import User, Item

from functools import wraps

from mongoengine import connect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'someRandomStringPleaseChange'

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

@app.route('/item', methods=['POST'])
def register_item():
	item = request.values.get('email') 


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Render register template.
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.values.get('email')
        pw = request.values.get('password')

        # Get user from database.
        user = User.objects(mail=email)
        if len(user) != 1:
        	abort(401)
        if user[0].password == pw:
        	# Work only with user id from email.
        	session['user'] = email.split('@')[0]


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    # Render register template.
    if request.method == 'GET':
        return render_template('register.html')

    # Insert user into database.
    # TODO: Check for previous email created.
    if request.method == 'POST':
        email = request.values.get('email')
        pw = request.values.get('password')

        user = User(email, pw)
        user.save()

        return 'Success!'

# @app.route('/get')
# def get():

if __name__ == '__main__':
	# Create database
    connect('todo')
    app.run()