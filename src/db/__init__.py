from .users import User
from .quizzes import Quiz
from .engine import Base

Base.metadata.create_all()
