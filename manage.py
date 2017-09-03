#!/usr/bin/env python

# THIS MODULE IS TO MANAGE ALL THE APP WITH A SIMPLE COMMANDS


import os
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# CREATE AND INITIALIZE THE FLASK EXTENSION'S
app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # INITIALIZE AN INSTANCE OF THE APP PASSING IT THE CONFIG
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():  # THIS IS TO USE A SHELL TO INTERACT WITH THE APP
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command  # A DECORATOR TO EASY COMMAND CREATION
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()