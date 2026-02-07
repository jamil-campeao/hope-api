from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    WAHA_DASHBOARD_USERNAME: str
    WAHA_DASHBOARD_PASSWORD: str
    WAHA_API_KEY: str
    WAHA_BASE_URL: str = "http://waha:3000"
    WHATSAPP_SWAGGER_USERNAME: str
    WHATSAPP_SWAGGER_PASSWORD: str

    N8N_BASIC_AUTH_ACTIVE: bool
    N8N_BASIC_AUTH_USER: str
    N8N_BASIC_AUTH_PASSWORD: str
    N8N_HOST: str
    TOKEN: str
    N8N_PASSWORD: str
    
    # Google Integration
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    @property
    def POSTGRES_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
