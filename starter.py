import tornado.ioloop
import tornado.web
import tracemalloc

from tortoise import Tortoise, run_async

from infrastructure.settings import TORTOISE_ORM, settings
from infrastructure.web.urls import routes

# Start tracing memory allocations, storing up to 10 frames per allocation
tracemalloc.start(settings.TRACE_MEMORY_ALLOCATION_PER_FRAME)

async def db_init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    # NOTE: is this a good practice


def app():
    return tornado.web.Application(routes)

if __name__ == "__main__":
    run_async(db_init())
    app = app()
    app.listen(8888)
    print("Tornado server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
