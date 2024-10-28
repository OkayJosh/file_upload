# File Upload Service

This project implements a **File Upload Service** using the **Tornado** web framework, **SQLAlchemy** for database interaction, and **Pydantic** for input validation. The service follows a **ports and adapters** (also known as **hexagonal**) architecture to promote separation of concerns and flexibility.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [WebSocket Support](#websocket-support)
- [Testing](#testing)
- [Contributing](#contributing)

## Overview

This service provides an API for uploading large files, splitting them into manageable chunks for storage. The architecture follows the **Clean Architecture** pattern to ensure separation between business logic and infrastructure concerns. 

Key components include:
- **File upload and chunking.**
- **Progress tracking via WebSockets.**
- **Persistent file storage using PostgreSQL via SQLAlchemy.**
- **Dependency injection for easy integration of repositories and notifiers.**

## Architecture

This project is structured based on **Ports and Adapters** (Hexagonal Architecture) to keep the business logic decoupled from the infrastructure details.

- **Domain Layer**: Contains the business logic (e.g., `FileEntity`).
- **Application Layer**: Implements use cases (e.g., `UploadUseCase`) that use the ports.
- **Adapters Layer (Infrastructure)**: Contains the actual implementations (e.g., `File`) of the ports, dealing with database access, WebSocket connections, etc.
- **Ports**: Define the boundaries between the application layer and the outer layers, such as the database or WebSockets.

## Features

- **Chunked file upload**: Large files are uploaded in chunks for more efficient handling.
- **Progress notifications**: Users receive real-time progress updates during file uploads via WebSockets.
- **Pydantic-based validation**: All input data is validated using Pydantic.
- **SQLAlchemy integration**: Async database operations are handled via SQLAlchemy and PostgreSQL.
- **Clean architecture**: Promotes testability, flexibility, and separation of concerns.

## Technologies

- [Tornado](https://www.tornadoweb.org/en/stable/) - Web framework.
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM.
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation library.
- [PostgreSQL](https://www.postgresql.org/) - Database used for persistent storage.
- WebSockets - Used for real-time progress updates.

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.9+
- PostgreSQL (or a compatible database)
- [pipenv](https://pipenv.pypa.io/en/latest/) or pip

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/OkayJosh/file_upload.git
    cd file-upload
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your PostgreSQL database**:
    ```bash
    createdb file_upload_db
    ```

4. **Configure environment variables**:
    Create a `.env` file with your settings or modify the settings directly in `infrastructure/settings.py`. Example:
    ```env
    DATABASE_URL=postgresql+asyncpg://user:password@localhost/file_upload_db
    ```

5. **Run database migrations** (if applicable):
    ```bash
    alembic upgrade head
    ```

## Configuration

All configuration settings are stored in the `infrastructure/settings.py` file. You can customize the following settings:
- `DATABASE_URL`: The connection string for your PostgreSQL database.
- Any other application settings (logging, debug mode, etc.).

## Running the Application

Start the Tornado application by running:

```bash
python starter.py
```