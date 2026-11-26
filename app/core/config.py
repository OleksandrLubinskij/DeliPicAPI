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
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class S3Settings(BaseSettings):
    s3_bucket_name: str
    s3_endpoint_url: str
    s3_access_key: SecretStr
    s3_secret_key: SecretStr
    s3_public_url: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class GeminyAISettings(BaseSettings):
    geminy_api_key: SecretStr

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AuthSettings(BaseSettings):
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class AdminAccount(BaseSettings):
    login: SecretStr
    email: SecretStr
    password: SecretStr

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

db_settings = DatabaseSettins()
s3_settings = S3Settings()
geminy_ai_settings = GeminyAISettings()
auth_settings = AuthSettings()
admin_account = AdminAccount()