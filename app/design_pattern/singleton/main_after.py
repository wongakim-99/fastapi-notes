# main_after.py
# 싱글톤 패턴에서의 좋은 예시 -> ReportGenerator 가 __init__ 을 통해 외부에서 settings 객체를 전달받는것에 주목

from fastapi import FastAPI, Depends
from app.design_pattern.singleton.core.config_after import AppSettings

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("FastAPI 애플리케이션 싱글톤 패턴(좋은예시) 시작")

# --- 의존성 주입(Dependency Injection)을 위한 설정 ---
# 1. 앱 전체에서 공유할 유일한 인스턴스를 명시적으로 생성합니다.
# (해당 코드는 main.py 에 있기에 인스턴스 생명주기를 제어하기 좋습니다.)
app_settings_instance = AppSettings()

# 2. 해당 인스턴스를 반환하는 '공급자(Provide)' 함수를 만듭니다.
# FastAPI 의 Depends 가 해당 함수를 호출하여 의존성을 주입합니다.
def get_settings():
    logger.info("   -> DI 시스템이 settings 객체를 주입합니다.")
    return app_settings_instance

# -----------------------------------------------------

@app.get("/good")
# 의존성 주입이 일어나는 지점
# API 함수는 "settings" 객체를 파라미터로 "주입" 받습니다.
# 해당 함수는 "settings" 가 어떻게 만들어지는지 전혀 신경쓰지 않습니다.
def get_current_theme(settings: AppSettings = Depends(get_settings)):
    logger.info("\n--- API 요청 : '/good' ---")
    current_theme = settings.get_theme()

    logger.info(f"  [API] 현재 테마 조회: {current_theme}")
    return {"example_type" : "good", "current_theme" : current_theme}


@app.put("/good/theme/{theme_name}")
def change_theme(theme_name: str, settings: AppSettings = Depends(get_settings)):
    logger.info(f"\n--- API 요청: '/good/theme/{theme_name}' ---")
    logger.info(f"  [API] 테마를 '{theme_name}'(으)로 변경 요청...")

    settings.set_theme(theme_name)
    new_theme = settings.get_theme()

    logger.info(f"  [API] 변경 완료된 테마: {new_theme}")
    return {"message" : "Theme changed successfully", "new_theme" : new_theme}