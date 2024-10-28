"""
Module: infrastructure.adapters.db_file_repository

This module implements the DbFile class, which is responsible for
interfacing with the database to store and retrieve file data. It adheres to the
FileRepository interface defined in the application layer, ensuring a consistent
contract for file storage functionality.

The repository uses TortoiseORM with an asynchronous setup to handle database
operations efficiently.

Usage:
    To use this repository, instantiate the SQLAlchemyFile class and
    call its methods to save or retrieve file chunks.
"""
from typing import TYPE_CHECKING, Union

from application.interfaces.file_repository import FileRepository
from domain.entity import FileEntity

if TYPE_CHECKING:
    from infrastructure.models.file_model import FileModel


_FileEntity = Union[FileEntity, None]

class DBFile(FileRepository):
    """
    DBFile is an implementation of the FileRepository
    interface that utilizes Tortoise ORM to persist file data in a SQLite database asynchronously.

    Attributes:
        None: Uses Tortoise ORM for database interactions.
    """

    async def save_file_chunk(self, file_entity: FileEntity, offset: int, chunk_size: int) -> None:
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
        from infrastructure.models.file_model import FileModel

        file_record = await FileModel.get_or_none(filename=file_entity.filename)

        if file_record:

            existing_content = file_record.content
            updated_content = existing_content + file_entity.content[offset:offset + chunk_size]
            file_record.content = updated_content
        else:

            file_record = FileModel(
                filename=file_entity.filename,
                content=file_entity.content[offset:offset + chunk_size]
            )

        await file_record.save()

    async def get_file(self, filename: str) -> _FileEntity:
        """
        Retrieves a file from the database by its filename.

        Args:
            filename (str): The name of the file to retrieve.

        Returns:
            _FileEntity: Either an instance of FileEntity containing the file's name and content or None.

        Raises:
            Exception: If there is an error while retrieving the file from the database.
        """
        from infrastructure.models.file_model import FileModel

        file_record = await FileModel.get_or_none(filename=filename)

        if file_record:
            return FileEntity(filename=file_record.filename, content=file_record.content)

        return None
