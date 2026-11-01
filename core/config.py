from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, SecretStr

class DatabaseSettins(BaseSettings):
    db_name: SecretStr
    db_user: SecretStr
    db_password: SecretStr
    db_host: str = "db"
    db_port: int = 5432

    @computed_field
    @property
    def db_address(self) -> str:
        name = self.db_name.get_secret_value()
        user = self.db_user.get_secret_value()
        password = self.db_password.get_secret_value()
        url =  f"postgresql+asyncpg://{user}:{password}@{self.db_host}:{self.db_port}/{name}"
        return SecretStr(url)
    
    model_config = SettingsConfigDict(env_file=".env")

db_settings = DatabaseSettins()