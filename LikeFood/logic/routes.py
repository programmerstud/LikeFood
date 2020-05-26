#!/usr/local/bin/python
# coding: utf-8
from flask import render_template, request, flash, abort, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from wtforms.fields import SubmitField
from werkzeug.security import check_password_hash, generate_password_hash
from flask import send_from_directory
import os
import random
import string
from werkzeug.utils import secure_filename
from logic import app
from logic.LikeFood import likeFood


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

class AddRecipeForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    image = FileField('image', validators=[DataRequired()])
    recipe_text = TextAreaField('recipe_text', validators=[DataRequired()])

class AddAuthorForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])

class Filtration(FlaskForm):
    name = StringField('name')
    login = StringField('login')
    author = BooleanField('author')
    sort_choices = [('like', 'По рейтингу'),
                      ('new', 'По новизне')]
    filter_choices = [('1', 'Первые блюда'),
                    ('2', 'Вторые блюда'),
                    ('3', 'Салаты'),
                    ('4', 'Закуски'),
                    ('5', 'Десерты')]
    sort = SelectField(u'Сортировка', choices=sort_choices)
    filter = SelectMultipleField(u'Фильтрация', choices=filter_choices)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods = ['GET', 'POST'])
def main_page(page = 1, name=None, log = None, author=None, filter=None, sort=None):
    if likeFood.current_user_is_authenticated():
        form = Filtration()
        per_page = 9
        is_author = False
        if likeFood.current_user_role() == "Author":
            is_author = "True"
        if form.validate_on_submit():
            return redirect(url_for('main_page', page=1, name=form.name.data, log=form.login.data, author=form.author.data, filter=form.filter.data, sort=form.sort.data))
        recipes = likeFood.get_filtered_recipes(request.args.get('name'), request.args.get('log'), str(request.args.get('author')), request.args.get('filter'), request.args.get('sort'))
        return render_template('index.html', form = form, name=request.args.get('name'), log = request.args.get('log'), author = request.args.get('author'), filter = request.args.get('filter'), sort = request.args.get('sort'),  page=1, recipes= recipes.paginate(page, per_page, error_out=False),
                               names_authors=likeFood.show_recipes(recipes, 'authors')[(page-1)*per_page:(page-1)*per_page+per_page+1], likes=likeFood.show_recipes(recipes, 'likes')[(page-1)*per_page:(page-1)*per_page+per_page+1], is_author=is_author)
    else:
        return login()


@app.route('/top_authors', methods=['GET', 'POST'])
@login_required
def raiting_page():
    is_admin = False
    if likeFood.current_user_role() == "Admin":
        is_admin = "True"
    return render_template('top_page.html', raiting = likeFood.show_top_raiting(), is_admin=is_admin)


@app.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe_page():
    if current_user.role == "Author":
        return create_recipe_page()
    else:
        return main_page()

def login():
    form = LoginForm()
    login = form.login.data
    password = form.password.data
    if form.validate_on_submit():
        if login and password:
            user = likeFood.check_user(login)
            if user and user.password == password:
                likeFood.login(login)
                return redirect(url_for('main_page'))
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
                user = likeFood.check_user(login)
                if user is not None:
                    flash('Пользователь с таким логином уже существует!')
                else:
                    likeFood.register(login, password, 'Reader')

                    return redirect(url_for('main_page'))
    else:
        if login:
            flash("Данный логин не допустим!")
    return render_template('registration.html', form = form)


@app.route('/сhange_password', methods=['GET', 'POST'])
@login_required
def change_password():
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
                likeFood.change_password(login, new_password)
                flash("Вы успешно сменили пароль!")
    return render_template('change_password.html', form = form)


@app.route('/author_registration', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AddAuthorForm()
    login = form.login.data
    str = ""; l = ""; p = ""
    if form.validate_on_submit():
        if not (login):
            flash('Пожалуйста, заполните поле логина!')
        elif likeFood.check_user(login) is not None:
            flash('Пользователь с таким логином уже существует!')
        else:
            password = likeFood.gen_password(method=["uppercase", "lowercase", "digits"])
            likeFood.register(login, password, 'Author')
            str += "Информация для авторизации:"
            l += "Логин: " + login
            p += "Пароль: " + password
    return render_template('author_registration.html', form = form, content = str, login = l, password = p)


def create_recipe_page():
    form = AddRecipeForm()
    title = form.title.data
    image = form.image.data
    recipe_text = form.recipe_text.data
    categories = likeFood.show_categories()
    if form.validate_on_submit():
        category_id = request.form.get('category')
        if not (title or image or recipe_text or category_id):
            flash('Пожалуйста, заполните все поля!')
        else:
            likeFood.create_recipe(title, category_id, image, recipe_text)
        return redirect(url_for('main_page'))
    else:
        if title:
            flash("Данный логин не допустим!")
    return render_template('new_recipe_page.html', form=form, categories=categories)


@app.route('/logout')
@login_required
def logout():
    likeFood.logout()
    return redirect(url_for('main_page'))


@app.route('/recipe/<int:id>', methods=['GET', 'POST'])
@login_required
def recipe_page(id):
    recipe = likeFood.get_recipe_info(id)
    is_admin = False
    is_author = False
    if likeFood.current_user_role() == "Admin":
        is_admin = "True"
    if likeFood.current_user_role() == "Author":
        is_author = "True"
    if request.method == 'POST':
        action = request.form['submit_button']
        if action=='like':
            if likeFood.is_user_like_recipe(id):
                likeFood.delete_like_from_recipe(id)
            else:
                likeFood.add_like_to_recipe(id)
        if action=='OK':
            likeFood.delete_recipe(id)
            return redirect(url_for('main_page'))

    return render_template('recipe_page.html', raiting = likeFood.show_top_raiting(),recipe=recipe, like = likeFood.is_user_like_recipe(id), is_admin=is_admin, is_author=is_author)

if __name__=="__main__":
    app.run(debug=True)