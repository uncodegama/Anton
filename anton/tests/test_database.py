import os
import anton.utils.database as aud


def test_find_db_file():
    path = os.path.join(os.getcwd(), "Anton1.db")

    open(path, "a").close()

    assert aud.find_db_file("Anton1.db") == path
