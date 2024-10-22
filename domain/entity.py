"""
Module: file_entity

This module defines the `FileEntity` class, which represents a file in the
application. The `FileEntity` serves as a data transfer object (DTO) that holds
the essential information about a file being processed in the system, such as
its name and content.

The class utilizes Python's dataclass feature to provide a simple and efficient
way to define data structures with automatic generation of common methods such as
__init__, __repr__, and __eq__.

Example Use Case:
    - Representing files during upload processes, where the filename and content
      are required to manage file storage and processing operations.
"""

from dataclasses import dataclass


@dataclass
class FileEntity:
    """
    FileEntity is a data class that represents a file with its associated
    metadata and content. This class serves as a container for the information
    needed to handle file uploads, storage, and processing in the application.

    Attributes:
        filename (str): The name of the file, including its extension.
        content (bytes): The raw byte content of the file to be processed or stored.
    """

    filename: str
    content: bytes

