import os

from importerlibs.utils.file_utils import get_project_root


class Constants:
    TIMEOUT_CONNECT = 60
    TIMEOUT_READ = 60
    HEADER_ACCEPT_JSON = {'Accept': 'application/json'}
    ROOT = get_project_root()
    FILES = os.path.join(ROOT, "files")

    API = "api"
