from abc import ABC, abstractmethod

# 인터페이스 정의
# ABC : Abstract Base Class (추상 기본 클래스)
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message: str):
        pass