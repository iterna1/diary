from flask import Flask, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, NoteEditForm, NoteCreateForm, AddDelForm
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
    note_sequence_by_date = db.Column(db.Boolean, default=True, nullable=False)
    administrator = db.Column(db.Boolean, nullable=False)

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


def logged():
    if 'login' not in session:
        return False
    else:
        eq = User.query.filter_by(id=session['user_id']).first()
        if eq is None or session['login'] != eq.login:
            return False
    return True


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
        if not logged():
            return redirect('/init/login')

        user = User.query.filter_by(login=session['login']).first()
        notes = Note.query.filter_by(user_id=user.id)

        if user.note_sequence_by_date:
            filt = Note.id
        else:
            filt = Note.title

        form = AddDelForm()
        if form.validate_on_submit():
            if form.plus.data:
                return redirect('/note/new')
            elif form.sort.data:
                if user.note_sequence_by_date:
                    filt = Note.title
                    user.note_sequence_by_date = False
                else:
                    filt = Note.id
                    user.note_sequence_by_date = True  # like date bcs id is primary key
        db.session.commit()

        ln = notes.count()
        if ln == 1:
            separation = 1
        elif ln > 8:
            separation = 3
        else:
            separation = 2
        return render_template('index.html', user=user, notes=notes.order_by(filt).all(), len=ln, sep=separation, form=form)


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
            user = User(login=login, password_hash=password_hash, administrator=False)
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
        if id == 'new':
            form = NoteCreateForm()
            note_content = Note(title='untitled', user_id=user.id, date=get_date())
            if form.validate_on_submit():
                note_content.text = form.text.data
                note_content.title = form.title.data
                db.session.add(note_content)
                db.session.commit()
                return redirect('index')
            form.text.data = note_content.text
            form.title.data = note_content.title
            return render_template('note.html', user=user, form=form, date=note_content.date)

        else:
            form = NoteEditForm()
            note_content = Note.query.filter_by(id=int(id)).first()
            if form.validate_on_submit():
                note_content.text = form.text.data
                note_content.title = form.title.data
                db.session.commit()
                return redirect('/index')
            # existing content in the note
            form.text.data = note_content.text
            form.title.data = note_content.title

    except AttributeError and ValueError:
        return redirect('/not_found')

    return render_template('note.html', user=user, form=form, date=note_content.date)


@app.route('/delete/<id>')
def delete(id):
    if not logged():
        return redirect('/init/login')
    try:
        note = Note.query.filter_by(id=id).first()
        db.session.delete(note)
        db.session.commit()
    except Exception as e:
        return redirect('/not_found')
    return redirect('/')


@app.route('/not_found')
def not_found():
    return '''<title>404 Error</title><h1>404 ERROR</h1>'''


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
