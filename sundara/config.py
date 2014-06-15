"""Read in configuration options from a project's Sundara config."""

import os
import shutil
from configparser import ConfigParser

from sundara import resources

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
        self.config = ConfigParser()
        self.config.read(project_conf)

    def get(self, section, option):
        return self.config.get(section, option)
