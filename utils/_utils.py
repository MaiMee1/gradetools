import csv
from pathlib import Path
from typing import List, AnyStr, TypeVar, Type

from utils import models

BASE_DIR = Path(__file__).absolute().parent.parent
# Keep this file in utils/_utils.py, else ^ would not work

T = TypeVar('T')


def get_all_students(model: Type[T] = models.Student) -> list[T]:
    """
    Get all students from the csv file.

    Data in each rows in the csv file is directly passed to `model` to
    create objects. If you use custom models be sure to match the init
    with the format of the csv file.
    """
    students = []
    with open(BASE_DIR / 'assets/students.csv', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0].startswith('#'):
                continue
            students.append(model(*row))
    return students


def get_submissions(pattern: str) -> List[AnyStr]:
    """
    Returns content of files matching pattern in the submissions folder.
    """
    files = []
    for file in Path.glob(BASE_DIR / 'assets/submissions', pattern):
        files.append(file.open().read())
    return files
