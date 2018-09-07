
import os

_FILE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')

def get_app_file(app, file_name):
    f = os.path.join(_FILE_DIR, app, file_name)
    if not os.path.exists(f):
        raise RuntimeError("%s file %s does not exist" % (app, file_name))
    return f

def get_kiko_file(file_name):
    f = os.path.join(_FILE_DIR, 'kiko', file_name)
    if not os.path.exists(f):
        raise RuntimeError("Kiko file %s does not exist" % file_name)
    return f