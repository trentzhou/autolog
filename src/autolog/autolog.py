# -*- coding: utf-8 -*-
from .data_access import DataAccess
import datetime
import fetch_data
import logging

LOGGER = logging.getLogger('AutoLog')

class AutoLog(object):
    def __init__(self, data_dir, baidu_token, city):
        self.data_dir = data_dir
        self.data_access = DataAccess(data_dir)
        self.baidu_token = baidu_token
        self.city = city

    def _new_log(self, date=None):
        if not date:
            date = datetime.date.today()
        LOGGER.debug("Creating new log for {0}".format(date))
        return {
            "date": date.isoformat(),
            "weekday": date.isoweekday(), # sunday=7, monday=1
            "weekday_text": u"星期" + [u"一", u"二", u"三", u"四", u"五", u"六", u"日"][date.isoweekday() - 1],
            "weather": None,
            "news": None,
            "logs": []
        }

    def list(self):
        return self.data_access.list_logs()

    def fetch(self):
        today = datetime.date.today()
        log = self.data_access.read_log(today)
        if not log:
            log = self._new_log()
        if not log['weather']:
            weather = fetch_data.get_weather(self.baidu_token, self.city)
            if weather['status'] == 'success' and weather['date'] == log['date']:
                w = {}
                today_weather = weather['results'][0]['weather_data'][0]
                w['condition'] = today_weather['weather']
                w['wind'] = today_weather['wind']
                w['temperature'] = today_weather['temperature']
                w['city'] = weather['results'][0]['currentCity']
                w['pm25'] = int(weather['results'][0]['pm25'])
                w['dayPictureUrl'] = today_weather['dayPictureUrl']
                w['nightPictureUrl'] = today_weather['nightPictureUrl']

                if w['pm25'] > 100:
                    pm25_color = 'red'
                elif w['pm25'] > 50:
                    pm25_color = 'orange'
                else:
                    pm25_color = 'green'
                w['pm25_color'] = pm25_color
                log['weather'] = w
                LOGGER.debug(u"Got weather for {0}: {1}: {2}".format(weather['date'],
                                                                    w['condition'],
                                                                    w['temperature']))
                self.data_access.write_log(log)
        # get the latest news
        news = fetch_data.get_news()
        format = '%a, %d %b %Y %H:%M:%S %Z'
        t = datetime.datetime.strptime(news['date'], format)
        LOGGER.debug("Date for latest news is {0}".format(t))
        # get the log for the date
        log = self.data_access.read_log(t.date())
        if not log:
            log = self._new_log(t.date())
        if not log['news']:
            log['news'] = {
                'titles': news['news'],
                'link': news['link']
            }
            LOGGER.debug(u"Got news for {0}: {1}".format(t.date(), "\n".join(news['news'])))
            self.data_access.write_log(log)

    def get(self, date):
        return self.data_access.read_log(date)

    def put(self, msg):
        today = datetime.date.today()
        log = self.data_access.read_log(today)
        if not log:
            log = self._new_log()
        log['logs'].append(msg)
        LOGGER.debug(u"Appending msg {0}".format(msg))
        self.data_access.write_log(log)

def test():
    logging.basicConfig(level=logging.DEBUG)
    l = AutoLog('/tmp/autolog', '1ef059103bc02c7f1cd9b35e5bcab3ab', '南京')
    l.fetch()
