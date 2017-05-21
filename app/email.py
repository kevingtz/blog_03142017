# HERE WE GONNA PUT ALL ABOUT THE EMAIL SUPPORT

from threading import Thread  # WE USE THIS IN ORDER TO USE A SECOND THREAD TO SEND THE EMAIL
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):  # THIS METHOD IS USING TO SEND THE ASYNC MAIL
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()  # ASSIGN THE APP
    msg = Message(app.config['BLOG_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['BLOG_MAIL_SENDER'], recipients=[to])  # THE RECIPER AND THE SUBJECT
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])  # PUTTING THE EMAIL IN A SECOND THREAD
    thr.start()
    return thr
