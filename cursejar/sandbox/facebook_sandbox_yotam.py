__author__ = 'yotam'
# coding: utf-8

import facebook
import os
from pprint import pprint

graph = facebook.GraphAPI()
graph.access_token = facebook.get_app_access_token(os.environ['FACEBOOK_APP_ID'], os.environ['FACEBOOK_SECRET_KEY'])

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
