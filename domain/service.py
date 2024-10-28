"""
Module: file_service

This module defines the `FileService` class, which encapsulates the business logic
for handling file uploads in the application. The `FileService` is responsible for
managing the process of uploading files, breaking them into manageable chunks,
and notifying progress during the upload process.

The service interacts with the file repository (for storage) and the progress notifier
(to inform users about the upload status), following the principles of the Clean Architecture.

Example Use Case:
    - Uploading a large file in smaller chunks to prevent memory overload,
      while keeping the user informed of the progress.
"""
from typing import TypeVar

_F = TypeVar('_F', bound='FileEntity')
_T = TypeVar('_T', bound='FileRepository')
_N = TypeVar('_N', bound='ProgressNotifier')


class FileService:
    """
    FileService provides the functionality to upload files by managing the
    process of chunking the file into smaller parts and notifying progress
    during the upload.

    This class relies on a file repository for storing the file chunks and
    a progress notifier to communicate the upload status.

    Attributes:
        UPLOAD_RANGE (int): The number of chunks to divide the file into during upload.
        file_repo: The file repository instance that handles file storage operations.
        progress_notifier: The progress notifier instance that communicates upload progress.
    """

    UPLOAD_RANGE = 10  # The number of chunks to divide the file into during upload.

    def __init__(self, file_repo: _T, progress_notifier: _N):
        """
        Initialize the FileService with the necessary dependencies.

        Args:
            file_repo(_T): The file repository instance that will handle file storage.
            progress_notifier(_N): The progress notifier instance to notify upload progress.
        """
        self.file_repo = file_repo
        self.progress_notifier = progress_notifier

    async def upload_file(self, file_entity: _F) -> None:
        """
        Uploads a file in chunks to the file repository. This method divides the
        file content into smaller chunks, saves each chunk using the repository,
        and notifies the progress notifier after each chunk is uploaded.

        Args:
            file_entity (_F): The file entity containing the file's metadata and content
                                      that needs to be uploaded.

        Raises:
            Exception: May raise an exception if there is an error in saving the chunk
                        or notifying progress.
        """
        total_size = len(file_entity.content)
        chunk_size = total_size // self.UPLOAD_RANGE
        uploaded_size = 0

        for i in range(self.UPLOAD_RANGE):
            uploaded_size += await self._upload_chunk(
                file_entity, uploaded_size, chunk_size, i
                )

    async def _upload_chunk(self, file_entity: _F,
                            uploaded_size: int, chunk_size: int,
                            chunk_index: int) -> int:
        """
        Handles the upload of a single chunk of the file and notifies progress.

        Args:
            file_entity (_F): The file entity being uploaded.
            uploaded_size (int): The cumulative size of uploaded data.
            chunk_size (int): The size of the current chunk.
            chunk_index (int): The index of the current chunk.

        Returns:
            int: The updated uploaded size after processing the chunk.
        """

        await self.file_repo.save_file_chunk(
            file_entity, uploaded_size, chunk_size
        )
        uploaded_size += chunk_size

        # Notify progress via notifier adapter.
        self.progress_notifier.notify_progress(f"{(chunk_index + 1) * self.UPLOAD_RANGE}%")
        return uploaded_size
