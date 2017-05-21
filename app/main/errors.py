# THIS MODULE IS FOR PUT ALL ERRORS ROUTES
# WE NEED RENDER_TEMPLATE MODULE
from flask import render_template

# WE ALSO NEED ALL THIS MODULE TO GET THE BLUEPRINT
from . import main

# WE GONNA USE THE DECORATORS FROM THE BLUEPRINT IN ORDER TO PUT THE ERROR PAGES


@main.app_errorhandler(404)  # WE USE THE 'MAIN.APP' CAUSE IF WU USE ONLY 'ERROR HANDLER'
def page_not_found(e):  # THAT ONLY SHOWS WHEN A ONE THREAD [WIP]
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

