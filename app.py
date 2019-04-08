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

@app.route('/list', methods=['GET'])
def list():
    # Get list of items from database for any given user.
    user_obj = User.objects(mail=session['user']).first()

    # Get list of items from database.
    items = Item.objects(user=user_obj.id).to_json()

    # Remove this when you have included items
    items = [{'name': i.mail} for i in User.objects()] 

    context = {
        'items': items,
        'user': user_obj.mail.split('@')[0]

    }

    return render_template('list.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Render register template.
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.values.get('email')
        pw = request.values.get('password')

        # Get user from database.
        users = User.objects(mail=email)
        if len(users) != 1:
            abort(401)

        user = users[0]
        if user.password == pw:
            session['user'] = user.mail
            return 'Success!'

        return 'error'


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

if __name__ == '__main__':
    connect('todo')
    app.run()