# 앞선 main_before_di.py 에서 생겼던 문제를 DI 의존성 주입으로 해결이 가능하다.

from fastapi import Depends, FastAPI, HTTPException

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# ------------ 가짜 DB ------------
# 실제 DB 대신 간단한 dict로 흉내 낸다.
fake_items_db = {
    "item1" : {"name" : "Gawon"},
    "item2" : {"name" : "Hyunwoo"},
    "item3" : {"name" : "Soomin"},
    "item4" : {"name" : "Heeyoung"},
    "item5" : {"name" : "Seungchan"},
    "item6" : {"name" : "Jihoon"},
    "item7" : {"name" : "Hyungjoon"},
}

class FakeDBSession:
    def __init__(self):
        logger.info("✅ DB 커넥션 열림")
        self.db = fake_items_db

    def get_item(self, item_id: str):
        if item_id not in self.db:
            return None

        return self.db[item_id]

    def close(self):
        logger.info("🛑 DB 커넥션 닫힘")

# STEP 1 : 의존성 함수 만들기
# 이 함수가 DB 커넥션의 '생성'과 '해제'를 책임진다.
def get_db():
    db = FakeDBSession()

    try:
        yield db  # yield : 함수가 호출되면 이 부분의 결과 (db 객체)를 주입하고,
    finally:
        db.close()  # 요청 처리가 끝나면 finally 부분이 실행된다.


# STEP 2 : 경로 작동 함수에서 Depends로 의존성 주입받기
@app.get("/items/{item_id}")
async def read_item(item_id: str, db: FakeDBSession = Depends(get_db)):
    # 이제 해당 함수는 "어떻게" DB 를 가져올지 신경 쓰지 않는다.
    # 오직 '무엇을' 할 것인지(비즈니스 로직)에만 집중한다.
    item = db.get_item(item_id)

    if item is None:
        raise HTTPException(status_code = 404, detail = "Item not found")
    return item

@app.get("/users/{user_id}")
async def read_user(user_id: str, db: FakeDBSession = Depends(get_db)):
    # 해당 API 에서 또한 마찬가지로 코드가 더욱 더 깔끔해진다.
    user_info = db.get_item("item1")
    return {"user_id" : user_id, "info" : user_info}