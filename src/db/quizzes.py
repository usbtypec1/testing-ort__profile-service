from datetime import datetime

from sqlalchemy import Integer, Column, String, Text, DateTime, ForeignKey, func

from db.engine import Base


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    quiz_file_path = Column(String, unique=True, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    created_by_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
