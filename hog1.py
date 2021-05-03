import itertools
import os
import pathlib
import subprocess

import diff
import utils
from hog_test import HogProj


def print_sim_to_original():
    students = utils.get_all_students(utils.models.Student)
    rs = []
    for student in students:
        # proj = HogProj(student)
        # proj.chdir()
        # print(student.firstname)
        file = pathlib.Path(f'assets/submissions/{student.firstname}/hog/hog.py')
        if not file.exists(): continue
        d, r = diff.check_diff(pathlib.Path(f'assets/hog.py'),
                               file,
                               False)
        print(f'{student.firstname},{r:.3f}')
        rs.append(r)
    print(f'average: {sum(rs) / len(rs)}')


if __name__ == '__main__':
    students = utils.get_all_students(utils.models.Student)
    rs = []
    for student in students:
        break
        proj = HogProj(student)
        # proj.chdir()
        # print(student.firstname)

        ### SHOW COMMIT MESSAGE SHORTLY ###
        # count commits in master
        # cps = subprocess.run(['git', 'rev-list', '--count', 'master'], capture_output=True)
        # print(cps.stdout.decode())

        # Show more info than rev-list
        # cps = subprocess.run(['git', 'shortlog', 'master'], capture_output=True)
        # print(cps.stdout.decode())

        ### RUN ok score ###
        # cps = subprocess.run(['py', 'ok', '-q', '01', '--score', '--local'], capture_output=True)
        # print(cps.stdout.decode())

        ### Lock/unlock tests ###
        # proj.unlock_test()
        # proj.revert_test()
        # break

    record_file = open(f'recordfile.txt', 'w')
    record_file.write(f'2021-05-03\n')
    combinations = itertools.combinations(students, 2)
    diff.func(combinations, lambda s: pathlib.Path(f'assets/submissions/{s.firstname}/hog/hog.py'), record_file, cutoff=-1)
