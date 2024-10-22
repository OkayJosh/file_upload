import os

class Settings:
    """
    Settings class for holding application configurations.

    This class is responsible for loading and providing configuration
    settings for the application, including database connection strings
    and other environment-specific variables.
    """

    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Create a global settings instance
settings = Settings()
