# -*- coding: utf-8 -*-
#
# Weather Bot
#
# Monitor the feed provided by the gov (https://data.gov.hk/en-data/provider/ hk-hko) 
# Relay the update to user via telegram bot (https://core.telegram.org/bots)
#
# Johnny Chen
# 2016/08/20

import xml.etree.ElementTree as ET
import requests
import re

class weather:
    def get_current(self):
        pass
    def get_warning(self):
        pass
    def get_pubdate(self):
        pass

class English(weather):
    def __init__(self):
        self.current_xml= 'http://rss.weather.gov.hk/rss/CurrentWeather.xml'
        self.warning_xml= 'http://rss.weather.gov.hk/rss/WeatherWarningBulletin.xml'

    def get_current(self):
        xml = requests.get(self.current_xml)
        tree = ET.fromstring(xml.text)
        item = tree.find('channel/item')
        result = item.find('description').text
        result = re.search('<p>([\s\S]+)<p>', result)
        result = result.group(1)
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        result = re.sub('<[^<>]+>',' ', result)
        return result

    def get_warning(self):
        xml = requests.get(self.warning_xml)	
        tree = ET.fromstring(xml.text)
        item = tree.find('channel/item')
        result = item.find('description').text
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        return result

    def get_pubdate(self):
        xml = requests.get(self.warning_xml)	
        tree = ET.fromstring(xml.text)
        item = tree.find('channel')
        result = item.find('pubDate').text
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        return result

class Traditional(weather):
    def __init__(self):
        self.current_xml = 'http://rss.weather.gov.hk/rss/CurrentWeather_uc.xml'
        self.warning_xml = 'http://rss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml'

    def get_current(self):
        xml = requests.get(self.current_xml)
        tree = ET.fromstring(xml.text)
        item = tree.find('channel/item')
        result = item.find('description').text
        result = re.search('<br/><br/>([\s\S]+)<p>', result)
        result = result.group(1)
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        result = re.sub('<[^<>]+>',' ', result)
        return result

    def get_warning(self):
        xml = requests.get(self.warning_xml)	
        tree = ET.fromstring(xml.text)
        item = tree.find('channel/item')
        result = item.find('description').text
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        return result

    def get_pubdate(self):
        xml = requests.get(self.warning_xml)	
        tree = ET.fromstring(xml.text)
        item = tree.find('channel')
        result = item.find('pubDate').text
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        return result		
		
class Simplified(weather):
    def __init__(self):
        self.current_xml = 'http://gbrss.weather.gov.hk/rss/CurrentWeather_uc.xml'
        self.warning_xml = 'http://gbrss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml'
		
    def get_current(self):
        xml = requests.get(self.current_xml)
        tree = ET.fromstring(xml.text)
        item = tree.find('channel/item')
        result = item.find('description').text
        result = re.search('<br/><br/>([\s\S]+)<p>', result)
        result = result.group(1)
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        result = re.sub('<[^<>]+>',' ', result)
        return result

    def get_warning(self):
        xml = requests.get(self.warning_xml)	
        tree = ET.fromstring(xml.text)
        item = tree.find('channel/item')
        result = item.find('description').text
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        return result
		
    def get_pubdate(self):
        xml = requests.get(self.warning_xml)	
        tree = ET.fromstring(xml.text)
        item = tree.find('channel')
        result = item.find('pubDate').text
        result = re.sub('\s+',' ', result)
        result = result.replace('<br/>', '\n')
        return result		
