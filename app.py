import datetime
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func, update
from dao.db import PostgresDb
from dao.orm.model import *
import os
from forms.album import AlbumForm
from forms.genre import GenreForm
from forms.login import userlogin
from forms.melody import MelodyForm
from forms.order import OrderForm
from forms.performer import PerformerForm
from forms.signup import SignUpForm
from forms.student import StudentForm
import plotly
import plotly.graph_objs as go
import json
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dao.db import PostgresDb
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "zlatakhodosjoj")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = PostgresDb()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    check = db.sqlalchemy_session.query(student.username.label('username'), student.password.label('password')).filter(student.id==user_id)
    user_check = student(id = user_id, username = check[0][0], password=check[0][1])
    return user_check

@app.route('/', methods = ['GET', 'POST'])
def index():
    error = None
    form = userlogin()
    s_users = list(db.sqlalchemy_session.query(student.username))
    users = []
    for i in range(len(s_users)):
        users.append(s_users[i][0])
    if request.method=='POST':
        if not form.validate():
            return render_template('index.html', form=form, action='')
        else:
            if form.login.data=='admin' and form.password.data=='admin':
                return redirect(url_for('admin'))
            elif (form.login.data not in users):
                return render_template('index.html', form=form, action='', error = 'Неправильний логін або пароль')
            else:
                user = db.sqlalchemy_session.query(student.password.label('password')).filter(student.username == form.login.data)
                pass_to_check = user[0][0]
                user_data = db.sqlalchemy_session.query(student.id.label('id'),
                                                        student.username.label('username'),
                                                        student.password.label('password')).filter(
                    student.username == form.login.data)
                print(user_data[0])
                user_for_login = student(id=user_data[0][0], username=user_data[0][1], password=user_data[0][2])
                print('user for login', user_for_login)
                if user:
                    if check_password_hash(pass_to_check, form.password.data):
                        login_user(user_for_login, remember=True)
                        return redirect(url_for('do_order'))
                    else:
                        error = 'Невірний логін чи пароль'
                        return render_template('index.html', form=form, action='', error=error)
            return render_template('index.html', form=form, action = '', error=error)
    return render_template('index.html', form=form, action = '')


@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/do_order', methods = ['GET', 'POST'])
@login_required
def do_order():
    order_student = 0
    form=OrderForm()
    username = current_user.username
    today = datetime.datetime.today().date()
    form.username.data = username
    form.date.data = today
    form.criteria.choices = [('melody', 'Назва пісні'), ('genre', 'Жанр пісні'), ('performer', 'Виконавець')]
    form.criteria.coerce = str
    #print(form.criteria.data)
    if request.method=='POST':
        print('post')
        if not form.validate():
            return render_template('order.html', form=form, action='do_order', form_name='Зробити замовлення', order_student = order_student)
        else:
            order_id = list(db.sqlalchemy_session.query(func.max(order.id)))[0][0]
            order_obj = order(
                id = order_id+1,
                username = form.username.data,
                date = form.date.data,
                criteria = form.criteria.data,
                value = form.value.data
            )

            db.sqlalchemy_session.add(order_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('my_orders'))
    return render_template('order.html', form = form, action='do_order', form_name='Зробити замовлення', order_student = order_student)

# @app.route('/signup', methods = ['GET', 'POST'])
# def signup():
#     db = PostgresDb()
#     form = StudentForm()
#     error = None
#     usernames = list(db.sqlalchemy_session.query(student.username))
#     users = []
#     for i in range(len(usernames)):
#         users.append(usernames[i][0])
#     if request.method == 'POST':
#         if not form.validate():
#             return render_template('new_student.html', form=form, action='signup')
#         else:
#             student_id = list(db.sqlalchemy_session.query(func.max(student.id)))[0][0]
#             if form.username.data in users:
#                 return render_template('new_student.html', form=form, action='signup', error='Username already exists')
#             else:
#                 gen_pass = generate_password_hash(form.password.data, 'sha256')
#                 student_obj = student(
#                 id=student_id+1,
#                 faculty = form.faculty.data,
#                 surname= form.surname.data,
#                 name= form.name.data,
#                 username= form.username.data,
#                 password=gen_pass
#             )
#                 db.sqlalchemy_session.add(student_obj)
#                 db.sqlalchemy_session.commit()
#
#                 return redirect(url_for('index'))
#
#     return render_template('new_student.html', form = form, error = error, action='signup')

