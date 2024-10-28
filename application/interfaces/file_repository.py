from typing import Protocol

from domain.entity import FileEntity


class FileRepository(Protocol):
    """
    FileRepository defines an interface for file repository Implementation.
    It acts as a port in the interfaces and adapters
    pattern, providing an interface that different storage mechanisms (e.g., local
    storage, cloud storage like S3) must implement.

    The key responsibility of this port is to provide a method for saving file chunks
    progressively, allowing large files to be saved in smaller parts (chunks).

    This abstraction enables the application to interact with different storage
    mechanisms without being tied to a specific storage implementation.
    """

    def save_file_chunk(self, file_entity: FileEntity, offset: int, chunk_size: int) -> None:
        """
        Save a chunk of a file to the repository.

        This method must be implemented by any class that inherits from FileRepository.
        It is responsible for saving part of a file, starting at a specific offset, with a
        defined chunk size. This allows the file to be uploaded or saved in multiple chunks,
        improving memory efficiency for large files.

        Args:
            file_entity (FileEntity): The file entity containing file metadata and content.
            offset (int): The starting byte position in the file where the chunk should be saved.
            chunk_size (int): The size of the chunk to be saved, in bytes.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        ...
