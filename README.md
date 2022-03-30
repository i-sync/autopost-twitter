# 每天特定时间执行该脚本，自动发布天气，历史上的今天等信息到TWITTER
## 天气
页面URL: [http://m.weather.com.cn/mweather/101010300.shtml](http://m.weather.com.cn/mweather/101010300.shtml)

请求接口，需要指定header, Referer:http://m.weather.com.cn/ , 否则返回403
[https://d1.weather.com.cn/sk_2d/101010100.html?_=1648633609931](https://d1.weather.com.cn/sk_2d/101010100.html?_=1648633609931)

返回结果
```js
var dataSK={"nameen":"beijing","cityname":"北京","city":"101010100","temp":"9","tempf":"48","WD":"东北风","wde":"NE","WS":"2级","wse":"7km\/h","SD":"65%","sd":"65%","qy":"1022","njd":"17km","time":"18:10","rain":"0","rain24h":"0","aqi":"25","aqi_pm25":"25","weather":"多云","weathere":"Cloudy","weathercode":"d01","limitnumber":"1和6","date":"03月30日(星期三)"}
```

## 历史上的今天
前面已经从中文维基百科上的历史上的今天抓取了所有的数据并生成了JSON文件，现在拿过来直接使用，
详细获取数据，请参考：[https://github.com/i-sync/history_of_today](https://github.com/i-sync/history_of_today)