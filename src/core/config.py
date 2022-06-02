import pathlib

from environs import Env

env = Env()
env.read_env()

SRC_DIR = pathlib.Path(__file__).parent.parent
QUIZZES_DIR = SRC_DIR.parent / 'quizzes'

DATABASE_URL: str = env.str('DATABASE_URL')
SECRET_KEY: str = env.str('SECRET_KEY')
