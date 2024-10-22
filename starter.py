import tornado.ioloop
import tornado.web

from application.upload_use_case import UploadUseCase
from infrastructure.web.handlers.file_upload_handler import FileUploadHandler
from infrastructure.web.handlers.websocket_handler import ProgressWebSocketHandler
from infrastructure.adapters.file_repository import FileRepository
from infrastructure.adapters.websocket_progress_notifier import WebSocketProgressNotifier

def app():
    file_repo = FileRepository()
    progress_notifier = WebSocketProgressNotifier(ProgressWebSocketHandler)
    upload_use_case = UploadUseCase(file_repo, progress_notifier)

    # Return the Tornado application with the following routes:
    # - Redirect from root ("/") to the static HTML file (index.html)
    # - "/upload" for file uploads (handled by FileUploadHandler)
    # - "/ws/progress" for WebSocket connections to notify clients of progress (handled by ProgressWebSocketHandler)
    # - "/static" for serving static files like HTML, CSS, and JS
    return tornado.web.Application([
        (r"/", tornado.web.RedirectHandler, {"url": "/static/index.html"}),
        (r"/upload", FileUploadHandler, dict(upload_use_case=upload_use_case)),
        (r"/ws/progress", ProgressWebSocketHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static"}),
    ])

if __name__ == "__main__":
    app = app()
    app.listen(8888)
    print("Tornado server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
