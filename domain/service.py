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

    def __init__(self, file_repo, progress_notifier):
        """
        Initialize the FileService with the necessary dependencies.

        Args:
            file_repo: The file repository instance that will handle file storage.
            progress_notifier: The progress notifier instance to notify upload progress.
        """
        self.file_repo = file_repo
        self.progress_notifier = progress_notifier

    def upload_file(self, file_entity):
        """
        Uploads a file in chunks to the file repository. This method divides the
        file content into smaller chunks, saves each chunk using the repository,
        and notifies the progress notifier after each chunk is uploaded.

        Args:
            file_entity (FileEntity): The file entity containing the file's metadata and content
                                      that needs to be uploaded.

        Raises:
            Exception: May raise an exception if there is an error in saving the chunk
                        or notifying progress.
        """
        total_size = len(file_entity.content)
        chunk_size = total_size // self.UPLOAD_RANGE
        uploaded_size = 0

        for i in range(self.UPLOAD_RANGE):
            # Write file in chunks using repository adapter.
            self.file_repo.save_file_chunk(file_entity, uploaded_size, chunk_size)
            uploaded_size += chunk_size  # Update the uploaded size.

            # Notify progress via notifier adapter.
            self.progress_notifier.notify_progress(f"{(i + 1) * self.UPLOAD_RANGE}%")
