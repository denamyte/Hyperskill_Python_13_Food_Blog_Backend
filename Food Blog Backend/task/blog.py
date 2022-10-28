import argparse
from typing import List

from ini_db import ini_db
from blog_search import blog_search
from blog_fill import blog_fill


def split(s: str) -> List[str]:
    return s.split(',') if s else []


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('db_name', help='The database name')
    parser.add_argument('--ingredients', help='The ingredients list to search for')
    parser.add_argument('--meals', help='The meals list to search for')
    args = parser.parse_args()
    db_name = args.db_name

    ini_db(db_name)

    if args.ingredients or args.meals:
        blog_search(db_name, split(args.ingredients), split(args.meals))
    else:
        blog_fill(db_name)
