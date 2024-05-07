import os.path
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the base directory where this script resides
BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """
    This class is a subclass of BaseSettings from the pydantic library. It is used to manage environment-specific settings throughout the project.
    The settings are loaded from a `.env` file located in the base directory of the script. Extra fields not defined in the model are ignored.

    Attributes:
        model_config (SettingsConfigDict): Configuration for loading environment variables from a `.env` file.
        postgres_host (str): Hostname of the PostgreSQL server.
        postgres_port (str): Port on which the PostgreSQL server is running.
        postgres_db_name (str): Name of the database to connect to within PostgreSQL.
        postgres_schema (str): Database schema used within PostgreSQL.
        postgres_user (str): Username for authenticating with PostgreSQL.
        postgres_password (SecretStr): Password for authenticating with PostgreSQL, stored as a secret.
        postgres_ingress_port (str): Local port used to connect to PostgreSQL, typically used during development.
        local_development (bool): Flag to indicate if the application is running in a local development environment.
        debug_mode (bool): Flag to enable or disable debug mode, impacting error reporting and logging.
        log_level (str): Defines the severity level of logs to capture.
        json_logs (bool): Determines if logs should be output in JSON format.
        gunicorn_workers (int): Number of worker processes for handling requests, used when running with Gunicorn.
        fastapi_host (str): Hostname to bind the FastAPI application to.
        fastapi_port (str): Port to bind the FastAPI application to.
        jwt_secret_signature (SecretStr): Secret key used for signing JWTs, stored as a secret.
        api_prefix (str): Prefix for API routes, typically used for versioning or endpoint grouping.

    Methods:
        get_db_url() -> str:
            Constructs the database connection URL.
            If running in a local development environment, it connects via the local ingress port.
            Otherwise, it uses the configured PostgreSQL host and port.
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(str(BASE_DIR), ".env"), env_file_encoding="utf-8", extra="ignore"
    )
    # Postgres settings
    postgres_host: str
    postgres_port: str
    postgres_db_name: str
    postgres_schema: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_ingress_port: str
    postgres_test_db_name: str
    # Redis settings
    redis_host: str
    redis_port: str
    redis_ingress_port: str
    # FastAPI settings
    local_development: bool
    debug_mode: bool
    log_level: str
    json_logs: bool
    gunicorn_workers: int
    fastapi_host: str
    fastapi_port: str
    jwt_secret_signature: SecretStr
    api_prefix: str
    algorithm: str
    jwt_expire_time: int
    decimal_places: int
    check_default_line_width: int
    print_check_endpoint_name: str
    str_length: str = "str_length"
    check_identifier: str = "check_identifier"

    def get_test_db_url(self) -> str:
        """
        Constructs the database connection URL for testing.
        If running in a local development environment, it connects via the local ingress port.
        Otherwise, it uses the configured PostgreSQL host and port.
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@"
            f"127.0.0.1:{self.postgres_ingress_port}/{self.postgres_test_db_name}"
        )

    def get_db_url(self) -> str:
        """
        Constructs the database connection URL.
        If running in a local development environment, it connects via the local ingress port.
        Otherwise, it uses the configured PostgreSQL host and port.
        """
        if self.local_development:
            return (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@"
                f"127.0.0.1:{self.postgres_ingress_port}/{self.postgres_db_name}"
            )
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"
        )

    def get_redis_url(self) -> str:
        """
        Constructs the Redis connection URL.
        If running in a local development environment, it connects via the local ingress port.
        Otherwise, it uses the configured Redis host and port.
        """
        if self.local_development:
            return f"redis://{self.redis_host}:{self.redis_ingress_port}"
        return f"redis://{self.redis_host}:{self.redis_port}"


settings = Settings()  # An instance of the Settings class
