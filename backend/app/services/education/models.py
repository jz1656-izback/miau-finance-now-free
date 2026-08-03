"""Education platform — course content models, SQLAlchemy ORM."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Course(Base):
    __tablename__ = 'education_courses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, server_default=text("''"))
    category = Column(String(64), server_default=text("'general'"))
    difficulty = Column(String(16), server_default=text("'beginner'"))
    icon = Column(String(8), server_default=text("'📚'"))
    lesson_count = Column(Integer, server_default=text('0'))
    estimated_minutes = Column(Integer, server_default=text('0'))
    order_index = Column(Integer, server_default=text('0'))
    is_published = Column(Boolean, server_default=text('TRUE'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))


class Lesson(Base):
    __tablename__ = 'education_lessons'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey('education_courses.id', ondelete='CASCADE'), nullable=False)
    slug = Column(String(64), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, server_default=text("''"))
    content_type = Column(String(32), server_default=text("'markdown'"))
    order_index = Column(Integer, server_default=text('0'))
    estimated_minutes = Column(Integer, server_default=text('5'))
    is_published = Column(Boolean, server_default=text('TRUE'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))


class Quiz(Base):
    __tablename__ = 'education_quizzes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('education_lessons.id', ondelete='CASCADE'), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(Text, nullable=False)  # JSON array of options
    correct_index = Column(Integer, nullable=False)
    explanation = Column(Text, server_default=text("''"))
    order_index = Column(Integer, server_default=text('0'))


class Enrollment(Base):
    __tablename__ = 'education_enrollments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('education_courses.id', ondelete='CASCADE'), nullable=False)
    progress_pct = Column(Numeric(5, 2), server_default=text('0'))
    completed_lessons = Column(Integer, server_default=text('0'))
    quiz_score = Column(Numeric(5, 2), server_default=text('0'))
    is_completed = Column(Boolean, server_default=text('FALSE'))
    certificate_id = Column(String(64))
    enrolled_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    completed_at = Column(DateTime(timezone=True))

    __table_args__ = ()
