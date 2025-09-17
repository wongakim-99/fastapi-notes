from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.design_pattern.strategies.alarm.email_strategy import EmailStrategy
from app.design_pattern.strategies.alarm.slack_strategy import SlackStrategy
from app.design_pattern.strategies.alarm.sms_strategy import SmsStrategy

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class NotificationRequest(BaseModel):
    type: str
    message: str

# 각 문자열 타입에 맞는 전략 클래스를 "부품" 처럼 미리 준비해 둡니다.
strategies = {
    "email" : EmailStrategy(),
    "sms" : SmsStrategy(),
    "slack" : SlackStrategy()
}

@app.post("/send-notification-after")
def send_notification(request: NotificationRequest):
    strategy = strategies.get(request.type)

    if not strategy:
        raise HTTPException(status_code=400, detail="Unsupported notification type")

    # 선택된 전략(부품)을 실행하기만 하면 된다.
    # API 는 '어떻게' 보내는지는 전혀 신경쓰지 않는다.
    strategy.send(request.message)

    return {"status" : "success", "method" : request.type}