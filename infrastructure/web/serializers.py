"""
Module: file_upload_schema

This module defines the `FileUploadSchema` class, which is a Pydantic model for validating
the schema of file upload requests. It provides a structured way to define the expected
data format for file uploads, ensuring that the provided filename and content meet the specified
requirements.

Example Use Case:
    - Validating incoming file upload requests to ensure they contain valid filenames and byte content.
"""

from pydantic import BaseModel, ValidationError

class FileUploadSchema(BaseModel):
    """
    FileUploadSchema is a Pydantic model used to validate the structure of file upload data.

    This class ensures that the uploaded file has a valid filename and content format.
    By using Pydantic's validation features, it simplifies error handling and enforces
    data integrity for file upload operations.

    Attributes:
        filename (str): The name of the file being uploaded.
        content (bytes): The content of the file represented as bytes.
    """
    filename: str
    content: bytes

    @staticmethod
    def validate_data(filename: str, content: bytes):
        """
        Validates incoming data for the file upload schema using Pydantic.

        This static method checks the provided filename and content against the schema.
        If the data does not conform to the schema, a ValidationError is raised.

        Args:
            filename (str): The name of the file to be validated.
            content (bytes): The content of the file to be validated.

        Returns:
            FileUploadSchema: An instance of FileUploadSchema containing validated data.

        Raises:
            ValidationError: Raised if the provided data does not conform to the schema.
        """
        try:
            return FileUploadSchema(filename=filename, content=content)
        except ValidationError as e:
            raise e  # Reraise the validation error for further handling
