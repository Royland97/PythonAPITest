from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    username: str
    password: str
    host: str
    port: int
    database: str

    model_config = SettingsConfigDict(
        env_prefix="APP_MONGO_",
        env_file=".env",
        extra="ignore"
    )

    @property
    def mongo_url(self):
        return (
            f"mongodb://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
            "?authSource=admin"
        )

# Load MongoDB settings
db_settings = DatabaseSettings()
