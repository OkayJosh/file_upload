"""
Module: progress_notifier_port

This module defines the `ProgressNotifierPort` class, which is an abstract base class
that serves as a port for notifying the progress of operations, such as file uploads or
downloads. The class defines an interface that different progress notification mechanisms
(e.g., WebSocket, HTTP, or any other communication channel) must implement.

This module is part of the ports and adapters pattern, providing an abstraction for
notifying progress updates, allowing the application to send progress updates
without being tightly coupled to a specific implementation.

Example Use Case:
    - A WebSocket notifier that sends file upload progress to clients in real-time.
    - A logging-based notifier that logs progress to a file or console.
"""
from abc import ABC, abstractmethod

class ProgressNotifierPort(ABC):
    """
    ProgressNotifierPort is an abstract base class (ABC) that defines the contract for
    notifying progress updates. It serves as a port in the ports and adapters pattern,
    allowing different progress notification mechanisms (e.g., WebSocket, HTTP, logging)
    to be implemented without changing the core business logic.

    The primary responsibility of this port is to notify clients or systems about the
    current progress of an ongoing task (e.g., file upload, data processing) in a flexible,
    decoupled manner.
    """

    @abstractmethod
    def notify_progress(self, progress: str):
        """
        Abstract method for notifying progress updates.

        This method must be implemented by any class that inherits from ProgressNotifierPort.
        It is responsible for sending a progress update, typically represented as a string.
        The progress information can be used to inform clients, systems, or logs about the
        current status of a task.

        Args:
            progress (str): A string representing the progress status (e.g., "50% completed", "Upload in progress").

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        pass
