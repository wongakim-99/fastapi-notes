# app/core/config_after.py
# 싱글톤패턴에 대한 좋은 예시

# 의존성 주입(DI)을 사용한 코드
'''
이 예시는 필요한 객체(의존성)를 내부에서 직접 만들거나 가져오지 않고, 외부에서 전달받는
(주입받는)방식입니다. -> FastAPI 는 이 패턴을 효과적으로 지원
'''

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AppSettings:
    _instance = None  # 유일한 인스턴스를 저장할 클래스 변수

    # 1. __new__ 메서드를 오버라이딩하여 객체 생성을 제어
    def __new__(cls):
        if not cls._instance:
            logger.info(f"✅ App Settings : 단 하나의 설정 객체를 최초로 생성합니다.")
            cls ._instance = super().__new__(cls)
        else:
            logger.info(f"✅ App Settings : 이미 생성된 객체를 반환합니다.")

        return cls ._instance

    # 2. __init__ 은 객체가 생성될 때마다 호출될 수 있으므로,
    # 실제 초기화 로직은 한 번만 실행되도록 플래그로 막는다.
    def __init__(self):
        if not hasattr(self, "initialized"):
            logger.info("  -> 초기 설정 값을 로드합니다.")
            self.settings = {"theme" : "light"}
            self.initialized = True  # 초기화 완료 플래그

    def get_theme(self):
        return self.settings['theme']

    def set_theme(self, theme: str):
        logger.info(f"  -> 테마를 '{self.get_theme()}'에서 '{theme}'(으)로 변경합니다.")
        self.settings['theme'] = theme


# 싱글톤 인스턴스를 전역 변수로 생성
settings = AppSettings()

# 앞선 before_settings 와 차이점이 있다면 전역 인스턴스를 생성하는 코드를 삭제
# settings = AppSettings() -> 해당 줄 삭제