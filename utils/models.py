from __future__ import annotations

from typing import Union


class Student:
    """
    Represents a KU student
    """
    def __init__(self, student_id: Union[int, str], name_en: str, name_th: str):
        self._student_id: str = str(student_id)
        self._name_en: str = name_en
        self._name_th: str = name_th

    @property
    def id(self):
        return self._student_id

    @property
    def name(self):
        return self._name_en

    def __str__(self):
        return f'{self.id}_{self.name}'

    def __eq__(self, other: Student):
        try:
            return self._student_id == other._student_id
        except AttributeError:
            return False
