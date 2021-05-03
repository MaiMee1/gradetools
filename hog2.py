import itertools
import os
import pathlib
import pprint
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


def run_ok():
    with open('ok-res-2.csv', 'w') as file:
        students = utils.get_all_students(utils.models.Student)
        rs = []
        for student in students:
            try:
                student_proj = HogProj(student)
            except FileNotFoundError:
                continue

            ### Lock/unlock tests ###
            # student_proj.restore_tests()
            # student_proj.unlock_tests()

            qs, score = student_proj.run_ok()
            row = [student.firstname, score]
            ls = student_proj.count_locked()
            for i in range(13):
                row.append(qs[i]['score'])
                row.append(qs[i]['passed'])
                row.append(qs[i]['failed'])
                row.append(ls[i][True])
                row.append(ls[i][False])
            line = ','.join(map(str, row))
            print(line)
            file.write(line + '\n')
            file.flush()
            # break

if __name__ == '__main__':
    with open('doctest-res.csv', 'w') as file:
        students = utils.get_all_students(utils.models.Student)
        rs = []
        for student in students:
            try:
                student_proj = HogProj(student)
            except FileNotFoundError:
                continue
            # student_proj.chdir()
            # print(student.firstname)

            ### ok history ###
            # try:
            #     hist = proj.open_ok_history()
            # except FileNotFoundError:
            #     print(student.firstname, 'N', '', '', sep=',')
            #     continue
            # print(student.firstname, 'Y', hist['all_attempts'], hist['question'][0].split(' ')[1] if len(hist['question']) > 0 else '', sep=',')

            ## SHOW COMMIT MESSAGE SHORTLY ###
            # count commits in master
            # cps = subprocess.run(['git', 'rev-list', '--count', 'master'], capture_output=True)
            # print(cps.stdout.decode())

            # Show more info than rev-list
            # cps = subprocess.run(['git', 'shortlog', 'master'], capture_output=True)
            # file.write(cps.stdout)
            # file.write(bytes('^'*10 + student.firstname + '^'*10 + '\n', encoding='utf-8'))
            # print(cps.stdout.decode())

            # student_proj.restore_tests()
            # student_proj.unlock_tests()
            if student.firstname == 'Thakonwan':
                continue
            try:
                fail, all = student_proj.run_doctest()
                print(f"{student.firstname},{fail},{all}")
                file.write(f"{student.firstname},{fail},{all}\n")
            except IndentationError:
                print(f"{student.firstname},IndentationError,IndentationError")
                file.write(f"{student.firstname},IndentationError,IndentationError\n")
            file.flush()
            # break
