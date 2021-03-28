import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from webapp.db import get_db

# creates a Blueprint named 'auth'.
# the blueprint needs to know where it’s defined, so __name__ is passed as the second argument
# url_prefix will be prepended to all the URLs associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        address = request.form['address']
        occupation = request.form['occupation']
        

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'    
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not phone:
            error = 'Phone is required.'
        elif not first_name:
            error = 'First Name is required.'
        elif not middle_name:
            error = 'Middle Name is required.'
        elif not last_name:
            error = 'Last Name is required.'
        elif not address:
            error = 'Address is required.'
        elif not occupation:
            error = 'Occupation is required.'
        
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        if error is None:
            db.execute(
                'INSERT INTO user \
                    (username, password, email, phone, first_name, middle_name, last_name, \
                    address, occupation) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (username, generate_password_hash(password), email, phone, first_name, middle_name, last_name, \
                    address, occupation)
                )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')
    # return render_template('auth/register_1.html')


# login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username, )).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            # check_password_hash() hashes the submitted password in the same way as the stored hash
            # and securely compares them. 
            error = 'Incorrect password.'

        if error is not None:
            flash(error)
        else:
            # session is a dict that stores data across requests.
            # session.permanent = True
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
    return render_template('auth/login.html')


# user’s id is stored in the session, it will be available on subsequent requests. 
# At the beginning of each request, 
# if a user is logged in their information should be loaded and made available to other views.

# bp.before_app_request() registers a function that runs before the view function, 
# no matter what URL is requested. 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# @bp.before_app_request
# def make_session_permanent():
#     session.permanent = True
#     bp.permanent_session_lifetime = timedelta(minutes=2)
#     session.modified = True

# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# change password
@bp.route('/change_password', methods=('GET', 'POST'))
def change_password():
    user = get_db().execute('SELECT * FROM user WHERE username = ?', (g.user['username'], )).fetchone()
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        error = None

        if new_password != confirm_password:
            error = 'Passwords do not match.'

        elif check_password_hash(user['password'], new_password):
            error = 'New password should be different.'

        if error is None:
            db = get_db()
            db.execute('UPDATE user SET password = ? WHERE id = ?', (generate_password_hash(new_password), user['id']))
            db.commit()
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/changepassword.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view