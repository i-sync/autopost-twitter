# coding=utf-8

"""
Auto Post Twitter
"""
import re
import os
import time
import math
import json
import tweepy
import random
import requests
import traceback
from config import configs

def get_aqi_txt(num):
    if num < 50:
        return "优"
    elif num < 100:
        return "良"
    elif num < 150:
        return "轻度污染"
    elif num < 200:
        return "中度污染"
    elif num < 300:
        return "重度污染"
    else:
        return "严重污染"

def temperature():
    url = f"https://d1.weather.com.cn/weixinfc/101010100.html?_={math.floor(time.time()*1000)}"
    headers = {
        "Referer": "http://m.weather.com.cn/"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return ""
    try:
        res = res.content.decode('utf-8').replace("var fc=", "")
        res = json.loads(res)
        return f'[{res["f"][1]["fd"]}℃ ~ {res["f"][1]["fc"]}℃]'
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return ""

def weather():
    url = f"https://d1.weather.com.cn/sk_2d/101010100.html?_={math.floor(time.time()*1000)}"
    headers = {
        "Referer": "http://m.weather.com.cn/"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return "获取天气数据失败！"
    try:
        res = res.content.decode('utf-8').replace("var dataSK=", "")
        res = json.loads(res)
        aqi = int(res["aqi_pm25"])
        aqi_txt = get_aqi_txt(aqi)

        return f'{res["cityname"]}, 今天是{time.localtime().tm_year}年{res["date"]} {res["weather"]} {res["WD"]}{res["WS"]}, 当前温度: {res["temp"]}°C{temperature()}, 空气质量: {aqi} ({aqi_txt})'
    except Exception as e:
        return "获取天气数据失败！" + str(e)

def history():
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file = f"{dir_path}/history-of-today/{month}-{day}.json"
    if not os.path.exists(json_file):
        return "获取历史上的今天失败！文件不存在"
    #index = random.randint(0, 2)
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        json_data = json_data["res"][0]
        name = json_data["name"]
        while True:
            i = random.randint(0, len(json_data["lists"]) -1)
            title = json_data["lists"][i]["title"].replace("\n", "")
            year = json_data["lists"][i]["year"]
            if title:
                break
        if year == "None" and re.search("(\d{2,4})年", title):
            year = re.search("(\d{2,4})年", title).group(1)
        title = re.sub(f"{year}年[:， ]?", f"{year}年{month}月{day}日 ", title)
        return title
'''
def test():
    for month in range(1, 13):
        for day in range(1, 32):
            if month == 2 and day > 29 or month in [4,6,9,11] and day > 30:
                continue
            dir_path = os.path.dirname(os.path.realpath(__file__))
            json_file = f"{dir_path}/history-of-today/{month}-{day}.json"
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                json_data = json_data["res"][0]
                for item in json_data["lists"]:
                    title = item["title"].replace("\n", "")
                    if title:
                        year = item["year"]
                        if year == "None" and re.search("(\d{2,4})年", title):
                            year = re.search("(\d{2,4})年", title).group(1)
                        title = re.sub(f"{year}年[:， ]?", f"{year}年{month}月{day}日 ", title)
                        if title.find(f"{year}年{month}月{day}日 ") == -1:
                            print(month,day , "----", title)
'''
if __name__ == "__main__":
    w = weather()
    h = history()
    text = f"[天气自动播报] {w}\n[历史上的今天] {h}"
    client=tweepy.Client(consumer_key=configs.twitter.apikey,
                     consumer_secret=configs.twitter.apikey_secret,
                     access_token=configs.twitter.access_token,
                     access_token_secret=configs.twitter.access_token_secret)
    client.create_tweet(text=text)