# main_before.py
# 싱글톤 패턴에서의 나쁜 예시 -> 다른 모듈이 싱글톤 객체를 직접 import 해서 사용하는 고전적인 방식
# 강한 결합(Tight Coupling) 을 유발하여 테스트를 거의 불가능하게 만든다.

from fastapi import FastAPI
from app.design_pattern.singleton.core.config_before import settings  # 이 부분이 문제의 핵심

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("FastAPI 애플리케이션 싱글톤 패턴(나쁜예시) 시작")

class ReportGenerator:
    def __init__(self):
        # 해당 클래스는 core.config_before.py 의 'settings' 객체가 없으면 동작할 수 없음
        # 'settings' 와 운명 공동체가 됨 (강한 결합)
        pass

    def generate(self):
        # 비즈니스 로직 안에서 전역 싱글톤을 직접 사용
        current_theme = settings.get_theme()
        return f"현재 테마 '{current_theme}' 기반의 리포트 생성 완료!"

@app.get("/")
def get_report():
    # ReportGenerator 를 사용하려면 그냥 생성하면 됨
    # 하지만 이 클래스가 내부적으로 'settings'에 의존하는지는 밖에서는 알기 힘듬
    reporter = ReportGenerator()

    return {"report" : reporter.generate()}