@app.route('/view_orders', methods = ['GET', 'POST'])
def view_orders():
    orders = db.sqlalchemy_session.query(order).all()
    return render_template('view_orders.html', orders = orders)

@app.route('/edit_order', methods = ['GET', 'POST'])
def edit_order():
    order_student = -1
    form = OrderForm()
    db = PostgresDb()
    form.criteria.choices = [('melody', 'Назва пісні'), ('genre', 'Жанр пісні'), ('performer', 'Виконавець')]
    form.criteria.coerce = str
    if request.method == 'GET':

        id = request.args.get('id')

        order_obj = db.sqlalchemy_session.query(order).filter(order.id == id).one()

        # fill form and send to user
        form.id.data = order_obj.id
        form.username.data = order_obj.username
        form.date.data = order_obj.date

        form.value.data = order_obj.value

        return render_template('order.html', form=form, form_name="Редагувати інформацію про замовлення",
                               action="edit_order", order_student=order_student)

    else:
        if not form.validate():
            return render_template('order.html', form=form, form_name="Редагувати інформацію про замовлення",
                                   action="edit_order", order_student=order_student)
        else:
            db = PostgresDb()
            # find professor
            order_obj = db.sqlalchemy_session.query(order).filter(order.id == form.id.data).one()

            # update fields from form data
            order_obj.id = form.id.data
            order_obj.username = form.username.data
            order_obj.date = form.date.data
            order_obj.criteria = form.criteria.data
            order_obj.value = form.value.data

            wish_id = list(db.sqlalchemy_session.query(func.max(wish.id)))[0][0]
            student_id = list(db.sqlalchemy_session.query(student.id).filter(student.username==form.username.data))[0][0]

            insert_wish = wish(id=wish_id+1, student_id=student_id, wish_date=form.date.data,
                               wish_criteria=form.criteria.data)

            db.sqlalchemy_session.add(insert_wish)
            db.sqlalchemy_session.commit()

            return redirect(url_for('view_orders'))

@app.route('/delete_order', methods = ['GET', 'POST'])
def delete_order():
    order_id = request.args.get('id')

    result = db.sqlalchemy_session.query(order).filter(order.id == order_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('view_orders'))

@app.route('/my_orders', methods=['GET', 'POST'])
def my_orders():
    orders = db.sqlalchemy_session.query(order).filter(order.username==current_user.username)
    return render_template('my_orders.html', orders=orders)

@app.route('/search_melodies', methods = ['GET', 'POST'])
def search_melodies():
    id = request.args.get('id')
    print(id)
    wish_object = list(db.sqlalchemy_session.query(wish.wish_criteria).filter(wish.id==id))[0][0]
    print(wish_object)
    student_username = list(db.sqlalchemy_session.query(student.username).\
                            join(wish, wish.student_id==student.id).filter(wish.id==id))[0][0]
    #student_username = list(db.sqlalchemy_session.query(student.username).filter(student.id==wish.student_id))[0][0]
    id_to_compare = list(db.sqlalchemy_session.query(order.id).filter(order.username==student_username))[0][0]
    date_to_compare = list(db.sqlalchemy_session.query(order.date).filter(order.date==wish.wish_date))[0][0]
    criteria_to_compare = list(db.sqlalchemy_session.query(order.criteria).filter(order.criteria==wish_object))[0][0]
    print(student_username, id_to_compare, date_to_compare, criteria_to_compare)
    try:
        order_comp = list(db.sqlalchemy_session.query(order.value.label('value')).filter(order.id==id_to_compare,
                                                               order.date==date_to_compare,
                                                               order.criteria==criteria_to_compare))[0][0]
        print(order_comp)

        if wish_object=='melody':
            melodies = db.sqlalchemy_session.query(melody.id, melody.title, melody.singer).filter(melody.title==order_comp)
        elif wish_object=='genre':
            genre_comp = list(db.sqlalchemy_session.query(genre.id).filter(genre.name==order_comp))[0][0]
            melodies = db.sqlalchemy_session.query(melody.id, melody.title, melody.singer).filter(melody.melody_genre==genre_comp)
        else:
            melodies = db.sqlalchemy_session.query(melody.id, melody.title, melody.singer).filter(melody.singer==order_comp)
        return render_template('melodies.html', melodies=melodies, id=id)
    except IndexError:
        return render_template('melodies.html', nothing = 'nothing to show')

