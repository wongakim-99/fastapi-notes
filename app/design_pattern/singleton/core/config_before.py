# app/core/config_before.py
# 싱글톤 패턴에 대한 안좋은 예시

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AppSettings:
    """
    앱의 설정을 관리하는 싱글톤 클래스
    """
    _instance = None  # 유일한 인스턴스를 저장할 클래스 변수

    # 1. __new__ 메서드를 오버라이딩하여 객체 생성을 제어
    def __new__(cls):
        if not cls._instance:
            logger.info(f"✅ (나쁜 예시) App Settings : 단 하나의 설정 객체를 최초로 생성합니다.")
            cls ._instance = super().__new__(cls)
        else:
            logger.info(f"✅ (나쁜 예시) App Settings : 이미 생성된 객체를 반환합니다.")

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
# 이것이 싱글톤 패턴이 적용안된 나쁜 방식의 핵심입니다.
# 다른 파일에서는 이 'settings' 변수를 직접 import 하여 사용하게 됩니다.
settings = AppSettings()