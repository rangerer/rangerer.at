#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *


env.use_ssh_config = True
env.hosts = ['web01.rangerer.at']


def deploy():
    archive = '/tmp/rangerer.at.tar.gz'
    pip = '/usr/local/lib/pythonenv/rangerer-at-www/bin/pip'
    local('git archive -o {} HEAD'.format(archive))
    put(archive, archive)
    with cd('/srv/www/rangerer.at/www/'):
        run('tar xzf {}'.format(archive))
        sudo('{} install -r requirements.txt'.format(pip))
        run('rm requirements.txt')
    sudo('apache2ctl graceful')
    run('rm {}'.format(archive))
    local('rm {}'.format(archive))
