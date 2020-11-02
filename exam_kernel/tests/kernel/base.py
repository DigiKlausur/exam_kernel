import unittest
import os
import sys


class BaseTest(unittest.TestCase):

    def setUp(self):
        # Create path to config file
        self.config_path = os.path.join(sys.prefix, 'etc', 'jupyter')
        self.config_file = os.path.join(self.config_path, 'ipython_config.py')
        os.makedirs(self.config_path, exist_ok=True)

    def tearDown(self):
        if os.path.isfile(self.config_file):
            os.remove(self.config_file)