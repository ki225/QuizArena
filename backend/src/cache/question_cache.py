import json
from .redis_client import redis

async def get_question_cache(game_id: str, question_id: str):
    key = f"game:{game_id}:question:{question_id}"
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    return None

async def set_question_cache(game_id: str, question_id: str, question_data: dict, expire_seconds: int = 3600):
    key = f"game:{game_id}:question:{question_id}"
    await redis.set(key, json.dumps(question_data), ex=expire_seconds)