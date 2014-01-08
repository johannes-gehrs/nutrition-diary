from __future__ import absolute_import, division, unicode_literals
from fabric.api import run, cd, env

env.hosts = ['root@srv.gehrs.me']

def deploy():
    code_dir = '/usr/share/nutrition-diary'
    with cd(code_dir):
        run("git pull")
        run("/etc/init.d/gunicorn reload")