@app.route('/melody_to_wish', methods = ['GET', 'POST'])
def melody_to_wish():
    if request.method == 'GET':
        melody_id = request.args.get('melody_id')
        wish_id = request.args.get('wish_id')
        print(melody_id, wish_id)
        #-----------------------------------------------------------------
        new_wish = db.sqlalchemy_session.query(wish.id, wish.student_id, wish.wish_date,
                                                  wish.wish_criteria,
                                                  wish.melody_id).filter(wish.id == wish_id)
        print(list(new_wish))
        newer_wish = list(new_wish)
        db.sqlalchemy_session.query(wish).filter(wish.id==wish_id).delete(synchronize_session=False)
        print(newer_wish)

        #db.sqlalchemy_session.query(wish).delete(saved_value2)

        newest_wish = wish(id=newer_wish[0][0], student_id=newer_wish[0][1],
                        wish_date=newer_wish[0][2], wish_criteria=newer_wish[0][3],
                        melody_id=melody_id)

        db.sqlalchemy_session.add_all([newest_wish])
        db.sqlalchemy_session.commit()

        wishes = db.sqlalchemy_session.query(wish.id, student.username, wish.wish_date, wish.wish_criteria, wish.melody_id). \
            join(wish, student.id == wish.student_id).all()
        return render_template('wish.html', wishes = wishes)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    error = None
    usernames = list(db.sqlalchemy_session.query(student.username))
    users = []
    for i in range(len(usernames)):
        users.append(usernames[i][0])
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_student.html', form=form, form_name = "Зареєструватись", action='signup')
        else:
            student_id = list(db.sqlalchemy_session.query(func.max(student.id)))[0][0]
            if form.username.data in users:
                return render_template('new_student.html', form=form, form_name="Зареєструватись", action='signup', error='Username already exists')
            else:
                gen_pass = generate_password_hash(form.password.data)
                student_obj = student(
                id=student_id+1,
                faculty = form.faculty.data,
                surname= form.surname.data,
                name= form.name.data,
                username= form.username.data,
                    password=gen_pass
            )
                db.sqlalchemy_session.add(student_obj)
                db.sqlalchemy_session.commit()

                return redirect(url_for('index'))

    return render_template('new_student.html', form=form, form_name = "Зареєструватись", action='signup')


@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template('adminpanel.html')

@app.route('/student', methods = ['GET', 'POST'])
def student_show():
    result = db.sqlalchemy_session.query(student).all()
    return render_template('student.html', students = result)

