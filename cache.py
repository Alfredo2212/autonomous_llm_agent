import redis
import hashlib
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def make_cache_key(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()

def check_cache(query: str):
    key = make_cache_key(query)
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return None

def store_cache(query: str, result: str):
    key = make_cache_key(query)
    r.set(key, json.dumps(result), ex=3600)