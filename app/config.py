from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://kompis:hemligt@db/kompis"
    file_storage_path: str = "/data/files"
    zebra_printer_ip: str = "192.168.1.100"
    zebra_printer_port: int = 9100
    anthropic_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
