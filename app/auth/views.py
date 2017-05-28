# HERE BE THE VIEW FUNCTIONS FOR THE AUTHENTICATION

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, \
    PasswordResetForm, ChangeEmailForm
from ..email import send_email


@auth.before_app_request
def before_request():  # THIS FUNCTION ONLY WORKS WHEN THE NEXT CONDITIONS ARE TRUE:
    if current_user.is_authenticated:
        current_user.ping()  # HERE WE CALL PING METHOD IN ORDER TO UPDATE THE LAST SEEN USER PROPERTY
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':  # THE USER IS AUTHENTICATED, THE CURRENT USER IS NOT CONFIRMED,
                #  AND OTHER THAT IN THIS POINT I DON'T GET WELL
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # WE CALL THE LOGIN FORM CLASS
    if form.validate_on_submit():  # VALIDATE THAT THE FORM WAS SENT
        user = User.query.filter_by(email=form.email.data).first()  # SEARCHING THE USER BY EMAIL
        if user is not None and user.verify_password(form.password.data):  # VALIDATING THAT THE USER EXIST AND
            # IT IS THEIR CORRECT PASSWORD
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))  # [SPANISH] SI EL USUARIO INTENTO
            # ACCEDER MEDIANTE UNA URL PROTEGIDA, ESTO LE HABRA MANDADO AL LOGIN Y POSTERIORMENTE DE VERIFICAR SUS
            # CREDENCIALES LO RETORNARA A LA URL PROTEGIDA QUE ESTABA ACCEDIENDO, ES DECIR AL 'SIGIENTE' ARGUMENTO QUE TRAIA SU URL,
            # EN CASO DE QUE ESTE ARGUMENTO NO EXISTA SIMPLEMENTE LO REDIRIGE AL INDEX DEL BLUEPRINT MAIN.
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():  # THIS METHOD IS GOING TO REGISTER THE NEW USERS
    form = RegistrationForm()  # FIRST AT ALL WE NEED
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()  # HERE WE GONNA TO MAKE A COMMIT ON THE DB BECAUSE IF IT WAITS AFTER THE REQUEST IT WILL
        # BE TO LATE TO PASS THE ID OF THE NEW USER AN SEND IT TO HIM IN A EMAIL.
        token = user.generation_confirmed_token()  # CREATING THE TOKEN
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)  # SENDING A EMAIL
        # WITH THE TOKEN
        flash('A confirmation email was send to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):  # THE SUPPORT OF REQUEST FOR THE CONFIRMATION TOKENS
    if current_user.confirmed:  # THE USER IS CONFIRMED
        return redirect(url_for('main.index'))
    elif current_user.confirm(token):  # IF NOT THEN NOW IS CONFIRMED
        flash("You have confirmed your account, thank's!")
    else:  # SOME ERROR WITH THE TOKEN
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():  # A SUPPORT TO RESEND A CONFIRMATION TOKEN
    token = current_user.generation_confirmed_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password have been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset your password', 'auth/email/reset_password', user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        elif user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your new email address.', 'auth/email/change_email', user=current_user,
                       token=token)
            flash('An email with instructions to confirm yor new email address has been sent to you')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request')
    return redirect(url_for('main.index'))
