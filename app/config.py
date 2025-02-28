from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback/google"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    SENDGRID_API_KEY: str
    EMAIL_FROM: str = "noreply@yourapp.com"
    SENDGRID_API_KEY: str = "default_sendgrid_api_key"


    # Additional fields from your errors
    project_name: str
    version: str
    debug: bool
    host: str
    port: int
    algorithm: str
    refresh_token_expire_minutes: int
    cors_origins: list[str]
    mongodb_uri: str
    database_name: str
    mongodb_min_pool_size: int
    mongodb_max_pool_size: int
    mongodb_timeout_ms: int
    mongodb_max_idle_time_ms: int
    mongodb_retry_writes: bool
    mongodb_retry_reads: bool
    mongodb_tls: bool
    mongodb_server_selection_timeout_ms: int
    mongodb_heartbeat_frequency_ms: int
    redis_url: str
    redis_host: str
    redis_port: int
    claude_api_key: str
    claude_model: str
    max_upload_size: int
    allowed_file_types: list[str]
    default_page_size: int
    max_page_size: int
    cache_expiration: int
    log_level: str

    supabase_url:str
    supabase_key:str


    class Config:
        env_file = ".env"


settings = Settings()