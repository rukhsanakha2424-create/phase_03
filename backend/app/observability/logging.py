import logging
from typing import Optional

from loguru import logger


def configure_logging(level: str = "INFO") -> None:
    logging.getLogger().handlers = []
    logger.remove()
    logger.add(lambda msg: logging.getLogger("uvicorn").info(msg.rstrip()), level=level)


def request_id_filter(request_id: Optional[str]) -> dict:
    return {"request_id": request_id or "unknown"}
