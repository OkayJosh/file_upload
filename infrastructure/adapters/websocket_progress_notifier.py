"""
Module: websocket_progress_notifier

This module defines the `WebSocketProgressNotifier` class, which implements the
`ProgressNotifier` interface for sending progress updates through a WebSocket connection.
The `WebSocketProgressNotifier` is responsible for notifying clients about the status
of file uploads or any other processes that require progress reporting.

This implementation facilitates real-time communication with clients, allowing them to
receive updates as tasks are completed or as progress is made.

Example Use Case:
    - Notifying users about the progress of file uploads in real time using WebSocket connections,
      allowing for a more interactive user experience.
"""
from tornado.websocket import WebSocketHandler
from typing_extensions import TypeVar, Type

from application.interfaces.progress_notifier import ProgressNotifier

_T = TypeVar('_T', bound=WebSocketHandler)

class WebSocketProgressNotifier(ProgressNotifier):
    """
    WebSocketProgressNotifier is an implementation of the ProgressNotifier interface,
    providing methods to notify clients of progress updates via a WebSocket connection.

    This class takes a WebSocket handler as a dependency and uses it to send progress
    messages to connected clients.

    Attributes:
        ws_handler: The WebSocket handler instance responsible for managing WebSocket connections
                    and sending messages to clients.
    """

    def __init__(self, ws_handler: Type[_T]) -> None:
        """
        Initialize the WebSocketProgressNotifier with the specified WebSocket handler.

        Args:
            ws_handler: The WebSocket handler instance that will be used to send progress updates
                        to connected clients.
        """
        self.ws_handler = ws_handler

    def notify_progress(self, progress: str) -> None:
        """
        Send a progress update to clients connected via WebSocket.

        This method uses the WebSocket handler to send the provided progress message to
        all connected clients, allowing them to be informed about the current status of
        an ongoing task.

        Args:
            progress (str): A string message indicating the current progress (e.g., percentage
                            completion) of the upload or task.

        Raises:
            Exception: If there is an error in sending the progress update through the WebSocket.
        """
        self.ws_handler.send_update(progress)
