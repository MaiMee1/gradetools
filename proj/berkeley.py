import abc
import dataclasses
import doctest
import importlib
import os
import pathlib
import pickle
import re
import subprocess
import sys
import typing

import utils


class OkProj:
    _unlocked_tests = pathlib.Path('')

    def __init__(self, student: utils.models.Student):
        self.student = student
        self.proj_root = self.get_proj_root().relative_to(utils.BASE_DIR)  # relative path
        self.ok_history: typing.Optional[dict] = None

        self.tests_dir = self.proj_root / 'tests'
        self._cache_dir = self.proj_root / '.original'

    @property
    def cache_dir(self) -> pathlib.Path:
        """ Relative to utils.BASE_DIR """
        if not self._cache_dir.exists():
            self._cache_dir.mkdir()
        assert self._cache_dir.exists()
        return self._cache_dir

    @abc.abstractmethod
    def get_proj_root(self) -> pathlib.Path:
        # absolute PATH
        raise NotImplementedError

    @abc.abstractmethod
    def get_proj_xx_ok(self) -> pathlib.Path:
        raise NotImplementedError

    def unlock_tests(self):
        self.replace_original(self.tests_dir.relative_to(self.proj_root), self._unlocked_tests)

    def restore_tests(self):
        self.restore_original(self.tests_dir.relative_to(self.proj_root))

    def replace_original(self, original: str, replacement: pathlib.Path):
        """Replace original file at path

        :param original: file path relative to self.proj_root
        :param replacement: relative to utils.BASE_DIR
        """
        os.chdir(utils.BASE_DIR)  # wsl can't do absolute WindowsPath
        if (self.cache_dir / original).exists():
            raise ValueError("Already replaced!")
        subprocess.run(['wsl', 'mv', (self.proj_root / original).as_posix(), (self.cache_dir / original).as_posix()], check=True)
        subprocess.run(['wsl', 'cp', '-r', replacement.as_posix(), (self.proj_root / original).as_posix()], check=True)

    def restore_original(self, original: str):
        """Replace original file at path

        :param original: relative to self.proj_root
        """
        os.chdir(utils.BASE_DIR)  # To make it the same as above (parallelism)
        if not (self.cache_dir / original).exists():
            raise ValueError(f"Can't find cached original file '{self.cache_dir / original}' from '{self.cache_dir / original}'")
        subprocess.run(['wsl', 'rm', '-rf', (self.proj_root / original).as_posix()], check=True)
        subprocess.run(['wsl', 'mv', (self.cache_dir / original).as_posix(), (self.proj_root / original).as_posix()], check=True)

    @dataclasses.dataclass()
    class LockedResults:
        locked: int
        unlocked: int

    def count_locked_q(self, q: str):
        file = utils.BASE_DIR / self.tests_dir / f'{q}.py'
        if not file.exists():
            raise FileNotFoundError(f"Cannot find '{file}' for student '{self.student.firstname}'")
        with file.open('r') as f:
            contents = f.read()
            return self.LockedResults(
                locked=contents.count("'locked': True"),
                unlocked=contents.count("'locked': False"),
            )

    def count_locked(self, files: typing.List[str]) -> typing.Dict[str, typing.Dict[bool, int]]:
        dct = dict()
        for i in files:
            file = utils.BASE_DIR / self.tests_dir / f'{i}.py'
            if not file.exists():
                raise FileNotFoundError(f"Cannot find '{file}' for student '{self.student.firstname}'")
            if i.isnumeric():
                i = str(int(i))
            dct[i] = dict()
            with file.open('r') as f:
                contents = f.read()
                dct[i][True] = contents.count("'locked': True")
                dct[i][False] = contents.count("'locked': False")
        return dct

    # re1 = re.compile(r'-{69}\nQuestion (\d+)\n {4}Passed: (\d+)\n {4}Failed: (\d+)')  # old
    re2 = re.compile(r'-{69}\nProblem (.+)\n {4}Passed: (\d+)\n {4}Failed: (\d+)')  # 1 = Problem, 2 = Passed, 3 = Failed
    re3 = re.compile(r'-{69}\nPoint breakdown')
    re4 = re.compile(r' {4}Problem (.+): (\d+.\d+)/(\d+)\n')  # 1 = Problem, 2 = score, 3 = fullscore
    re5 = re.compile(r' {4}Total: (\d+.\d+)')  # 1 = total score

    @dataclasses.dataclass()
    class OkResults:
        question: str
        passed: int
        failed: int
        fullscore: int
        score: str

    def run_ok_q(self, q: str) -> OkResults:
        self.chdir()
        scp = subprocess.run(['py', 'ok', '-q', q, '--score', '--local'], capture_output=True)
        out = scp.stdout.decode().replace('\r\n', '\n')
        m = self.re2.search(out)
        m2 = self.re4.search(out)
        try:
            return self.OkResults(
            question=m.group(1),
            passed = int(m.group(2)),
            failed = int(m.group(3)),
            fullscore = int(m2.group(3)),
            score = m2.group(2),
        )
        except Exception:
            print(out)
            raise

    def run_ok(self) -> typing.Tuple[typing.Dict[str, typing.Any], str]:
        try:
            self.chdir()
            scp = subprocess.run(['py', 'ok', '--score', '--local'], capture_output=True)
            out = scp.stdout.decode()
            qs = dict()
            for m in self.re2.finditer(out):
                question = m.group(1)
                passed = int(m.group(2))
                failed = int(m.group(3))
                qs[question] = {'passed': passed, 'failed': failed}
            for m in self.re4.finditer(out[self.re3.search(out).span()[1]:]):
                question = m.group(1)
                score = m.group(2)
                fullscore = int(m.group(3))
                qs[question]['score'] = score
            total = self.re5.search(out).group(1)
            # print(qs)
        except Exception:
            print(out)
            raise
        return qs, total

        # for line in out.splitlines():
        #     try:
        #         if line.startswith('Question ') and 'Suite' not in line and 'Case' not in line:
        #             question = int(line[len('Question '):])
        #             continue
        #         if line.startswith('    Passed: '):
        #             passed = int(line[len('    Passed: '):])
        #             continue
        #         if line.startswith('    Failed: '):
        #             failed = int(line[len('    Failed: '):])
        #             continue
        #         if line.startswith('[') and line.endswith('passed'):
        #             qs[question] = {'passed': passed, 'failed': failed}
        #             del question, passed, failed
        #             continue
        #         if line.startswith('    Question '):
        #             question = int(line.split(' ')[-2][:-1])
        #             qs[question]['score'] = line.split(' ')[-1].split('/')[0]
        #             continue
        #         if line.startswith('    Total: '):
        #             total = line[len('    Total: '):]
        #             continue
        #     except Exception:
        #         print(out)
        #         raise
        # # print(out)
        # return qs, total

    def open_ok_history(self) -> dict:
        ok_history = utils.BASE_DIR / self.proj_root / '.ok_history'
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
        os.chdir(self.get_proj_root())

    def run_doctest(self) -> typing.Tuple[int, int]:
        sys.path.append(self.proj_root.as_posix())
        mod = importlib.import_module('hog')
        importlib.reload(mod)
        fail, all = doctest.testmod(mod)
        sys.path.remove(self.proj_root.as_posix())
        return fail, all
