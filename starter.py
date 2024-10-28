import tornado.ioloop
import tornado.web
import tracemalloc

from tortoise import Tortoise, run_async

from application.upload_use_case import UploadUseCase
from infrastructure.adapters.db_file_repository import DBFile
from infrastructure.settings import TORTOISE_ORM
from infrastructure.web.handlers.file_upload_handler import FileUploadHandler
from infrastructure.web.handlers.websocket_handler import ProgressWebSocketHandler
from infrastructure.adapters.websocket_progress_notifier import WebSocketProgressNotifier

# Start tracing memory allocations, storing up to 10 frames per allocation
tracemalloc.start(10)

async def db_init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


def app():
    file_repo = DBFile()
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
    run_async(db_init())
    app = app()
    app.listen(8888)
    print("Tornado server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
