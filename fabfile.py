# This is specific to my personal deployment of the software and probably irrelevant to you (JG)

from __future__ import absolute_import, division, unicode_literals
from fabric.api import run, cd, env

env.hosts = ['root@srv.gehrs.me']

def deploy():
    code_dir = '/usr/share/nutrition-diary'
    with cd(code_dir):
        run("git pull")
        run("pip install --upgrade --requirement=requirements.txt")
        run("/etc/init.d/gunicorn reload")
