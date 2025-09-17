from app.design_pattern.strategies.alarm.base import NotificationStrategy

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class EmailStrategy(NotificationStrategy):
    def send(self, message: str):
        logger.info(f"이메일 발송 : {message}")
        # 이메일 발송 로직
