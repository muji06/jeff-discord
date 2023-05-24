import time
import requests
import json
import redis

from timeloop import Timeloop
from datetime import timedelta, datetime

from config import DOWNLOAD_URLS, ROTATIONS, FIRST_WEEK

class RedisManager(object):
    def __init__(self):
        conn = redis.Redis(host="redis_jeff",port=6378, db=1)
        self.cache = conn

cache = RedisManager()
tl = Timeloop()

@tl.job(interval=timedelta(hours=2))
def calculate_incarnation_week():
    print(f"[calculate_incarnation_week][{time.ctime()}]:\t[Checking time for update]")

    # trick website into thinking we are a browser
    response = requests.get("https://timezone.abstractapi.com/v1/current_time/?api_key=23368da787414c17b1e67f510447f287&location=Paris, France")
    current_timestamp = datetime.strptime(response.json()["datetime"], "%Y-%m-%d %H:%M:%S")
    
    week1_timestamp = datetime.fromtimestamp(FIRST_WEEK)
    weeks_passed = (current_timestamp - week1_timestamp).days // 7
    current_rotation = weeks_passed % len(ROTATIONS) # get index
    rotation = ",".join(ROTATIONS[current_rotation])
    cache.cache.set("circuit:1",rotation)
    print(f"[calculate_incarnation_week][{time.ctime()}]:\t[New week calculated for circuit rotations]")

@tl.job(interval=timedelta(seconds=3600))
def refill_wiki_data():
    for key, url in DOWNLOAD_URLS.items():
        ready = False
        retries = 0
        while not ready and retries < 100:
            retries += 1
            print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading data for '{key}'...]")
            try:
                data = requests.get(url=url).json()
            except:
                print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading failed '{key}'{chr(10)}]")
                continue
                
            if 'data' in data:
                ready = True
                text = json.dumps(data)
                cache.cache.set(key, text)
                print(f"[refill_wiki_data][{time.ctime()}]:\t[{key} data ready on redis!']")
                break
            else:
                print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading not succesful for '{key}'data retrieved: {data}. Retrying...]")
                
        


tl.start(block=True)