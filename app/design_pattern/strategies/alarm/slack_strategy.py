from app.design_pattern.strategies.alarm.base import NotificationStrategy

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SlackStrategy(NotificationStrategy):
    def send(self, message):
        logger.info(f"슬랙 알림 메시지 발송 : {message}")