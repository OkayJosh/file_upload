"""
Module: infrastructure.adapters.sqlalchemy_file_repository

This module implements the SQLAlchemyFileRepository class, which is responsible for
interfacing with the database to store and retrieve file data. It adheres to the
FileRepositoryPort interface defined in the application layer, ensuring a consistent
contract for file storage functionality.

The repository uses SQLAlchemy with an asynchronous setup to handle database
operations efficiently.

Usage:
    To use this repository, instantiate the SQLAlchemyFileRepository class and
    call its methods to save or retrieve file chunks.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from application.ports.file_repository import FileRepositoryPort
from domain.entity import FileEntity
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from infrastructure.models.file_model import FileModel
from infrastructure.settings import settings

Base = declarative_base()


class SQLAlchemyFileRepository(FileRepositoryPort):
    """
    SQLAlchemyFileRepository is an implementation of the FileRepositoryPort
    interface that utilizes SQLAlchemy to persist file data in a PostgreSQL
    database asynchronously.

    Attributes:
        engine (AsyncEngine): The SQLAlchemy async engine for database connections.
        SessionLocal (sessionmaker): A session factory for creating new database sessions.

    Usage:
        repository = SQLAlchemyFileRepository()
        await repository.save_file_chunk(file_entity, offset, chunk_size)
        file_entity = await repository.get_file(filename)
    """

    def __init__(self):
        """
        Initializes the SQLAlchemyFileRepository instance.

        This constructor creates an asynchronous database engine and a session
        factory using the database URL specified in the settings module.
        The echo parameter is set to True for logging SQL statements.

        Raises:
            Exception: If there is an issue creating the database engine.
        """
        self.engine = create_async_engine(settings.DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def save_file_chunk(self, file_entity: FileEntity, offset: int, chunk_size: int):
        """
        Saves a chunk of a file to the database. If a file with the same filename
        already exists, this method appends the new chunk to the existing content.

        Args:
            file_entity (FileEntity): The entity representing the file to be saved.
            offset (int): The starting index from which to read the content chunk.
            chunk_size (int): The size of the chunk to be saved.

        Raises:
            Exception: If there is an error while saving the file chunk to the database.
        """
        async with self.SessionLocal() as session:
            file_model = await session.execute(select(FileModel).where(FileModel.filename == file_entity.filename))
            file_record = file_model.scalar_one_or_none()

            if file_record:
                # If the file already exists, we can append to it
                existing_content = file_record.content
                updated_content = existing_content + file_entity.content[offset:offset + chunk_size]
                file_record.content = updated_content
            else:
                # Create new file record
                file_record = FileModel(filename=file_entity.filename, content=file_entity.content[offset:offset + chunk_size])
                session.add(file_record)

            await session.commit()

    async def get_file(self, filename: str) -> FileEntity:
        """
        Retrieves a file from the database by its filename.

        Args:
            filename (str): The name of the file to retrieve.

        Returns:
            FileEntity: An instance of FileEntity containing the file's name and content.
            None: If the file with the given filename does not exist.

        Raises:
            Exception: If there is an error while retrieving the file from the database.
        """
        async with self.SessionLocal() as session:
            file_model = await session.execute(select(FileModel).where(FileModel.filename == filename))
            file_record = file_model.scalar_one_or_none()
            if file_record:
                return FileEntity(filename=file_record.filename, content=file_record.content)
            return None
