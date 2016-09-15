import os
import random
import subprocess
import sys
import unittest

import requests
import requests.exceptions
from retry.api import retry_call


class MainTest(unittest.TestCase):

    def test_application_is_starting(self):
        port = random.randint(30000, 60000)
        env = os.environ.copy()
        env.update(dict(
            FLASK_APP="arsenal.main:app"
        ))
        p = subprocess.Popen([sys.executable, _get_entry_point_path('flask'), 'run', '--port', str(port)], env=env)

        try:
            def test():
                r = requests.get("http://localhost:{}".format(port))
                self.assertEqual(404, r.status_code)

            retry_call(test, tries=20, delay=0.05, exceptions=requests.exceptions.ConnectionError)
        finally:
            p.kill()


def _get_entry_point_path(entry_point):
    return os.path.join(os.path.dirname(sys.executable), entry_point)
