from app.design_pattern.strategies.alarm.base import NotificationStrategy

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SmsStrategy(NotificationStrategy):
    def send(self, message: str):
        logger.info(f"문자 메시지 발송 : {message}")