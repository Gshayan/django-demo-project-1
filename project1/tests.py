from django.test import TestCase
from django.conf import Settings
import os
from django.contrib.auth.password_validation import validate_password

class demo1TestCase(TestCase):
    def test_secret_key_check(self):
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        # self.assertNotEqual(SECRET_KEY, "abc213")
        try:
            is_string = validate_password(SECRET_KEY)
        except Exception as e:
            msg = f"This is a bad key: {e.messages}"
            self.fail(msg)