
import os
import sys

import nose
from nose.config import Config, all_config_files
from nose.plugins.manager import DefaultPluginManager

import kiko

app_name = sys.argv[1]

unit_test = None
if len(sys.argv) > 2:
    unit_test = sys.argv[2]

if app_name == 'maya':
    from units import maya as app_specific
    from maya import standalone
    standalone.initialize(name='python')
    from maya import cmds

elif app_name == 'nuke':
    from units import nuke as app_specific
    import nuke
elif app_name == 'houdini':
    pass

os.environ['KIKO_APP_NAME'] = app_name

kiko.initialize()

current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
nose_config = os.path.join(current_dir, 'config', 'nose.cfg')
config_files = [nose_config] + all_config_files()
c = Config(env=os.environ, files=config_files, plugins=DefaultPluginManager())

app_s_loader = nose.loader.TestLoader()
if unit_test is None:
    app_s_suite = app_s_loader.loadTestsFromModule(app_specific)
else:
    app_s_suite = app_s_loader.loadTestsFromName(unit_test)

test_suite = nose.suite.ContextSuite()
test_suite.addTest(app_s_suite)

sys.exit(nose.main(config=c, suite=test_suite))


