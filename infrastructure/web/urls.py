import tornado

from application.upload_use_case import UploadUseCase
from infrastructure.adapters.db_file_repository import DBFile
from infrastructure.adapters.websocket_progress_notifier import WebSocketProgressNotifier
from infrastructure.web.handlers.file_upload_handler import FileUploadHandler
from infrastructure.web.handlers.websocket_handler import ProgressWebSocketHandler

file_repo = DBFile()
progress_notifier = WebSocketProgressNotifier(ProgressWebSocketHandler)
upload_use_case = UploadUseCase(file_repo, progress_notifier)

routes = [
    # Return the Tornado application with the following routes:
    # - Redirect from root ("/") to the static HTML file (index.html)
    # - "/upload" for file uploads (handled by FileUploadHandler)
    # - "/ws/progress" for WebSocket connections to notify clients of progress (handled by ProgressWebSocketHandler)
    # - "/static" for serving static files like HTML, CSS, and JS
    (r"/", tornado.web.RedirectHandler, {"url": "/static/index.html"}),
    (r"/upload", FileUploadHandler, dict(upload_use_case=upload_use_case)),
    (r"/ws/progress", ProgressWebSocketHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static"}),
]