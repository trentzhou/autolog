# -*- coding: utf-8 -*-
import requests
import os
import logging
import json
import feedparser
import re

LOGGER = logging.getLogger("FetchData")

class GetWeatherError(Exception):
    pass

def get_weather(baidu_token, city):
    """
    Get today's weather information from baidu.

    :param baidu_token: Baidu's developer token
    :param city: city name
    """
    # convert the unicode string to utf-8 str
    if isinstance(city, str):
        city = city.decode('utf-8')
    url = "http://api.map.baidu.com/telematics/v3/weather?" \
          "location={0}&output=json&ak={1}".format(city.encode('utf-8'), baidu_token)
    LOGGER.debug(u"Getting weather information for city {0}".format(city))
    result = requests.get(url)
    if result.status_code == 200:
        data = result.json()
        LOGGER.debug(u"Weather information for city {0}: {1}".format(city,
                        json.dumps(data, indent=4, sort_keys=True)))
        return data
    raise GetWeatherError("Failed to get weather for city {0}".format(city))

def get_news():
    """
    Get latest news from http://www.pentitugua.com/rss.xml
    :return dict: the result as a dict.
    {
        'date': '2016-11-03',
        'news': [
            "xxx",
            "yyy",
        ],
        'link': 'https://www.dapenti.com/blog/more.asp?name=xilei&id=116011'
    }
    """
    url = 'http://www.pentitugua.com/rss.xml'
    feed = feedparser.parse(url)
    item = feed['items'][0]
    news = []
    result = {
        'date': item['published'],
        'link': item['link'],
        'news': news
    }
    # add news titles
    news_text = item['summary']
    regex = re.compile(".*【\d+】(.*)")
    cleanr = re.compile('<.*?>')
    for line in news_text.split("\n"):
        line_utf8 = line.encode('utf-8')
        if len(news) < 20:
            match = regex.match(line_utf8)
            if match:
                title = match.group(1)
                cleantext = re.sub(cleanr, '', title)
                news.append(cleantext.decode('utf-8'))
    return result
