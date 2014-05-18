"""Sundara jāla: for a beautiful web.

Interface with git, so Sundara projects can be managed as git repos.
"""

import subprocess

def run(command):
    """command shoule be a list"""
    subprocess.call("git", command)
