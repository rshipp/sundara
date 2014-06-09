import unittest
from unittest.mock import Mock

import os
import shutil
import tempfile
import uuid
from configparser import ConfigParser
from http.server import HTTPServer

from sundara import server
from sundara import config
from sundara import resources

class TestServer(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mktemp()
        os.makedirs(self.dir)
        self.config_file = os.path.join(self.dir, config.PROJECT_CONF)
        # Make sure user config can't interfere with the tests.
        config.USER_CONF = ''
        # Mock getcwd.
        self.old_getcwd = os.getcwd
        os.getcwd = lambda: self.dir

    def tearDown(self):
        shutil.rmtree(self.dir)
        # Restore getcwd.
        os.getcwd = self.old_getcwd

    def test_can_use_config(self):
        with open(self.config_file, "w+") as f:
            f.write(resources.CONFIG)
        c = config.Config(self.dir)
        c.config.set('sundara', 'generate', self.dir)
        c.config.write(open(self.config_file, 'w+'))
        try:
            s = server.SundaraServer(config=c)
        except Exception:
            self.fail()
        self.assertEquals(s.ip, c.get('server', 'ip'))
        self.assertEquals(s.port, int(c.get('server', 'port')))

    def test_can_use_without_config(self):
        self.assertFalse(os.path.exists(self.config_file))
        os.makedirs(os.path.join(self.dir, 'www/'))
        try:
            s = server.SundaraServer()
        except Exception:
            self.fail()
        self.assertEquals(s.ip, '127.0.0.1')
        self.assertEquals(s.port, 8080)

    def test_excepts_if_no_path(self):
        self.assertRaises(IOError, server.SundaraServer)

    def test_run_serves(self):
        os.makedirs(os.path.join(self.dir, 'www/'))
        #server.SundaraServer().run()

    def test_run_excepts(self):
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
