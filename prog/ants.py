import pathlib

import prog.berkeley
import utils.models


class HogProj(prog.berkeley.OkProj):
    unlocked_tests = pathlib.Path('assets/ants/tests')

    def __init__(self, student: utils.models.Student):
        super(HogProj, self).__init__(student)

    def get_proj_root(self) -> pathlib.Path:
        # absolute PATH
        path = utils.BASE_DIR / f'assets/submissions/{self.student.firstname}/ants'
        if not path.exists():
            raise FileNotFoundError(f"project root for {self.student.firstname} not found")
        return path

    @property
    def ants_py(self) -> pathlib.Path:
        path = utils.BASE_DIR / self.proj_root / 'ants.py'
        if not path.exists():
            raise FileNotFoundError(f"cannot find 'ants.py' in student {self.student.firstname}")
        return path
