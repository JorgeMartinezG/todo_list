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


@app.route('/list', methods=['GET'])
def list():
    # Get list of items from database for any given user.
    user_obj = User.objects(mail=session['user']).first()

    # Get list of items from database.
    items = [{'name': i.text} for i in Item.objects(user=user_obj.id)] 

    context = {
        'items': items,
        'user': user_obj.mail.split('@')[0]

    }

    return render_template('list.html', **context)

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('user', None)

	return redirect(url_for('login'))


@app.route('/')
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

@app.route('/add', methods=['GET', 'POST'])
def add():
    # Render register template.
    if request.method == 'GET':
        return render_template('add.html')

    if request.method == 'POST':
        text = request.values.get('text')
        user_obj = User.objects(mail=session['user']).first()

        item = Item(user=user_obj.id, text=text)
        item.save()

        return 'Success!'


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