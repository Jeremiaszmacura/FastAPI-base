from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]


settings = Settings()