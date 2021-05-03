import subprocess
import typing
from typing import Iterable

from .berkeley import OkProj


def print_commit_messages(projects: Iterable[OkProj], file: typing.IO = None):
    for proj in projects:
        proj.chdir()
        print('v'*10 + '  ' + proj.student.firstname + '  ' + 'v'*10, file=file)
        print(file=file)

        # count commits in master
        # cps = subprocess.run(['git', 'rev-list', '--count', 'master'], capture_output=True)
        # print(cps.stdout.decode(), file=file)

        # Show more info than rev-list
        cps = subprocess.run(['git', 'shortlog', 'master'], capture_output=True)
        print(cps.stdout.decode(), file=file)


def print_ok_history(projects: Iterable[OkProj], file: typing.IO = None):
    for proj in projects:
        try:
            hist = proj.open_ok_history()
        except FileNotFoundError:
            print(proj.student.firstname, 'N', '', '', sep=',', file=file)
            continue
        print(proj.student.firstname, 'Y', hist['all_attempts'], hist['question'][0].split(' ')[1] if len(hist['question']) > 0 else '', sep=',', file=file)


def restore_all(projects: Iterable[OkProj]):
    for proj in projects:
        try:
            proj.restore_tests()
        except ValueError:
            pass


def unlock_all(projects: Iterable[OkProj]):
    for proj in projects:
        try:
            proj.unlock_tests()
        except ValueError:
            pass


def run_ok(csvfile: str, projects: Iterable[OkProj]):
    with open(csvfile, 'w') as file:
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


def print_doctest_to_csv(csvfile: str, projects: Iterable[OkProj]):
    with open(csvfile, 'w') as file:
        for proj in projects:
            try:
                fail, all = proj.run_doctest()
                print(f"{proj.student.firstname},{fail},{all}")
                file.write(f"{proj.student.firstname},{fail},{all}\n")
            except IndentationError:
                print(f"{proj.student.firstname},IndentationError,IndentationError")
                file.write(f"{proj.student.firstname},IndentationError,IndentationError\n")
            file.flush()

# reusable
#
# def print_sim_to_original(students: Iterable[utils.models.Student]):
#     rs = []
#     for student in students:
#         file = pathlib.Path(f'assets/submissions/{student.firstname}/hog/hog.py')
#         if not file.exists(): continue
#         d, r = diff.check_diff(pathlib.Path(f'assets/hog.py'),
#                                file,
#                                False)
#         print(f'{student.firstname},{r:.3f}')
#         rs.append(r)
#     print(f'average: {sum(rs) / len(rs)}')
#
#
# def print_sim_to_friends(projects: Iterable[OkProj]):
#     record_file = open(f'../recordfile.txt', 'w')
#     record_file.write(f'2021-05-03\n')
#     combinations = itertools.combinations([p.student for p in projects], 2)
#     diff.func(combinations, lambda s: pathlib.Path(f'assets/submissions/{s.firstname}/hog/hog.py'), record_file, cutoff=-1)
