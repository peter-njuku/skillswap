from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://peter:Peter@localhost/skillswap"
    SECRET_KEY:str = "4bf6847f76ba571fafe895389087776ca6d2125f594998bd00dec9ca521b39c1"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()