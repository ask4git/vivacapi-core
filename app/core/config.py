from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # -------------------------------------------------------------------------
    # 애플리케이션
    # -------------------------------------------------------------------------
    ENVIRONMENT: Literal["local", "dev", "prod"] = "local"

    # -------------------------------------------------------------------------
    # 데이터베이스 (직접 접속 시 사용)
    # local: docker-compose / prod: RDS 프라이빗 엔드포인트
    # -------------------------------------------------------------------------
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # -------------------------------------------------------------------------
    # Bastion Host (ENVIRONMENT=dev, 로컬에서 AWS RDS 접속 시 사용)
    # -------------------------------------------------------------------------
    USE_BASTION: str = "false"
    BASTION_HOST: str = ""
    BASTION_PORT: str = "22"
    BASTION_USER: str = "ec2-user"
    BASTION_SSH_KEY_PATH: str = ""
    BASTION_LOCAL_PORT: str = "5433"

    # Bastion 경유 시 실제 목적지 (RDS 프라이빗 엔드포인트)
    RDS_HOST: str = ""
    RDS_PORT: str = "5432"

    # -------------------------------------------------------------------------
    # Computed fields
    # -------------------------------------------------------------------------
    @computed_field
    @property
    def use_bastion(self) -> bool:
        return self.USE_BASTION.lower() == "true"

    @computed_field
    @property
    def database_url(self) -> str:
        """
        use_bastion=True : SSH 터널의 로컬 포트로 연결
        use_bastion=False: DB_HOST:DB_PORT 로 직접 연결
        """
        if self.use_bastion:
            host = "127.0.0.1"
            port = self.BASTION_LOCAL_PORT
        else:
            host = self.DB_HOST
            port = self.DB_PORT

        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{host}:{port}/{self.DB_NAME}"
        )


settings = Settings()
