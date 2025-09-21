# main_before.py
# 싱글톤 패턴에서의 나쁜 예시 -> 다른 모듈이 싱글톤 객체를 직접 import 해서 사용하는 고전적인 방식
# 강한 결합(Tight Coupling) 을 유발하여 테스트를 거의 불가능하게 만든다.

from fastapi import FastAPI

# 이 부분이 문제의 핵심입니다.
# 특정 파일 (config_bad) 의 특정 변수 (settings) 를 직접 가져와 사용합니다.
# 해당 코드는 settings 변수 없이는 절대 동작할 수 없습니다.
from app.design_pattern.singleton.core.config_before import settings

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("FastAPI 애플리케이션 싱글톤 패턴(나쁜예시) 시작")

@app.get("/bad")
def get_current_theme():
    logger.info("\n--- API 요청: '/bad' ---")

    # 전역 변수로 import 한 settings 객체를 직접 사용합니다.
    current_theme = settings.get_theme()
    logger.info(f"  [API] 현재 테마 조회: {current_theme}")

    return {"example_type" : "bad", "current_theme" : current_theme}

@app.put("bad/theme/{theme_name}")
def change_theme(theme_name: str):
    logger.info(f"\n--- API 요청: '/bad/theme/{theme_name}' ---")
    logger.info(f"  [API] 테마를 '{theme_name}' (으)로 변경 요청...")

    # 전역 변수 settings 의 상태를 직접 변경합니다.
    settings.set_theme(theme_name)
    new_theme = settings.get_theme()

    logger.info(f"  [API] 변경 완료된 테마: {new_theme}")
    return {"message" : "Theme changed successfully", "new_theme" : new_theme}