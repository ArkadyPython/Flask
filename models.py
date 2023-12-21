import os
import datetime
import atexit
from sqlalchemy import create_engine, DateTime, String, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped

POSTGRES_USER = os.getenv("POSTGRES_USER", "arkady")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")


PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

class Advertisement(Base):

    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(200), index=True, nullable=False)

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "registration_time": self.registration_time.isoformat(),
            "owner": self.owner
        }

Base.metadata.create_all(bind=engine)
atexit.register(engine.dispose)
