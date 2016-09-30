#!/usr/bin/env python
#encoding=utf-8

__author__ = 'yuanbin'

import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("config.ini")

# ZSTACK
URL = ''
URL_RESULT = ''
NAME = ''
PASSWORD = ''

def import_config():
    global URL
    global URL_RESULT
    global NAME
    global PASSWORD

    URL = conf.get("zstack", "url")
    URL_RESULT = conf.get("zstack", "url_result")
    NAME = conf.get("zstack", "name")
    PASSWORD = conf.get("zstack", "password")

if URL == "":
    import_config()