@app.route('/new_student', methods = ['GET', 'POST'])
def new_student():
    form = StudentForm()
    error = None
    usernames = list(db.sqlalchemy_session.query(student.username))
    users = []
    for i in range(len(usernames)):
        users.append(usernames[i][0])
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_student.html', form=form, form_name = "Додати студента", action='new_student')
        else:
            student_id = list(db.sqlalchemy_session.query(func.max(student.id)))[0][0]
            if form.username.data in users:
                return render_template('new_student.html', form=form, form_name="Додати студента", action='new_student', error='Username already exists')
            else:
                gen_pass = generate_password_hash(form.password.data)
                student_obj = student(
                id=student_id+1,
                faculty = form.faculty.data,
                surname= form.surname.data,
                name= form.name.data,
                username= form.username.data,
                    password=gen_pass
            )
                db.sqlalchemy_session.add(student_obj)
                db.sqlalchemy_session.commit()

                return redirect(url_for('student_show'))
    return render_template('new_student.html', form=form, form_name = "Додати студента", action='new_student')


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = StudentForm()
    db = PostgresDb()
    if request.method == 'GET':

        id = request.args.get('id')

        student_obj = db.sqlalchemy_session.query(student).filter(student.id == id).one()

        # fill form and send to user
        form.id.data = student_obj.id
        form.faculty.data = student_obj.faculty
        form.name.data = student_obj.name
        form.surname.data = student_obj.surname
        form.username.data = student_obj.username
        form.password.data = ''

        return render_template('new_student.html', form=form, form_name="Редагувати інформацію про студента", action="edit_student")

    else:
        if not form.validate():
            return render_template('new_student.html', form=form, form_name="Редагувати інформацію про студента", action="edit_student")
        else:
            db = PostgresDb()
            # find professor
            student_obj = db.sqlalchemy_session.query(student).filter(student.id == form.id.data).one()

            # update fields from form data
            student_obj.id = form.id.data
            student_obj.faculty = form.faculty.data
            student_obj.name = form.name.data
            student_obj.surname = form.surname.data
            student_obj.username = form.username.data
            student_obj.password = generate_password_hash(form.password.data)

            db.sqlalchemy_session.commit()

            return redirect(url_for('student_show'))

@app.route('/delete_student', methods = ['GET', 'POST'])
def delete_student():
    student_id = request.args.get('id')

    result = db.sqlalchemy_session.query(student).filter(student.id == student_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('student_show'))

@app.route('/genre', methods = ['GET', 'POST'])
def genre_show():
    result = db.sqlalchemy_session.query(genre).all()
    return render_template('genre.html', genres = result)

@app.route('/new_genre', methods = ['GET', 'POST'])
def new_genre():
    error= None
    form = GenreForm()
    genres = list(db.sqlalchemy_session.query(genre.name))
    gens = []
    for i in range(len(genres)):
        gens.append(genres[i][0])
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_genre.html', form=form, form_name="Новий жанр", action="new_genre")
        else:
            genre_id = list(db.sqlalchemy_session.query(func.max(genre.id)))[0][0]
            if form.genre_name.data in gens:
                return render_template('new_genre.html', form=form, form_name="Новий жанр", action="new_genre", error="Такий жанр вже є в базі")
            else:
                genre_obj = genre(
                id=genre_id + 1,
                name=form.genre_name.data,
                psychotype=form.psychotype.data)

                db.sqlalchemy_session.add(genre_obj)
                db.sqlalchemy_session.commit()

                return redirect(url_for('genre_show'))
    return render_template('new_genre.html', form = form, form_name = 'Новий жанр', action='new_genre', error=error)

@app.route('/edit_genre', methods=['GET', 'POST'])
def edit_genre():
    form = GenreForm()

    if request.method == 'GET':

        id = request.args.get('id')

        db = PostgresDb()
        genre_obj = db.sqlalchemy_session.query(genre).filter(genre.id == id).one()

        # fill form and send to user
        form.id.data = genre_obj.id
        form.genre_name.data = genre_obj.name
        form.psychotype.data = genre_obj.psychotype

        return render_template('new_genre.html', form=form, form_name="Редагувати інформацію про жанр", action="edit_genre")

    else:
        if not form.validate():
            return render_template('new_genre.html', form=form, form_name="Редагувати інформацію про жанр", action="edit_genre")
        else:
            db = PostgresDb()
            # find professor
            genre_obj = db.sqlalchemy_session.query(genre).filter(genre.id == form.id.data).one()

            # update fields from form data
            genre_obj.id = form.id.data
            genre_obj.name = form.genre_name.data
            genre_obj.psychotype = form.psychotype.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('genre_show'))

@app.route('/performer', methods = ['GET', 'POST'])
def performer_show():
    result = db.sqlalchemy_session.query(performer).all()
    return render_template('performer.html', performers = result)

