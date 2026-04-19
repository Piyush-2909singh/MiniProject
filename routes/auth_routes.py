import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import authenticate_user, register_user
import utils.security

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
@utils.security.limiter.limit("5 per minute")



def login():

    if request.method == 'POST':

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        logger.debug("Login POST received for username=%s password_len=%d", username, len(password))
        user = authenticate_user(username, password)

        if user:

            login_user(user)
            logger.info("Login successful for username=%s", username)
            return redirect(url_for('home'))
        
        else:

            logger.warning("Login failed for username=%s", username)
            flash('Invalid credentials', 'error')

    return render_template('login.html')




@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        logger.debug("Register POST received for username=%s password_len=%d", username, len(password))
        success, message = register_user(username, password)
        
        
        if success:

            logger.info("Registration successful for username=%s", username)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        else:


            logger.warning("Registration failed for username=%s reason=%s", username, message)
            flash(message, 'error')

            
    return render_template('register.html')



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
