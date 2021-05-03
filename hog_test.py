import doctest
import importlib
import os
import pathlib
import pickle
import re
import subprocess
import sys
import time
import typing

import lab2
import utils.models

_unlocked_tests = pathlib.Path('assets/tests')


class HogProj:
    def __init__(self, student: utils.models.Student):
        self.student = student
        self.hog_root = self.get_hog_root().relative_to(utils.BASE_DIR)  # relative path
        self.ok_history: typing.Optional[dict] = None

        self.tests_dir = self.hog_root / 'tests'
        self.original_tests = self.hog_root / '~original-tests'

    @property
    def hog_py(self) -> pathlib.Path:
        path = utils.BASE_DIR / self.hog_root / 'hog.py'
        if not path.exists():
            raise FileNotFoundError(f"cannot find 'hog.py' in student {self.student.firstname}")
        return path

    def get_hog_root(self) -> pathlib.Path:
        # absolute PATH
        path = utils.BASE_DIR / f'assets/submissions/{self.student.firstname}/hog'
        if not path.exists():
            raise FileNotFoundError(f"hog root for {self.student.firstname} not found")
        return path

    def unlock_tests(self):
        os.chdir(utils.BASE_DIR)
        if self.original_tests.exists():
            raise ValueError("Already unlocked!")
        subprocess.run(['wsl', 'mv', self.tests_dir.as_posix(), self.original_tests.as_posix()], check=True)
        subprocess.run(['wsl', 'cp', '-r', _unlocked_tests.as_posix(), self.tests_dir.as_posix()], check=True)

    def restore_tests(self):
        os.chdir(utils.BASE_DIR)
        if not self.original_tests.exists():
            raise ValueError("Can't find original tests")
        subprocess.run(['wsl', 'rm', '-rf', self.tests_dir.as_posix()], check=True)
        subprocess.run(['wsl', 'mv', self.original_tests.as_posix(), self.tests_dir.as_posix()], check=True)

    def count_locked(self) -> typing.Dict[int, typing.Dict[bool, int]]:
        dct = dict()
        for i in range(13):
            file = utils.BASE_DIR / self.tests_dir / f'{i:0>2}.py'
            if not file.exists():
                raise FileNotFoundError(f"Cannot find '{file}' for student '{self.student.firstname}'")
            dct[i] = dict()
            with file.open('r') as f:
                contents = f.read()
                dct[i][True] = contents.count("'locked': True")
                dct[i][False] = contents.count("'locked': False")
        return dct

    # q_re = re.compile(r'-{69}\nQuestion (\d+)\n {4}Passed: (\d+)\n {4}Failed: (\d+)')

    def run_ok(self) -> typing.Tuple[typing.Dict[int, typing.Any], str]:
        self.chdir()
        scp = subprocess.run(['py', 'ok', '--score', '--local'], capture_output=True)
        out = scp.stdout.decode()
        qs = dict()
        # print(out)
        for line in out.splitlines():
            try:
                if line.startswith('Question ') and 'Suite' not in line and 'Case' not in line:
                    question = int(line[len('Question '):])
                    continue
                if line.startswith('    Passed: '):
                    passed = int(line[len('    Passed: '):])
                    continue
                if line.startswith('    Failed: '):
                    failed = int(line[len('    Failed: '):])
                    continue
                if line.startswith('[') and line.endswith('passed'):
                    qs[question] = {'passed': passed, 'failed': failed}
                    del question, passed, failed
                    continue
                if line.startswith('    Question '):
                    question = int(line.split(' ')[-2][:-1])
                    qs[question]['score'] = line.split(' ')[-1].split('/')[0]
                    continue
                if line.startswith('    Total: '):
                    total = line[len('    Total: '):]
                    continue
            except Exception:
                print(out)
                raise
        # print(out)
        return qs, total

    def open_ok_history(self) -> dict:
        ok_history = utils.BASE_DIR / self.hog_root / '.ok_history'
        if not ok_history.exists():
            raise FileNotFoundError(".ok_history not found")
        with ok_history.open('rb') as binfile:
            history = pickle.loads(binfile.read())
            if not isinstance(history, dict):
                print(history)
                raise ValueError(".ok_history not a pickle of dict")
            self.ok_history = history
            return self.ok_history

    def chdir(self):
        os.chdir(self.get_hog_root())

    def run_doctest(self) -> typing.Tuple[int, int]:
        sys.path.append(self.hog_root.as_posix())
        mod = importlib.import_module('hog')
        importlib.reload(mod)
        fail, all = doctest.testmod(mod)
        sys.path.remove(self.hog_root.as_posix())
        return fail, all
