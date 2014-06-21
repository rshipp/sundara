import unittest

import os
import shutil
import tempfile
import uuid

from sundara import config
from sundara import resources
from sundara import exceptions

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mktemp()
        os.makedirs(self.dir)
        self.config_file = os.path.join(self.dir, config.PROJECT_CONF)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_creates_conf_if_not_exists(self):
        self.assertFalse(os.path.exists(self.config_file))
        config.Config(self.dir)
        self.assertTrue(os.path.isfile(self.config_file))

    def test_doesnt_overwrite_conf_if_exists(self):
        # Embed a unique string.
        unique_string = '[%s]' % str(uuid.uuid4())
        with open(self.config_file, "w+") as f:
            f.write(unique_string)
        self.assertTrue(os.path.isfile(self.config_file))
        # Run config again and check that the string is still there.
        config.Config(self.dir)
        with open(self.config_file, "r+") as f:
            self.assertEquals(unique_string, f.read())

    def test_copies_user_conf_if_exists(self):
        # Embed a unique string.
        os.mkdir(os.path.join(self.dir, 'USER'))
        config.USER_CONF = os.path.join(self.dir, 'USER',
                config.PROJECT_CONF)
        unique_string = '[%s]' % str(uuid.uuid4())
        with open(config.USER_CONF, "w+") as f:
            f.write(unique_string)
        # Run config and check that the file was copied.
        config.Config(self.dir)
        with open(self.config_file, "r+") as f:
            self.assertEquals(unique_string, f.read())

    def test_uses_resources_if_no_other_options(self):
        # Make sure user conf doesn't exist.
        os.mkdir(os.path.join(self.dir, 'USER'))
        config.USER_CONF = os.path.join(self.dir, 'USER',
                config.PROJECT_CONF)
        self.assertFalse(os.path.exists(config.USER_CONF))
        # Make sure project conf doesn't exist.
        self.assertFalse(os.path.exists(self.config_file))
        # Run config and check that it writes from resources.
        config.Config(self.dir)
        with open(self.config_file, "r+") as f:
            self.assertEquals(resources.CONFIG, f.read())

    def test_get_gets_config(self):
        # Embed a unique string.
        unique_section = str(uuid.uuid4())
        unique_option = str(uuid.uuid4())
        unique_value = str(uuid.uuid4())
        unique_string = '[%s]\n%s = %s' % (unique_section,
                unique_option, unique_value)
        with open(self.config_file, "w+") as f:
            f.write(unique_string)
        # Run config and check that it reads the correct value.
        c = config.Config(self.dir)
        self.assertEquals(unique_value, c.get(unique_section,
            unique_option))

    def test_raises_ConfigError_on_exception(self):
        c = config.Config(self.dir)
        self.assertRaises(exceptions.ConfigError, c.get, 'badsection', 'option')
        self.assertRaises(exceptions.ConfigError, c.get, 'sundara', 'badoption')
