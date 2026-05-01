"""
Bastion Host SSH 터널 매니저

사용 시나리오 (ENVIRONMENT=dev):
  로컬 머신 → (SSH) → Bastion Host (EC2) → RDS (프라이빗 서브넷)

터널이 열리면:
  127.0.0.1:{BASTION_LOCAL_PORT} ─► {RDS_HOST}:{RDS_PORT}

FastAPI lifespan에서 start_tunnel() / stop_tunnel() 을 호출합니다.
"""

import logging

from sshtunnel import SSHTunnelForwarder

from app.core.config import settings

logger = logging.getLogger(__name__)

_tunnel: SSHTunnelForwarder | None = None


def start_tunnel() -> None:
    """SSH 터널을 열고 모듈 전역 변수에 저장합니다."""
    global _tunnel

    if not settings.use_bastion:
        logger.info("Bastion tunnel disabled (USE_BASTION=false)")
        return

    _tunnel = SSHTunnelForwarder(
        (settings.BASTION_HOST, int(settings.BASTION_PORT)),
        ssh_username=settings.BASTION_USER,
        ssh_pkey=settings.BASTION_SSH_KEY_PATH,
        remote_bind_address=(settings.RDS_HOST, int(settings.RDS_PORT)),
        local_bind_address=("127.0.0.1", int(settings.BASTION_LOCAL_PORT)),
    )
    _tunnel.start()
    logger.info(
        "SSH tunnel established: 127.0.0.1:%s → %s:%s",
        settings.BASTION_LOCAL_PORT,
        settings.RDS_HOST,
        settings.RDS_PORT,
    )


def stop_tunnel() -> None:
    """SSH 터널을 닫습니다."""
    global _tunnel

    if _tunnel and _tunnel.is_active:
        _tunnel.stop()
        _tunnel = None
        logger.info("SSH tunnel closed")