@app.route('/new_performer', methods=['GET', 'POST'])
def new_performer():
    error = None
    form = PerformerForm()
    performers = list(db.sqlalchemy_session.query(performer.name))
    pers = []
    for i in range(len(performers)):
        pers.append(performers[i][0])
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_performer.html', form=form, form_name="Новий виконавець", action="new_performer")
        else:
            if form.name.data in pers:
                return render_template('new_performer.html', form=form, form_name="Новий виконавець", error='Такий виконавець вже існує', action="new_performer")
            else:
                performer_id = list(db.sqlalchemy_session.query(func.max(performer.id)))[0][0]
                performer_obj = performer(
                    id= performer_id + 1,
                    name = form.name.data)

                db.sqlalchemy_session.add(performer_obj)
                db.sqlalchemy_session.commit()

                return redirect(url_for('performer_show'))
    return render_template("new_performer.html", form = form, action= "new_performer", form_name = "Новий виконавець")

@app.route('/edit_performer', methods = ['GET', 'POST'])
def edit_performer():
    form = PerformerForm()

    if request.method == 'GET':

        id = request.args.get('id')

        db = PostgresDb()
        performer_obj = db.sqlalchemy_session.query(performer).filter(performer.id == id).one()

        # fill form and send to user
        form.id.data = performer_obj.id
        form.name.data = performer_obj.name

        return render_template('new_performer.html', form=form, form_name="Редагувати інформацію про виконавця", action="edit_performer")

    else:
        if not form.validate():
            return render_template('new_performer.html', form=form, form_name="Редагувати інформацію про виконавця", action="edit_performer")
        else:
            db = PostgresDb()
            # find professor
            performer_obj = db.sqlalchemy_session.query(performer).filter(performer.id == form.id.data).one()

            # update fields from form data
            performer_obj.id = form.id.data
            performer_obj.name = form.name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('performer_show'))

@app.route('/album', methods = ['GET', 'POST'])
def album_show():
    result = db.sqlalchemy_session.query(album.title, performer.name).join(performer, performer.id==album.performer_id).all()
    return render_template('album.html', albums = result)

@app.route('/new_album', methods = ['GET', 'POST'])
def new_album():
    form = AlbumForm()
    ch = []
    performers = sorted(list(db.sqlalchemy_session.query(performer.id).distinct()))
    pers = []
    for i in range(len(performers)):
        pers.append(performers[i][0])
    for i in range(len(performers)):
        tuple = performers[i][0], performers[i][0]
        ch.append(tuple)
    print(ch)
    form.album_performer.choices = ch
    error = None
    performers = list(db.sqlalchemy_session.query(performer.id))
    pers = []
    for i in range(len(performers)):
        pers.append(performers[i][0])
    albums = list(db.sqlalchemy_session.query(album.title))
    albs = []
    for i in range(len(albums)):
        albs.append(albums[i][0])
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_album.html', form=form, form_name="Новий альбом", action="new_album")
        else:
            if form.album_performer.data in pers and form.album_name.data in albs:
                return render_template('new_album.html', form=form, form_name="Новий альбом", action="new_album", error="Запис вже існує")
            else:
                album_id = list(db.sqlalchemy_session.query(func.max(album.id)))[0][0]
                album_obj = album(
                    id=album_id + 1,
                    title=form.album_name.data,
                    performer_id=form.album_performer.data)

                db.sqlalchemy_session.add(album_obj)
                db.sqlalchemy_session.commit()

                return redirect(url_for('album_show'))

    return render_template("new_album.html", form=form, action="new_album", form_name="Новий альбом")

@app.route('/melody', methods = ['GET', 'POST'])
def melody_show():
    result = db.sqlalchemy_session.query(melody.title, melody.singer, melody.release_date, genre.name, album.title.label("albumtitle")).\
        join(genre, genre.id==melody.melody_genre).join(album, melody.album_id==album.id).all()
    return render_template('melody.html', melodies = result)

