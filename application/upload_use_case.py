"""
Module: upload_use_case

This module defines the `UploadUseCase` class, which represents a use case in the
application for handling file uploads. It coordinates the interactions between
the file repository (storage) and the progress notifier, following the principles
of the Clean Architecture.

The `UploadUseCase` serves as the application layer, where the business logic for
uploading files is orchestrated, ensuring that files are correctly stored and the
upload progress is communicated through the appropriate notifier.

Example Use Case:
    - Uploading a file to a local or remote storage system while notifying clients
      of the upload progress via WebSocket or other channels.
"""

from domain.service import FileService


class UploadUseCase:
    """
    UploadUseCase is responsible for executing the business logic of file uploads.
    It coordinates the interaction between the file repository (for storing files)
    and the progress notifier (for notifying upload progress), ensuring that the
    file is successfully stored and progress updates are sent.

    The class serves as an entry point for the file upload process and uses
    the FileService to perform the actual file upload operation.

    Attributes:
        file_service (FileService): A service that handles the file upload process
                                    and progress notifications.
    """

    def __init__(self, file_repo, progress_notifier):
        """
        Initialize the UploadUseCase with the necessary dependencies.

        Args:
            file_repo: The file repository instance that handles file storage (e.g., local or S3 storage).
            progress_notifier: The progress notifier instance that communicates upload progress (e.g., via WebSocket).
        """
        self.file_service = FileService(file_repo, progress_notifier)

    def execute(self, file_entity):
        """
        Execute the file upload use case by delegating the file upload process
        to the FileService. This method is responsible for handling the
        business logic of uploading a file and ensuring that the upload
        progress is properly notified.

        Args:
            file_entity (FileEntity): The file entity containing the file's metadata and content
                                      that needs to be uploaded.
        """
        self.file_service.upload_file(file_entity)
