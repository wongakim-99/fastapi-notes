# FastAPI 를 통해 의존성 주입 (DI)이 왜 강력한가?
# 그리고 이를 통해 어떻게 코드의 질을 바꾸는가?

# 상황
"""
여러 API 엔드포인트에서 데이터베이스에 접근해야 한다고 가정.
각 함수마다 DB 연결을 만들고, 로직을 실행하고, 연결을 닫는 코드를 반복적으로 작성해야 한다.
"""
from aiohttp.abc import HTTPException
from fastapi import FastAPI

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
    """
    DB 커넥션을 흉내 내는 가짜 클래스
    """
    def __init__(self):
        logger.info("✅ DB 커넥션 열림")
        self.db = fake_items_db

    def get_item(self, item_id: str):
        if item_id not in self.db:
            return None
        return self.db[item_id]

    def close(self):
        logger.info("🛑 DB 커넥션 닫힘")


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    # 1. 모든 함수에서 DB 연결 코드를 반복
    db = FakeDBSession()

    try:
        item = db.get_item(item_id)
        if item_id is None:
            raise HTTPException(status_code = 404, detail = "Item not found")
        return item

    finally:
        # 2. 모든 함수에서 DB 를 닫는 코드를 반복
        db.close()

@app.get("/user/{user_id}")
async def read_user(user_id: str):
    # 다른 함수에서도 똑같은 코드가 반복된다.
    db = FakeDBSession()
    try:
        # (여기서는 그냥 아이템을 가져오는 로직으로 대체)
        user_info = db.get_item("item1")
        return {"user_id" : user_id, "info" : user_info}

    finally:
        db.close()

"""
위의 코드의 문제점

1. 코드 중복 : read_item 과 read_user 함수 모두 db = FakeDBSession()과 db.close() 
코드가 똑같이 반복된다. API가 100개가 되면 이 코드는 100번 반복된다.

2. 유지보수의 어려움 : DB 연결 방식이 바뀌면 (예 : 타임아웃 추가) 이 100개의 함수를 모두 수정해야 한다.

3. 테스트의 어려움 : 테스트할 때 실제 DB 대신 가짜 DB를 사용하고 싶은데, 함수 코드 자체를 바꾸지 않고는 불가능하다.
"""