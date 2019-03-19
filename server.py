from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, NoteEditForm
from tools import to_hash, password_exists, get_date

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=False, nullable=False)
    administrator = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %i %s %s>' % (self.id, self.login, self.password_hash)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=False, nullable=False)
    text = db.Column(db.String(1350), unique=False, nullable=True)
    date = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Note %i %s %s %s %i>' % (self.id, self.title, self.text, self.date, self.user_id)


db.create_all()
# user = User(login='root', password_hash=to_hash('toor'), administrator=1)
# db.session.add(user)
# db.session.commit()
# note = Note(title='6', text='', date='18.03.2021', user_id=1)
# db.session.add(note)
# db.session.commit()


def logged():
    if 'login' not in session:
        eq = User.query.filter_by(id=session['user_id']).first()
        if session['login'] != eq.login:
            return False
    return True


@app.route('/')
@app.route('/index')
def index():
    if not logged():
        return redirect('/init/login')
    user = User.query.filter_by(login=session['login']).first()
    notes = Note.query.filter_by(user_id=user.id).all()[::-1]
    ln = len(notes)
    if ln == 1:
        separation = 1
    elif ln > 8:
        separation = 3
    else:
        separation = 2
    return render_template('index.html', user=user, notes=notes, len=ln, sep=separation)


@app.route('/init/<mod>', methods=['POST', 'GET'])
def init(mod):
    # quit last user
    try:
        session.pop('login')
        session.pop('user_id')
    except KeyError:
        pass

    # authorization
    if mod == 'login':
        form = LoginForm()
        if form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            login_compared = User.query.filter_by(login=login).first()
            # if success
            if login_compared and password_exists(login_compared.password_hash, password):
                session['login'] = login
                session['user_id'] = login_compared.id
                return redirect('/')

    # registration
    elif mod == 'register':
        form = RegistrationForm()
        if form.validate_on_submit():
            login = form.login.data
            password_hash = to_hash(form.password.data)
            exists = bool(User.query.filter_by(login=login).first())
            if exists:
                return redirect('/init/register')
            # register user
            user = User(login=login, password_hash=password_hash, administrator=0)
            db.session.add(user)
            db.session.commit()
            return redirect('/init/login')

    return render_template('init.html', form=form)


@app.route('/note/<id>', methods=['GET', 'POST'])
def note(id):
    if not logged():
        return redirect('/init/login')
    try:
        user = User.query.filter_by(login=session['login']).first()
        form = NoteEditForm()
        note_content = Note.query.filter_by(id=int(id)).first()
        if form.validate_on_submit():
            note_content.text = form.text.data
            note_content.title = form.title.data
            print(request.form['data'])
            note_content.date = request.form['data']
            db.session.commit()
            return redirect('/index')
        # existing content in the note
        form.text.data = note_content.text
        form.title.data = note_content.title

    except AttributeError:
        return '''<title>404 Error</title>
                       <h1>404 ERROR</h1>'''
    return render_template('note.html', user=user, form=form, date=get_date()[0])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
