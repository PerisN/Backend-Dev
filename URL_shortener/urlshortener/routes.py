from flask import render_template, url_for, flash, redirect, request
from urlshortener import app, db, bcrypt
from urlshortener.forms import RegistrationForm, LoginForm
from urlshortener.models import User, URL
from flask_login import login_user, current_user, logout_user, login_required
import pyshorteners

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        original_url = form.url.data
        shortener = pyshorteners.Shortener()
        shortened_url = shortener.tinyurl.short(original_url)
        url = URL(original_url=original_url, shortened_url=shortened_url, user_id=current_user.id)
        db.session.add(url)
        db.session.commit()
        flash('URL has been shortened successfully', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form, current_user=current_user)

@app.route('/', methods=['GET', 'POST'])
def shorten_url():
    form = RegistrationForm()
    shortened_url = None
    if form.validate_on_submit():
        original_url = form.url.data
        shortener = pyshorteners.Shortener()
        shortened_url = shortener.tinyurl.short(original_url)
        url = URL(original_url=original_url, shortened_url=shortened_url, user_id=current_user.id)
        db.session.add(url)
        db.session.commit()
        form.url.data = ''
    return render_template('home.html', shortened_url=shortened_url, form=form)

@app.route('/history')
@login_required
def history():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', urls=urls, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))