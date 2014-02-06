__author__ = 'yotam'
__author__ = 'shaked'
# coding: utf-8

import facebook
from pprint import pprint
import cursejar.cursejar.settings.local as local

graph = facebook.GraphAPI()
graph.access_token = facebook.get_app_access_token(local.FACEBOOK_APP_ID, local.FACEBOOK_SECRET_KEY)

results = graph.get_connections('715900751', 'friends')
pprint(results)
#
# name = 'poetryslamisrael'
# select_self_published_status_query = """
# select about, fan_count, name, page_id, username
# from
# page
# where name={0}""".format(name)
#
# results2 = graph.fql(query=select_self_published_status_query)
# print results2
