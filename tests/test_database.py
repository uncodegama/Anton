import os
from src.database import find_db_file


def test_find_db_file():
    path = os.getcwd() + "Anton1.db"

    open(path, "a").close()

    assert find_db_file("Anton1.db") == path
