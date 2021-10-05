from sys import argv

from ini_db import ini_db

_, db_name = argv
ini_db(db_name)
