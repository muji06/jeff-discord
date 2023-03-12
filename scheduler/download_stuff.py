import time
import requests
import json

from timeloop import Timeloop
from datetime import timedelta

import redis

class RedisManager(object):
    def __init__(self):
        conn = redis.Redis(host="redis_jeff",port=6378, db=1)
        self.cache = conn

cache = RedisManager()
tl = Timeloop()

DOWNLOAD_URLS = {
    "void:1": "https://wf.snekw.com/void-wiki'",
    "weapon:1": "https://wf.snekw.com/weapons-wiki",
    "arcane:1": "https://wf.snekw.com/arcane-wiki",
    "mod:1": "https://wf.snekw.com/mods-wiki",
}


@tl.job(interval=timedelta(seconds=3600))
def refill_wiki_data():
    for key, url in DOWNLOAD_URLS.items():
        ready = False
        retries = 0
        while not ready and retries < 100:
            retries += 1
            print(f"[{time.ctime()}]:\t[Downloading data for '{key}'...]")
            try:
                data = requests.get(url=url).json()
            except:
                print(f"[{time.ctime()}]:\t[Downloading failed '{key}'{chr(10)}]")
                continue
                
            if 'data' in data:
                ready = True
                text = json.dumps(data)
                cache.cache.set(key, text)
                print(f"[{time.ctime()}]:\t[{key} data ready on redis!']")
                break
            else:
                print(f"[{time.ctime()}]:\t[Downloading not succesful for '{key}'data retrieved: {data}. Retrying...]")
                
        


tl.start(block=True)