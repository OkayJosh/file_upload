"""
Module: file_repository

This module defines the `FileRepository` class, which implements the
`FileRepository` interface for managing file storage in the local file system.
The `FileRepository` is responsible for saving file chunks to a specified upload
directory and ensuring that the directory exists before performing any file operations.

This implementation follows the interfaces and adapters architecture, allowing the
application to interact with the file system through an abstract interface.

Example Use Case:
    - Storing uploaded files in a local directory while allowing for potential
      future adaptation to different storage mechanisms (e.g., cloud storage).
"""

import os

from application.interfaces.file_repository import FileRepository
from domain.entity import FileEntity

UPLOAD_DIR = "uploads"  # Directory where uploaded files will be stored.

class File(FileRepository):
    """
    FileRepository is an implementation of the FileRepository interface,
    providing methods for saving file chunks to the local file system. This class
    manages the file storage operations and ensures that the required upload directory
    is created if it does not exist.

    Attributes:
        None
    """

    def __init__(self):
        """
        Initialize the FileRepository and create the upload directory if it doesn't exist.

        This constructor checks for the existence of the designated upload directory
        and creates it if it is not present, ensuring that file operations can proceed
        without errors related to missing directories.
        """
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

    def save_file_chunk(self, file_entity: FileEntity, offset: int, chunk_size: int):
        """
        Save a chunk of the file to the local file system.

        This method appends a specific chunk of the file content, defined by the
        offset and chunk size, to the designated file in the upload directory.

        Args:
            file_entity (FileEntity): The file entity containing the file's metadata
                                      and content that needs to be stored.
            offset (int): The starting position in the file content from which to
                          save the chunk.
            chunk_size (int): The size of the chunk to be saved.

        Raises:
            IOError: If there is an error during the file writing process.
        """
        file_path = os.path.join(UPLOAD_DIR, file_entity.filename)
        with open(file_path, 'ab') as f:  # Open the file in append-binary mode.
            f.write(file_entity.content[offset:offset + chunk_size])
