from src.ai import db_manager

import sys
import os


def check_init_db(argv):
    if "-init_db" in argv:
        db_manager.create_vector_db("data/", "db/")
        

check_init_db(sys.argv)