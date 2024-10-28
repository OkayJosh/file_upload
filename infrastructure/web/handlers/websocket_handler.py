"""
Module: progress_websocket_handler

This module defines the `ProgressWebSocketHandler` class, which is responsible for managing
WebSocket connections and broadcasting progress updates to all connected clients. This handler
allows real-time notifications regarding the status of ongoing tasks, such as file uploads.

The `ProgressWebSocketHandler` maintains a set of active WebSocket clients and provides methods
to send messages to all connected clients, ensuring they receive updates promptly.

Example Use Case:
    - Providing real-time feedback to users about the progress of file uploads through WebSocket connections.
"""
from tornado.websocket import WebSocketHandler


class ProgressWebSocketHandler(WebSocketHandler):
    """
    ProgressWebSocketHandler manages WebSocket connections for real-time progress updates.

    This handler allows clients to connect via WebSocket and receive notifications about
    the progress of various operations, such as file uploads. It maintains a list of connected
    clients and provides functionality to send messages to all of them.

    Attributes:
        clients (set): A set of currently connected WebSocket clients.
    """

    # Class-level attribute to store connected clients
    clients = set()

    def open(self):
        """
        Called when a new WebSocket connection is established.

        This method adds the newly connected client to the set of clients, allowing it to receive
        progress updates.

        It is automatically invoked by Tornado when a client successfully opens a WebSocket connection.
        """
        ProgressWebSocketHandler.clients.add(self)

    def on_close(self):
        """
        Called when a WebSocket connection is closed.

        This method removes the client from the set of connected clients, ensuring that it no longer
        receives updates after disconnection.

        It is automatically invoked by Tornado when a client closes the WebSocket connection.
        """
        ProgressWebSocketHandler.clients.remove(self)

    @classmethod
    def send_update(cls, message):
        """
        Sends a progress update message to all connected WebSocket clients.

        This class method iterates over the set of connected clients and sends the specified message
        to each one, allowing for real-time notifications about progress.

        Args:
            message (str): The message to be sent to all connected clients.
        """
        for client in cls.clients:
            client.write_message(message)
