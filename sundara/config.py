"""Read in configuration options from a project's Sundara config."""

import os
import shutil
import configparser

from sundara import resources
from sundara import exceptions

USER_CONF = os.path.expanduser('~/.sundararc')
PROJECT_CONF = '.sundararc'

class Config():
    def __init__(self, project_dir):
        project_conf = os.path.join(project_dir, PROJECT_CONF)

        # Make sure a project config exists; if not, create it.
        if not os.path.exists(project_conf):
            if os.path.exists(USER_CONF):
                shutil.copy(USER_CONF, project_conf)
            else:
                with open(project_conf, "w+") as f:
                    f.write(resources.CONFIG)

        # Read the config file.
        self.config = configparser.ConfigParser()
        self.config.read(project_conf)

    def get(self, section, option):
        try:
            return self.config.get(section, option)
        except configparser.Error as e:
            raise exceptions.ConfigError(str(e))
