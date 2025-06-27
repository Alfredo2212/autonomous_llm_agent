'''
Init redis client, connect to local redis port 6379
Retrieve past results quicky and avoid recomputing same queries
'''
import redis
import hashlib
import json

r = redis.Redis(host='localhost', port=6379, db=0)

#Attempt to create hashed keys to avoid issues with query strings
def make_cache_key(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()

#Compute key, retrieve from redis and decode back if found
def check_cache(query: str):
    key = make_cache_key(query)
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return None

#If no cache found, store it and serializes result with json
def store_cache(query: str, result: str):
    key = make_cache_key(query)
    r.set(key, json.dumps(result), ex=3600)