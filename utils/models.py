from __future__ import annotations

from typing import Union


class Student:
    """
    Represents a KU student
    # Firstname,Github,Name,ID,Email

    """
    def __init__(self, firstname_en: str, github: str, name_en: str, student_id: Union[int, str], email: str):
        self._student_id: str = str(student_id)
        self._firstname_en: str = firstname_en
        self._name_en: str = name_en
        self._github: str = github
        self._email: str = email

    @property
    def id(self) -> str:
        return self._student_id

    @property
    def firstname(self) -> str:
        return self._firstname_en

    @property
    def name(self) -> str:
        return self._name_en

    @property
    def github(self) -> str:
        return self._github

    def __repr__(self):
        return f'{self.id}_{self.firstname}'

    def __eq__(self, other: Student):
        try:
            return self._student_id == other._student_id
        except AttributeError:
            return False
