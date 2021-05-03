import os
import pathlib
import pickle
import subprocess
import typing

import utils.models

_unlocked_tests = pathlib.Path('assets/tests')


class HogProj:
    def __init__(self, student: utils.models.Student):
        self.student = student
        self.hog_root = self.get_hog_root().relative_to(utils.BASE_DIR)
        self.ok_history: typing.Optional[dict] = None

        self.tests_dir = self.hog_root / 'tests'
        self.original_tests = self.hog_root / '~original-tests'

    def get_hog_root(self) -> pathlib.Path:
        # absolute PATH
        path = utils.BASE_DIR / f'assets/submissions/{self.student.firstname}/hog'
        if not path.exists():
            raise FileNotFoundError(f"hog root for {self.student.firstname} not found")
        return path

    def unlock_test(self):
        os.chdir(utils.BASE_DIR)
        if self.original_tests.exists():
            raise ValueError("Already unlocked!")
        subprocess.run(['wsl', 'mv', self.tests_dir.as_posix(), self.original_tests.as_posix()], check=True)
        subprocess.run(['wsl', 'cp', '-r', _unlocked_tests.as_posix(), self.tests_dir.as_posix()], check=True)

    def revert_test(self):
        os.chdir(utils.BASE_DIR)
        if not self.original_tests.exists():
            raise ValueError("Can't find original tests")
        subprocess.run(['wsl', 'rm', '-rf', self.tests_dir.as_posix()], check=True)
        subprocess.run(['wsl', 'mv', self.original_tests.as_posix(), self.tests_dir.as_posix()], check=True)

    def open_ok_history(self) -> dict:
        ok_history = self.hog_root / '.ok_history'

        os.chdir(utils.BASE_DIR)
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
