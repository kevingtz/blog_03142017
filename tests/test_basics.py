# THIS MODULE IS TO MAKE THE TESTS OF THE APP [TODO: IMPROVE THIS MODULE]

import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):  # A BASE CLASS
    def setUp(self):  # PREPARING ALL TO SET UP THE APP IN ORDER TO TEST IT
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):  # GET DOWN BEFORE TEEST
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):  # ENSURE THAT THE APP ACTUALLY EXITS
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):  # ASSERT THE THE ENVIRONMENT OF THE APP IS TESTING
        self.assertTrue(current_app.config['TESTING'])
