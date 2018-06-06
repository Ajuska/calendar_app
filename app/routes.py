from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    events = Event.query.all()
    return render_template('index.html', title='Home Page', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registred user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        full_date = datetime.combine(form.date.data, form.time.data) #(datetime.date(2018, 6, 8), datetime.time(14, 20))
        event = Event(title=form.title.data, author = current_user,
        body=form.body.data, timestamp=full_date)
        db.session.add(event)
        db.session.commit()
        flash('Your event was created!')
        return redirect(url_for('index'))
    return render_template('new_event.html', title='New Event', form=form)
