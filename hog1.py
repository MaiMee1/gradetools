import itertools
import pathlib
import subprocess

import diff
import utils
from prog.hog import HogProj


students = utils.get_all_students(utils.models.Student)
projects = [HogProj(s) for s in students]


def print_sim_to_original():
    rs = []
    for student in students:
        file = pathlib.Path(f'assets/submissions/{student.firstname}/hog/hog.py')
        if not file.exists(): continue
        d, r = diff.check_diff(pathlib.Path(f'assets/hog.py'),
                               file,
                               False)
        print(f'{student.firstname},{r:.3f}')
        rs.append(r)
    print(f'average: {sum(rs) / len(rs)}')


def print_sim_to_friends():
    record_file = open(f'recordfile.txt', 'w')
    record_file.write(f'2021-05-03\n')
    combinations = itertools.combinations(students, 2)
    diff.func(combinations, lambda s: pathlib.Path(f'assets/submissions/{s.firstname}/hog/hog.py'), record_file, cutoff=-1)


def print_commit_messages():
    for proj in projects:
        proj.chdir()
        print(proj.student.firstname)

        # count commits in master
        # cps = subprocess.run(['git', 'rev-list', '--count', 'master'], capture_output=True)
        # print(cps.stdout.decode())

        # Show more info than rev-list
        cps = subprocess.run(['git', 'shortlog', 'master'], capture_output=True)
        # file.write(cps.stdout)
        # file.write(bytes('^'*10 + student.firstname + '^'*10 + '\n', encoding='utf-8'))
        print(cps.stdout.decode())


def print_ok_history():
    for student in students:
        proj = HogProj(student)
        try:
            hist = proj.open_ok_history()
        except FileNotFoundError:
            print(student.firstname, 'N', '', '', sep=',')
            continue
        print(student.firstname, 'Y', hist['all_attempts'], hist['question'][0].split(' ')[1] if len(hist['question']) > 0 else '', sep=',')


def restore_all():
    for proj in projects:
        try:
            proj.restore_tests()
        except ValueError:
            pass


def unlock_all():
    for proj in projects:
        try:
            proj.unlock_tests()
        except ValueError:
            pass


def run_ok():
    with open('ok-res-2.csv', 'w') as file:
        for proj in projects:
            qs, score = proj.student.run_ok()
            row = [proj.student.firstname, score]
            ls = proj.student.count_locked()
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


def print_doctest_to_csv(filename: str = 'doctest-res.csv'):
    with open(filename, 'w') as file:
        for proj in projects:
            try:
                fail, all = proj.run_doctest()
                print(f"{proj.student.firstname},{fail},{all}")
                file.write(f"{proj.student.firstname},{fail},{all}\n")
            except IndentationError:
                print(f"{proj.student.firstname},IndentationError,IndentationError")
                file.write(f"{proj.student.firstname},IndentationError,IndentationError\n")
            file.flush()


if __name__ == '__main__':
    pass
