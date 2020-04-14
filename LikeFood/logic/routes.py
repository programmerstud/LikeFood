#!/usr/local/bin/python
# coding: utf-8
from flask import render_template, request, flash, abort, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from wtforms.fields import SubmitField
from werkzeug.security import check_password_hash, generate_password_hash
import random
import string

from logic import app, db
from logic.models import User, Recipe, Category, user_like_recipe, user_schema


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    login = StringField('login', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password_repeat = PasswordField('password_repeat', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = StringField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    new_password_repeat = PasswordField('new_password_repeat', validators=[DataRequired()])

""""""
class AddRecipeForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    category_id = StringField('category_id', validators=[DataRequired()])
    image = StringField('image', validators=[DataRequired()])
    recipe_text = TextAreaField('recipe_text', validators=[DataRequired()])
""""""

class AddAuthorForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods = ['GET', 'POST'])
def mainPage(page = 1):
    if current_user.is_authenticated:
        per_page = 2
        is_author = False;
        if current_user.role == "Author":
            is_author = "True"
        recipes = Recipe.query.order_by(Recipe.id).paginate(page, per_page, error_out=False)
        return render_template('index.html', recipes=recipes, is_author=is_author)
    else:
        return login()


@app.route('/top_authors', methods=['GET', 'POST'])
@login_required
def raitingPage():
    if current_user.role == "Reader" or current_user.role == "Author":
        return topPage()
    else:
        return topPage()


@app.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def newRecipePage():
    if current_user.role == "Author":
        return createRecipePage()
    else:
        return mainPage()



def login():
    form = LoginForm()
    login = form.login.data
    password = form.password.data
    if form.validate_on_submit():
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.password == password:
                login_user(user)
                return redirect(url_for('mainPage'))
            else:
                flash('Логин или пароль введены неверно')
        else:
            flash('Пожалуйста, заполните поля логина и пароля!')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    login = form.login.data
    password = form.password.data
    password_repeat = form.password_repeat.data
    if form.validate_on_submit():
        if not (login or password or password_repeat):
            flash('Пожалуйста, заполните все поля!')
        elif password != password_repeat:
            flash('Пароли не совпадают!')
        else:
            if (not(7 < len(password) < 20) or (password.isdigit() or password.isalpha())):
                flash('Пароль не соответствует правилам безопасности!')
            else:
                user = User.query.filter_by(login=login).first()
                if user is not None:
                    flash('Пользователь с таким логином уже существует!')
                else:
                    new_user = User(login=login, password=password,role="Reader")
                    db.session.add(new_user)
                    db.session.commit()

                    return redirect(url_for('mainPage'))
    else:
        if login:
            flash("Данный логин не допустим!")
    return render_template('registration.html', form = form)


@app.route('/сhange_password', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    old_password = form.old_password.data
    new_password = form.new_password.data
    new_password_repeat = form.new_password_repeat.data
    if form.validate_on_submit():
        if not (current_user.password == old_password):
            flash('Введенный старый пароль не верен!')
        elif new_password != new_password_repeat:
            flash('Новый и введенный повторно пароли не совпадают!')
        else:
            if (not(7 < len(new_password) < 20) or (new_password.isdigit() or new_password.isalpha())):
                flash('Пароль не соответствует правилам безопасности!')
            else:
                user = User.query.filter_by(login=current_user.login).first()
                user.password = new_password
                db.session.add(user)
                db.session.commit()
                flash("Вы успешно сменили пароль!")
    return render_template('change_password.html', form = form)


@app.route('/author_registration', methods=['GET', 'POST'])
@login_required
def addAuthor():
    form = AddAuthorForm()
    login = form.login.data
    str = ""
    if form.validate_on_submit():
        if not (login):
            flash('Пожалуйста, заполните поле логина!')
        elif User.query.filter_by(login=login).first() is not None:
            flash('Пользователь с таким логином уже существует!')
        else:
            password = gen(method=["uppercase", "lowercase", "digits"])
            new_user = User(login=login, password=password,role="Author")
            db.session.add(new_user)
            db.session.commit()
            str += "Информация для авторизации: \n Логин: " + login + "\n Пароль: " + password
    return render_template('author_registration.html', form = form, content = str)


def gen(length=8, method=["lowercase", "uppercase", "digits", "punctuation"]):
    pwd = []
    for i in range(length):
        choice = random.choice(method)
        if choice == "lowercase":
            pwd.append(random.choice(string.ascii_lowercase))
        if choice == "uppercase":
            pwd.append(random.choice(string.ascii_uppercase))
        if choice == "digits":
            pwd.append(random.choice(string.digits))
        if choice == "punctuation":
            pwd.append(random.choice(string.punctuation))
        if choice == "string":
            pwd.append(random.choice(string.punctuation))
    random.shuffle(pwd)
    return ''.join(pwd)

'''
@app.route('/<int:page>',methods = ['GET', 'POST'])
@login_required
def allRecipePage(page = 1):
    per_page = 1
    recipes = Recipe.query.order_by(Recipe.id).paginate(page,per_page,error_out=False)
    return render_template('index.html',recipes=recipes)


@login_required
def allRecipePageAuthor():
    return render_template('index_for_authors.html')
'''

@login_required
def topPage():
    is_admin = False;
    if current_user.role == "Admin":
        is_admin = "True"
    rait = show_top_raiting()
    return render_template('top_page.html', raiting = rait, is_admin=is_admin)


def show_top_raiting():
    authors = User.query.filter_by(role='Author').all()
    raiting = {}
    for author in authors:
        count = 0
        recipes = Recipe.query.filter_by(author_id=author.id).all()
        for recipe in recipes:
            count += db.session.query(User).join(User.user_like_recipe).filter(Recipe.id==recipe.id).count()
        raiting[author.login]=count
    list_raiting = list(raiting.items())
    list_raiting.sort(key=lambda i: i[1], reverse=True)
    return list_raiting


def createRecipePage():
    form = AddRecipeForm()
    title = form.title.data
    category_id = form.category_id.data
    image = form.image.data
    recipe_text = form.recipe_text.data
    if form.validate_on_submit():
        if not (title or category_id or image or recipe_text):
            flash('Пожалуйста, заполните все поля!')
        else:
            author_id = current_user.id
            new_recipe = Recipe(title=title, category_id=category_id, image=image, recipe_text=recipe_text,author_id=author_id )
            db.session.add(new_recipe)
            db.session.commit()

        return redirect(url_for('mainPage'))
    else:
        if title:
            flash("Данный логин не допустим!")
    return render_template('new_recipe_page.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mainPage'))

if __name__=="__main__":
    app.run(debug=True)