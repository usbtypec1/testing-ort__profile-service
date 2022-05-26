from environs import Env

env = Env()
env.read_env()

DATABASE_URL: str = env.str('DATABASE_URL')
SECRET_KEY: str = env.str('SECRET_KEY')
