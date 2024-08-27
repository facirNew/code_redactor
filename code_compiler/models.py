from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TaskSolution(Base):
    __tablename__ = 'task_solution'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[int] = mapped_column(ForeignKey('task.id'))
    code: Mapped[str]
    status: Mapped[str]
    output: Mapped[str] = None


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str]
    body: Mapped[str]


class TaskData(Base):
    __tablename__ = 'task_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[int] = mapped_column(ForeignKey('task.id'))
    input_data: Mapped[str]
    output_data: Mapped[str]
