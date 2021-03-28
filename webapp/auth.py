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
        # create request for entering user information for registeration
        # request.form is a special type of dict mapping submitted form keys and values.
        # the user will input the following information
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

        # Validate that username and password are not empty.
        # the following check if the user information is filled properly
        # if not error message will show on the interface
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
        
        # Validate that username is not already registered by querying the database and checking if a result is returned.
        # db.execute takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders with.
        # fetchone() returns one row from the query.
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        # If validation succeeds, insert the new user data into the database.
        #  generate_password_hash() is used to securely hash the password, and that hash is stored.
        if error is None:
            db.execute(
                'INSERT INTO user \
                    (username, password, email, phone, first_name, middle_name, last_name, \
                    address, occupation) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (username, generate_password_hash(password), email, phone, first_name, middle_name, last_name, \
                    address, occupation)
                )
            # db.commit() needs to be called afterwards to save the changes.
            db.commit()
            # After storing the user, they are redirected to the login page.
            # redirect() generates a redirect response to the generated URL.
            return redirect(url_for('auth.login'))

        # If validation fails, the error is shown to the user
        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)

    return render_template('auth/register.html')
    # return render_template('auth/register_1.html')


# login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # The user is queried first and stored in a variable for later use.
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
    # load_logged_in_user checks if a user id is stored in the session 
    # and gets that user’s data from the database, storing it on g.user
    user_id = session.get('user_id')

    # If there is no user id, or if the id doesn’t exist, g.user will be None.
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# logout
@bp.route('/logout')
def logout():
    # remove the user id from the session for logging out
    session.clear()
    return redirect(url_for('index'))


# change password
@bp.route('/change_password', methods=('GET', 'POST'))
def change_password():
    # db.execute takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders with.
    # fetchone() returns one row from the query.
    user = get_db().execute('SELECT * FROM user WHERE username = ?', (g.user['username'], )).fetchone()
    
    if request.method == 'POST':
        # create request for entering user new password and confirm the new password
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        error = None

        # the entered new password and the confirm password should be the same
        if new_password != confirm_password:
            error = 'Passwords do not match.'

        # if the new password and the confirm password are the same
        # check if the new password is same as the old password
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