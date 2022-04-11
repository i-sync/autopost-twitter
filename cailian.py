#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import time
import random
import tweepy
import traceback
import requests

from config import configs
from orm import Cailian, session_scope

def crawler():
    url = "https://m.cls.cn/nodeapi/telegraphs?refresh_type=1&rn=10&last_time=1649657053807&app=CailianpressWap&sv=1&sign=f73828502cec98a41720ad8aa0f764be"
    headers = {
        "Referer": "https://m.cls.cn/telegraph",
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return
    try:
        # create tweepy client
        client=tweepy.Client(consumer_key=configs.twitter.apikey,
                     consumer_secret=configs.twitter.apikey_secret,
                     access_token=configs.twitter.access_token,
                     access_token_secret=configs.twitter.access_token_secret)

        json_data = res.json()
        print(json_data)
        for data in json_data["data"]["roll_data"]:
            id = data["id"]
            content = data["content"]
            ctime = data["ctime"]
            with session_scope() as session:
                obj = session.query(Cailian).filter(Cailian.id == id).first()
                if not obj:
                    obj = Cailian(id=id, content = content, ctime = ctime, created_at = time.time())
                    session.add(obj)
                    session.commit()
                    # crate tweepy
                    client.create_tweet(text=content)
                    time.sleep(random.randint(1, 3))

    except Exception as e:
        print(e)
        print(traceback.format_exc())

if __name__ == "__main__":
    crawler()