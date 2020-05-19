import os
import shutil
from datetime import datetime
from pathlib import Path


def check_files_exist(paths):
    not_found = []
    for _ in paths:
        if not os.path.exists(_):
            not_found.append(_)
    return len(not_found) == 0, not_found


def check_dirs_exist(paths):
    not_found = []
    for _ in paths:
        dir = _[:_.rfind('/')]
        if not os.path.exists(dir):
            not_found.append(dir)
    return len(not_found) == 0, not_found


def remove_existing_files(paths):
    for _ in paths:
        if os.path.exists(_):
            os.remove(_)


def folder_structure_from_date(date=None):
    if date is None:
        date = datetime.utcnow()
    try:
        date_folder = date.strftime("d=%Y-%m-%d/h=%H")
        return date_folder
    except Exception as error:
        raise error


def move_dirs(dir_names_to_move, org_dir, dest_dir):
    list_dir = os.listdir(org_dir)
    for sub_dir in list_dir:
        if sub_dir in dir_names_to_move:
            dir_to_move = os.path.join(org_dir, sub_dir)
            shutil.move(dir_to_move, dest_dir)


def get_project_root():
    """Returns project root folder."""
    return str(Path(__file__).parent.parent.parent) + '/'


if __name__ == '__main__':
    # move_dirs(["employment_projections","oes", "education"], Config.DIR_DATA, os.path.join(Config.DIR_DATA, DIR.XL))

    # path = os.path.join("", "")
    # print(f'path="{path}"')

    pass
