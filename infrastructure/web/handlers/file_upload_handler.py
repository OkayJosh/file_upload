"""
Module: file_upload_handler

This module defines the `FileUploadHandler` class, which is responsible for handling
file upload requests in a Tornado web application. It interacts with the UploadUseCase
to process and save the uploaded file data, managing JSON-based responses for both
success and error scenarios.

This handler serves as an entry point for HTTP-based file uploads and ensures that
all responses are formatted in JSON, providing a consistent interface for clients.

Example Use Case:
    - Accepting file uploads via POST requests and processing them while returning
      appropriate responses in JSON format.
"""

import tornado.web
from domain.entity import FileEntity
from infrastructure.web.serializers import FileUploadSchema

class FileUploadHandler(tornado.web.RequestHandler):
    """
    FileUploadHandler is responsible for handling file upload requests via POST.
    It interacts with the UploadUseCase to process and save the uploaded file data.

    This handler acts as an entry point for HTTP-based file uploads in the
    infrastructure layer and manages JSON-based responses for both success and error cases.

    Attributes:
        HTTP_OK (int): HTTP status code for successful responses.
        HTTP_BAD_REQUEST (int): HTTP status code for bad requests (e.g., missing file).
        HTTP_INTERNAL_SERVER_ERROR (int): HTTP status code for server errors.
    """

    # Class-level constants for HTTP status codes
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_INTERNAL_SERVER_ERROR = 500

    def initialize(self, upload_use_case):
        """
        Initializes the FileUploadHandler with the necessary upload use case.

        Args:
            upload_use_case (UploadUseCase): The use case responsible for handling
                                             the file upload process and business logic.
        """
        self.upload_use_case = upload_use_case

    def set_default_headers(self):
        """
        Sets default headers to ensure all responses are returned as JSON.
        This method ensures that the 'Content-Type' header is set to 'application/json'.
        """
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        """
        Custom error handler to return errors in JSON format.

        Args:
            status_code (int): HTTP status code for the error (e.g., 400, 500).
            **kwargs: Additional error information, such as exception details.

        Returns:
            JSON response with the error message and status code.
        """
        self.set_header('Content-Type', 'application/json')

        if "exc_info" in kwargs:
            # Extract the exception object from exc_info
            _, exc, _ = kwargs["exc_info"]
            self.finish({
                "status": "error",
                "message": str(exc)
            })
        else:
            self.finish({
                "status": "error",
                # Tornado's default reason for the status code
                "message": self._reason
            })

    def post(self):
        """
        Handles file uploads via POST requests. The method extracts the uploaded file,
        processes it using the FileEntity class, and executes the corresponding use case
        to handle storage and any associated logic.

        Expects:
            - A 'multipart/form-data' request containing the file under the 'file' key.

        Returns:
            A JSON response with the status of the upload operation.
        """
        try:
            file_info = self.request.files['file'][0]
            filename = file_info['filename']
            content = file_info['body']

            # Validate the uploaded data using the FileUploadSchema
            validated_data = FileUploadSchema.validate_data(filename=filename, content=content)

            # Create a FileEntity from the validated data
            file_entity = FileEntity(validated_data.filename, validated_data.content)

            # Execute the upload use case to handle the file storage process
            self.upload_use_case.execute(file_entity)

            # Respond with success message in JSON format
            self.set_status(self.HTTP_OK)
            self.write({
                "status": "success",
                "message": f"File '{filename}' uploaded successfully!"
            })

        except KeyError as exception:
            # Handle missing file key in the request
            self.send_error(self.HTTP_BAD_REQUEST, **exception.__dict__)

        except Exception as exception:
            # Handle any other exceptions during the file upload process
            self.send_error(self.HTTP_INTERNAL_SERVER_ERROR, **exception.__dict__)
