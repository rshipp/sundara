import unittest

import os
import shutil
import tempfile
import uuid

from sundara import server
from sundara import config

class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestHandler(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mktemp()
        os.makedirs(self.dir)
        self.config_file = os.path.join(self.dir, config.PROJECT_CONF)
        self.old_project_conf = config.PROJECT_CONF
        config.PROJECT_CONF = self.config_file
        # Make sure user config can't interfere with the tests.
        config.USER_CONF = ''
        # Set up the handler.
        self.handler = server.SundaraRequestHandler(None, None)
        # Mock getcwd.
        self.old_getcwd = os.getcwd
        os.getcwd = lambda: self.dir

    def tearDown(self):
        shutil.rmtree(self.dir)
        # Restore mocked pieces.
        config.PROJECT_CONF = self.old_project_conf
        os.getcwd = self.old_getcwd

    def test_translate_path_uses_conf_if_exists(self):
        unique_string = str(uuid.uuid4()) + '/'
        with open(self.config_file, "w+") as f:
            f.write('[sundara]\ngenerate = %s\n' % unique_string)
        self.assertEquals(unique_string, self.handler.translate_path('/'))

    def test_translate_path_uses_sane_default_if_no_conf(self):
        self.assertFalse(os.path.exists(self.config_file))
        self.assertEquals(os.path.join(self.dir, 'www/'),
                self.handler.translate_path('/'))

    def test_translate_path_translates_paths(self):
        paths = {
            '/': '',
            '/index.html': 'index.html',
            '/index.php?lang=en_US&bob=sue': 'index.php',
            '/favicon.ico': 'favicon.ico',
            '/some/path': 'some/path',
            '/some/path/': 'some/path',
            '/some/path/in.e?le': 'some/path/in.e',
        }
        for path in paths:
            self.assertEquals(os.path.join(self.dir, 'www/', paths[path]),
                    self.handler.translate_path(path))
