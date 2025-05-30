from src.ai import db_manager
from src.ai import ai

import sys
import os


def check_init_db(argv):
    if "-init_db" in argv:
        if os.path.exists("db/") == False:
            os.mkdir("db/")
        db_manager.create_vector_db("data/", "db/")
        

check_init_db(sys.argv)


QA_CHAIN = ai.set_qa_chain("db/")

ai.get_answer(QA_CHAIN, "What is the name of the company?")