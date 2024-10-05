import time
import json
import redis
import hashlib
import luadata
import requests

from timeloop import Timeloop
from datetime import timedelta, datetime

from config import DOWNLOAD_URLS, ROTATIONS, FIRST_WEEK,\
    NEW_DOWNLOAD_URLS, CHECKSUMS, WFCD

class RedisManager(object):
    def __init__(self):
        conn = redis.Redis(host="redis_jeff",port=6378, db=1)
        self.cache = conn

cache = RedisManager()
tl = Timeloop()

# @tl.job(interval=timedelta(hours=2))
# def calculate_incarnation_week():
#     print(f"[calculate_incarnation_week][{time.ctime()}]:\t[Checking time for update]")

#     response = requests.get("https://timezone.abstractapi.com/v1/current_time/?api_key=23368da787414c17b1e67f510447f287&location=Paris, France")
#     current_timestamp = datetime.strptime(response.json()["datetime"], "%Y-%m-%d %H:%M:%S")
    
#     week1_timestamp = datetime.fromtimestamp(FIRST_WEEK)
#     weeks_passed = (current_timestamp - week1_timestamp).days // 7
#     current_rotation = weeks_passed % len(ROTATIONS) # get index
#     rotation = ",".join(ROTATIONS[current_rotation])
#     cache.cache.set("circuit:1",rotation)
#     print(f"[calculate_incarnation_week][{time.ctime()}]:\t[New week calculated for circuit rotations]")

# @tl.job(interval=timedelta(seconds=3600))
# def refill_wiki_data():
#     for key, url in DOWNLOAD_URLS.items():
#         ready = False
#         retries = 0
#         while not ready and retries < 100:
#             retries += 1
#             print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading data for '{key}'...]")
#             try:
#                 data = requests.get(url=url).json()
#             except:
#                 print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading failed '{key}'{chr(10)}]")
#                 continue
                
#             if 'data' in data:
#                 ready = True
#                 text = json.dumps(data)
#                 cache.cache.set(key, text)
#                 print(f"[refill_wiki_data][{time.ctime()}]:\t[{key} data ready on redis!']")
#                 break
#             else:
#                 print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading not succesful for '{key}'data retrieved: {data}. Retrying...]")
                


def unserialize_lua_table(lua_table: str)-> dict:
    start_idx = lua_table.find('{')
    end_idx = lua_table.rfind('}') + 1
    lua_table = lua_table[start_idx:end_idx]
    return luadata.unserialize(lua_table)

@tl.job(interval=timedelta(seconds=3600))
def refill_wiki_data_v2():
    for key, url in NEW_DOWNLOAD_URLS.items():
        ready = False
        retries = 0
        while not ready and retries < 100:
            retries += 1
            print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading data for '{key}'...]")
            try:
                res = requests.get(url=url)
            except:
                print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading failed '{key}'{chr(10)}]")
                continue
            
            return_data = res.json().get('return')

            if return_data:
                # get valid lua table result
                unserialized_data = unserialize_lua_table(return_data)

                checksum = hashlib.md5(bytes("".join(json.dumps(unserialized_data)),encoding="utf-8")).hexdigest()
                cached = False
                # check if we have data cached
                old_checksum = ""
                if cache.cache.exists(CHECKSUMS[key]):
                    cached = True
                    old_checksum = cache.cache.get(CHECKSUMS[key])

                ready = True
                if checksum == old_checksum:
                    # create a new checksum
                    if not cached:
                        text = json.dumps(unserialized_data)
                        # save data
                        cache.cache.set(key, text)
                        # save checksum
                        cache.cache.set(CHECKSUMS[key],checksum)
                        print(f"[refill_wiki_data][{time.ctime()}]:\t[{key} data ready on redis!']")
                    else:
                        print(f"[refill_wiki_data][{time.ctime()}]:\t[No new data for {key}! Skipping']")
                else:
                    text = json.dumps(unserialized_data)
                    cache.cache.set(key, text)
                    cache.cache.set(CHECKSUMS[key],checksum)
                    print(f"[refill_wiki_data][{time.ctime()}]:\t[{key} data ready on redis!']")

                break
            else:
                print(f"[refill_wiki_data][{time.ctime()}]:\t[Downloading not succesful for '{key}'data retrieved: {return_data}. Retrying...({retries})]")


@tl.job(interval=timedelta(hours=24))
def refill_github_data():
    for key, url in WFCD:
        retries = 0
        ready = False

        while not ready and retries < 100:
            retries += 1
            print(f"[refill_github_data][{time.ctime()}]:\t[Downloading data for '{key}'...]")
            try:
                res = requests.get(url=url)
            except:
                print(f"[refill_github_data][{time.ctime()}]:\t[Downloading failed '{key}'{chr(10)}]")
                continue
            
            return_data = res.json()
            checksum = hashlib.md5(bytes(res.text)).hexdigest()
            cached = False
            ready = True
            # check if we have data cached
            old_checksum = ""
            if cache.cache.exists(CHECKSUMS[key]):
                cached = True
                old_checksum = cache.cache.get(CHECKSUMS[key])
                
            if checksum == old_checksum:
                # create a new checksum
                if not cached:
                    cache.cache.set(key, return_data)
                    # save checksum
                    cache.cache.set(CHECKSUMS[key], checksum)
                    print(f"[refill_github_data][{time.ctime()}]:\t[{key} data ready on redis!']")
                else:
                    print(f"[refill_github_data][{time.ctime()}]:\t[No new data for {key}! Skipping']")
            else:
                cache.cache.set(key, return_data)
                cache.cache.set(CHECKSUMS[key], checksum)
                print(f"[refill_github_data][{time.ctime()}]:\t[{key} data ready on redis!']")
                break

tl.start(block=True)