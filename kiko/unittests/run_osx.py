#!/usr/bin/env python2.7

# ==============================================================================
#
# KIKO is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version. This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
# for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================

import os
import subprocess

from argparse import ArgumentParser
from distutils.spawn import find_executable

import sys
import nose
from nose.config import Config, all_config_files

from nose.plugins.manager import DefaultPluginManager

from units import standalone

class TestsFailed(Exception):
    pass

MAYAPY_EXC = 'mayapy'
NUKE_EXC = 'Nuke9.0'


ALL_APPS = ['standalone', 'maya', 'nuke']

current_dir = os.path.dirname(os.path.realpath(__file__))
nose_config = os.path.join(current_dir, 'config', 'nose.cfg')
config_files = [nose_config] + all_config_files()
c = Config(env=os.environ, files=config_files, plugins=DefaultPluginManager())

nose_app = os.path.join(current_dir, 'bin', 'nose_app.py')
module_test = None

if len(sys.argv) == 1:
    apps = ALL_APPS
else:
    _, module_test, unit_test_name = nose.util.split_test_name(sys.argv[1])
    apps = [module_test.split('.')[1]]

for app in apps:
    print "\x1b[1;33mRunning %s tests \x1b[0m" % app

    if app == 'standalone':
        loader = nose.loader.TestLoader()
        if module_test is None:
            suite = loader.loadTestsFromModule(standalone)
        else:
            suite = loader.loadTestsFromName(sys.argv[1])

        result = nose.run(config=c, suite=suite)

    elif app == 'maya':
        if find_executable(MAYAPY_EXC):
            cmds = [MAYAPY_EXC, nose_app, app]
            if module_test is not None:
                cmds += [sys.argv[1]]
            p = subprocess.Popen(cmds, stdout=sys.stdout, stderr=sys.stderr)
            out, err = p.communicate()
            result = p.returncode == 0

    elif app == 'nuke':
        if find_executable(NUKE_EXC):
            cmds = [NUKE_EXC, '-x', nose_app, app]
            if module_test is not None:
                cmds += [sys.argv[1]]

            print ' '.join(cmds)

            p = subprocess.Popen(cmds, stdout=sys.stdout, stderr=sys.stderr)
            out, err = p.communicate()
            result = p.returncode == 0

    if not result:
        print "\x1b[1;31mUNIT TESTS FAILED\x1b[0m"
        raise TestsFailed("Tests Failed.")

print "\x1b[1;33mUNIT TESTS SUCCESSFULL\x1b[0m"
