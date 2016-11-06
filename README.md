每日一页
====
这个程序是一个超级简单的小博客系统。它的功能有：

- 每天自动从[喷嚏图卦](http://www.pentitugua.com/rss.xml)抓取至多20条当天的天下大事
- 每天从[百度开放平台](http://developer.baidu.com/map/carapi-7.htm)抓取当天的天气情况
- 以短信息的方式呈现用户状态
- 每天一个页面

我希望它能够提供方便打印的格式，以便于用户创建自己的日记书。

RESTful接口
-----

| 方法  | 路径             | 解释                          |
|------|------------------|------------------------------|
| GET  | /autolog/v1/info | 获取日志的概况                  |
| GET  | /autolog/v1/logs/{date} | 获取某一天的日志         |
| GET  | /autolog/v1/logs?oldest={oldest_date}&newest={newest_date} | 获取某一时间段的日志 |
| POST | /autolog/v1/logs?token={token} | 发布一条消息 |

### 获取日志概况 ###

例子：

    GET http://{ip}:{port}/autolog/v1/info

    200 OK

    {
        "logs": [
            "2016-11-05",
            "2016-11-04"
        ]
    }

### 获取某一天的日志 ###

例子:

    GET http://{ip}:{port}/autolog/v1/logs/2016-11-04

    200 OK

    {
        "date": "2016-11-04",
        "weekday": 5,
        "weather": {
            "condition": "晴",
            "temperature": "23 ~ 11℃",
            "pm25": "97",
            "dayPictureUrl" : "http://api.map.baidu.com/images/weather/day/qing.png",
            "nightPictureUrl" : "http://api.map.baidu.com/images/weather/night/qing.png",
            "wind": "南风微风",
            "city": "南京"
        },
        "news": {
            "link": "https://www.dapenti.com/blog/more.asp?name=xilei&id=116039",
            "titles": [
                "我国首枚重型运载火箭长征5号成功发射",
                "人大常委会将主动就基本法条款释法",
                "国家网信办发布《互联网直播服务管理规定》",
                "楼继伟：正积极推进房地产税和个税改革",
                "环保部：今冬雾霾频率偏高 但峰值不会爆表",
                "中国代表审查冰岛、津巴布韦、叙利亚人权状况",
                "北苑车祸官方通报",
                "东方网总裁致马化腾公开信：企鹅帝国将挑战国家权威",
                "谢亚龙再被建议减刑一年 已获六次表扬",
                "宋祖英老区唱响《十送红军》",
                "重庆一男子拿花圈求婚 女孩果断拒绝",
                "有房的，你还创个什么业？创业的，你买得起房吗？",
                "朴槿惠再次发表国民电视讲话 否认被邪教控制",
                "驻韩美军司令称最快于明年上半年完成“萨德”入韩",
                "英国法院裁定议会必须对脱欧投票",
                "美入学考试ACT取消10月亚洲部分考生写作成绩",
                "法国共和党举行第二次初选辩论",
                "日本成功复原一架零式战斗机并试飞",
                "日本报社用人工智能完成创刊纪念报道 有意保留错别字",
                "洪秀柱：年底蓝营县市登陆办农产品展",
            ]
        },
        "logs": [
            {
                "time": "2016-11-04 16:52:04+08:00",
                "content": "我今天在图书馆待了一天，看了一本讲建筑的书"
            },
            {
                "time": "2016-11-04 19:20:34+08:00",
                "content": "晚上找了一家中介公司，蹭网看片子"
            }
        ]
    }

### 获取某一时间段的日志 ###

例子:

    GET http://{ip}:{port}/autolog/v1/logs?oldest=2016-11-04&newest=2016-11-05

    200 OK

    {
        "logs": [
            {
                "date": "2016-11-05"
                // other stuff
            },
            {
                "date": "2016-11-04"
                // other stuff
            }
        ]
    }

### 发布一条消息 ###

例子:

    POST http://{ip}:{port}/autolog/v1/logs?token=the_super_magic_token_only_author_knows

    201 Created

    {
        "result": "success"
    }

## 网页显示 ##

应该用一个单页的小程序就可以搞定了。

## Environment variables ##

- BAIDU_TOKEN
- DATA_DIR
- TZ
- CITY
