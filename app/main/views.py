# HERE WE GONNA PUT ALL ABOUT OUR VIEWS

from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


# HERE WE DEFINE A VIEW FUNCTION FOR THE INDEX
@main.route('/', methods=['GET', 'POST'])  # WE USE THE ROUTE METHOD FROM THE MAIN BLUEPRINT
def index():
    form = NameForm()  # ASSIGN THE FORM
    if form.validate_on_submit():  # IF THERE ARE INFORMATION ON THE FORM
        user = User.query.filter_by(username=form.name.data).first()  # SEARCH FOR THE USERNAME IN THE DB
        if user is None:  # IF THERE IS NOT, WE CREATE A NEW USER
            user = User(username=form.name.data)
            db.session.add(user)
            session['know'] = False
            if current_app.config['BLOG_ADMIN']:  # WE ASSERT THAT THE BLOG ADMIN IS TOOK
                send_email(current_app.config['BLOG_ADMIN'], 'New User', 'mail/new_user', user=user)  # WE SEND A EMAIL
        else:
            session['know'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))  # WE USE .INDEX CAUSE THIS MAKE REFERENCE FOR MAIN.
        # INDEX TO USE THE BLUEPRINT
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           know=session.get('know', False))