@app.route('/new_melody', methods=['GET', 'POST'])
def new_melody():
    #----------------------------------------------------------------------------------------------------------
    singers = list(db.sqlalchemy_session.query(performer.name))
    sings = []
    for i in range(len(singers)):
        sings.append(singers)
    ch_s = []
    for i in range(len(singers)):
        s_t = singers[i][0], singers[i][0]
        ch_s.append(s_t)
    # ----------------------------------------------------------------------------------------------------------
    genres = list(db.sqlalchemy_session.query(genre.name))
    gens=[]
    ch_g=[]
    for i in range(len(genres)):
        gens.append(genres[i][0])
        g_t = genres[i][0], genres[i][0]
        ch_g.append(g_t)
    # ----------------------------------------------------------------------------------------------------------
    albums = list(db.sqlalchemy_session.query(album.title))
    albs = []
    ch_a = []
    for i in range(len(albums)):
        albs.append(albums[i][0])
        a_t = albums[i][0], albums[i][0]
        ch_a.append(a_t)
    # ----------------------------------------------------------------------------------------------------------
    form = MelodyForm()
    form.singer.choices = ch_s
    form.melody_genre.choices = ch_g
    form.album.choices = ch_a
    # ----------------------------------------------------------------------------------------------------------
    genre_to_send = 0
    album_to_send = 0
    # ----------------------------------------------------------------------------------------------------------
    if request.method == 'POST':
        if not form.validate():
            return render_template('new_melody.html', form=form, form_name="Нова мелодія", action="new_melody")
        else:
            g_query = db.sqlalchemy_session.query(genre.id).filter(genre.name == form.melody_genre.data)
            a_query = db.sqlalchemy_session.query(album.id).filter(album.title == form.album.data)
            compare1 = (form.title.data, a_query[0].id, g_query[0].id, form.singer.data, form.release_date.data,)
            compare2 = list(db.sqlalchemy_session.query(melody.title, melody.album_id, melody.melody_genre, melody.singer, melody.release_date))
            print(compare1)
            print(compare2)
            if compare1 in compare2:
                return render_template('new_melody.html', form=form, form_name="Нова мелодія", action="new_melody", error='Такий запис вже існує')
            else:
                melody_id = list(db.sqlalchemy_session.query(func.max(melody.id)))[0][0]
                g_query = db.sqlalchemy_session.query(genre.id).filter(genre.name==form.melody_genre.data)
                a_query = db.sqlalchemy_session.query(album.id).filter(album.title==form.album.data)
                melody_obj = melody(
                    id = melody_id+1,
                    title = form.title.data,
                    singer = form.singer.data,
                    release_date =form.release_date.data,
                    melody_genre = g_query[0].id,
                    album_id = a_query[0].id)

                db.sqlalchemy_session.add(melody_obj)
                db.sqlalchemy_session.commit()

                return redirect(url_for('melody_show'))

    return render_template("new_melody.html", form = form, action="new_melody", form_name = "Нова мелодія")

@app.route('/wish', methods = ['GET', 'POST'])
def wish_show():
    result = db.sqlalchemy_session.query(wish.id, student.username, wish.wish_date, wish.wish_criteria, wish.melody_id).\
       join(wish, student.id==wish.student_id).all()
    return render_template('wish.html', wishes = result)

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    feature = 'FICT'
    bar = create_plot(feature)
    options = db.sqlalchemy_session.query(student.faculty).distinct()
    return render_template('dashboard.html', plot=bar, options=options)

def create_plot(feature):
    result2 = db.sqlalchemy_session.query(genre.psychotype.label('genre'), func.count(genre.psychotype).label('count')).\
        join(melody, genre.id==melody.melody_genre).join(wish, wish.melody_id==melody.id).join(student, student.id == wish.student_id).\
        filter(student.faculty==feature).group_by(student.faculty, genre.psychotype)
    print('list result', list(result2))
    # psychotypes = list(result2)
    for row in result2:
        print(row)
    psychotypes = dict((genre, count) for genre, count in result2)
    print(psychotypes)
    psychotypes_invert = dict((count, genre) for genre, count in result2)
    print(psychotypes_invert)
    maxkey = psychotypes_invert[max(psychotypes.values())]
    print(max(psychotypes.values()), 'and its key ', maxkey)

    x = []
    y = []
    for a in psychotypes.keys():
        x.append(a)
    for b in psychotypes.values():
        y.append(b)

    print(x)
    print(y)
    data = [
        go.Bar(
            x=x,  # assign x as the dataframe column 'x'
            y=y
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)

    return graphJSON

if __name__ == '__main__':
    app.run()
