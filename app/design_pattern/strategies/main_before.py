from fastapi import FastAPI
from pydantic import BaseModel

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class NotificationRequest(BaseModel):
    type: str # "email" or "sms"
    message: str

@app.post("/send-notification-before")
def send_notification(request: NotificationRequest):

    # 이 부분이 문제의 핵심
    if request.type == "email":
        logger.info(f"이메일 발송 : {request.message}")
        return {"status" : "success", "method" : "email"}

    elif request.type == "sms":
        logger.info(f"문자 발송 : {request.message}")
        return {"status" : "success", "method" : "sms"}

    elif request.type == "slack":
        logger.info(f"슬랙 메시지 발송 : {request.message}")
        return {"status" : "success", "method" : "slack"}

    else:
        return {"status" : "error", "message" : "Unsupported notification type"}

# 만약에 여기서 "푸시 알림" 기능을 추가하려면? API 함수 내부에 elif request.type == "push" 코드를 또 추가
# (OCP) 원칙 위반

'''
알림 종류가 10가지가 된다면 해당 if 문은 괴물이 될 것이고, 이메일 관련 버그를 수정하려고 해도 전체 API 코드를
들여다봐야 할 것입니다.
'''