import pathlib
import subprocess

import utils
from utils.models import Student

students = utils.get_all_students(Student)
# _id_s_map = None
# _fn_s_map = None
#
#
# def get_student_from_firstname(firstname: int) -> Student:
#     global _fn_s_map
#     if _fn_s_map is None:
#         _fn_s_map = {s.firstname: s for s in students}
#     return _fn_s_map[firstname]
#
#
# def get_student_from_id(id: int) -> Student:
#     global _id_s_map
#     if _id_s_map is None:
#         _id_s_map = {s.id: s for s in students}
#     return _id_s_map[id]


def main():
    # EDIT THIS                                        ↓↓↓↓↓↓↓↓
    for directory in pathlib.Path(f'assets/submissions/lab2_ext').glob('*'):
        if not directory.is_dir():
            continue
        for s in students:
            if (s.id in directory.name
                    or s.firstname in directory.name):
                print(f'found student {s.firstname} at {directory.name}')
                break
        else:
            continue
        # EDIT THIS                                                                           ↓↓↓↓↓↓↓↓
        subprocess.run(['wsl', 'mv', directory.as_posix(), f'assets/submissions/{s.firstname}/lab2_ext'], check=True)


if __name__ == '__main__':
    main()
