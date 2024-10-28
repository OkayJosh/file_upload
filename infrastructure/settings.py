import os
from dotenv import load_dotenv

class Settings:
    """
    Settings class for holding application configurations.

    This class is responsible for loading and providing configuration
    settings for the application, including database connection strings
    and other environment-specific variables.
    """

    def __init__(self):
        load_dotenv()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(project_root, "\n")
        # Use SQLite as the default database
        default_db_path = os.path.join(project_root, "db.sqlite3")
        print(default_db_path, "\n")
        self.DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{default_db_path}")
        # include project settings here
        self.NUMBER_UPLOAD_CHUNK = os.getenv("NUMBER_UPLOAD_CHUNK", 10)
        self.TRACE_MEMORY_ALLOCATION_PER_FRAME = os.getenv("TRACE_MEMORY_ALLOCATION_PER_FRAME", 20)



# Create a global settings instance
settings = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ["infrastructure.models.file_model", "aerich.models"],
            "default_connection": "default",
        }
    }
}