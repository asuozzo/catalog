from models import Base, User, Book, RegistrationForm
from flask import Flask, jsonify, session, request, render_template, url_for, redirect, flash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth
from wtforms import Form, StringField, PasswordField, validators
from functools import wraps

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///library.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()
app = Flask(__name__)


def check_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" in  session:
            return f(*args,**kwargs)
        else:
            flash("whoops, you need to be logged in to do that!")
            return redirect(url_for("login"))
    return wrapper

def check_object_owner(username):
    if username == session["username"]:
        return True
    else:
        return False

def verify_password(username, password):
    user = dbsession.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return True


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        if verify_password(username,password):
            session['username'] = username
            flash("You're now logged in")
            return redirect(url_for("showAllBooks"))
        else:
            error = "Sorry, that login doesn't look quite right"
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for("showAllBooks"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username=form.username.data
        email=form.email.data
        if dbsession.query(User).filter_by(username=username).first():
            error = "Username already exists"
            return render_template('signup.html', form=form, error=error)
        if dbsession.query(User).filter_by(email=email).first():
            error = "A user with that email is already registered"
            return render_template('signup.html', form=form, error=error)
        if form.validate():
            newUser=User(username=form.username.data,
                      email=form.email.data)
            password=form.password.data
            newUser.hash_password(password)
            dbsession.add(newUser)
            dbsession.commit()
            session['username'] = username
            flash("Welcome! Thanks for registering!")
            return redirect(url_for("showAllBooks"))
    return render_template('signup.html', form=form)


@app.route('/')
@app.route('/library/')
def showAllBooks():
    books = dbsession.query(Book).all()
    genres = [b.genre for b in dbsession.query(Book.genre).distinct()]
    return render_template('home.html', books=books,genres=genres)


@app.route("/library/<book_genre>")
def showGenreBooks(book_genre):
    books = dbsession.query(Book).filter_by(genre=book_genre)
    return render_template('genre.html', genre=book_genre,books=books)


@app.route('/library/<int:book_id>/')
def showBook(book_id):
    book = dbsession.query(Book).filter_by(id=book_id).one()
    user = dbsession.query(User).filter_by(id=book.user_id).one()
    username = user.username
    return render_template('item.html',book=book,username=username)


@app.route('/library/<int:book_id>/edit', methods=['GET','POST'])
@check_login
def editBook(book_id):
    book = dbsession.query(Book).filter_by(id=book_id).one()
    user = dbsession.query(User).filter_by(username=session['username']).one()
    if user.id == book.user_id:
        if request.method == 'POST':
            book.title = request.form['title']
            book.author = request.form['author']
            book.description = request.form['description']
            book.genre = request.form['genre']
            dbsession.commit()
            flash("Item successfully edited")
            return redirect(url_for("showBook", book_id=book.id))
        return render_template('edit.html',book=book)
    else:
        flash("Sorry, you can't edit a book you didn't create.")
        return redirect(url_for("showBook", book_id=book.id))


@app.route('/library/<int:book_id>/delete', methods=['GET','POST'])
@check_login
def deleteBook(book_id):
    book = dbsession.query(Book).filter_by(id=book_id).one()
    user = dbsession.query(User).filter_by(username=session['username']).one()
    if user.id == book.user_id:
        if request.method == 'POST':
            user = dbsession.query(User).filter_by(username=session['username']).one()
            dbsession.delete(book)
            dbsession.commit()
            flash("Item successfully deleted")
            return redirect(url_for("showAllBooks"))
        return render_template('delete.html',book=book)
    else:
        flash("Sorry, you can't delete a book you didn't create.")
        return redirect(url_for("showBook", book_id=book.id))



@app.route('/library/add', methods = ['GET','POST'])
@check_login
def addBook():
    if request.method == 'POST':
        newBook = Book(title=request.form['title'],
                       author=request.form['author'],
                       description=request.form['description'],
                       genre=request.form['genre'])
        user = dbsession.query(User).filter_by(username=session["username"]).one()
        newBook.user_id = user.id
        dbsession.add(newBook)
        dbsession.commit()
        flash("Success!")
        return redirect(url_for("showAllBooks"))
    return render_template('additem.html')


@app.route('/library/json')
def jsonifyBooks():
    books = dbsession.query(Book).all()
    return jsonify(books = [book.serialize for book in books])


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)