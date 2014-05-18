#!/usr/bin/env python3
"""Sundara jāla
   For a beautiful web.

   git.py
   Interface with git, so Sundara projects can be managed as git repos.
"""

import subprocess

def run(command):
    """command shoule be a list"""
    subprocess.call("git", command)
