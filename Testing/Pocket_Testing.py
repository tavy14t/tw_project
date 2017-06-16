import os
import sys
import requests
import time
from pocket import Pocket
import webbrowser
import collections
import json

sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trex.settings")
import django

django.setup()
from restapi.models import *
from random import randint

# POCKET_CONSUMER_KEY = '67853-fa80baf944f56fd495dab319' #Desktop
POCKET_CONSUMER_KEY = '67853-17e07228b29f7c44ef6d2784'  # Web
REDIRECT_URI = 'http://localhost:8000/home/about'
'''
# connecting to pocket API; pocket_api stores the http response
pocket_api = requests.post('https://getpocket.com/v3/oauth/request',
                           data={'consumer_key': POCKET_CONSUMER_KEY,
                                 'redirect_uri': 'http://localhost:8000/home/about'})

print pocket_api.status_code  # if 200, it means all ok.

print pocket_api.headers  # prints in JSON format

print pocket_api.text

code = pocket_api.text.split('=')[1]

print code

os.system('chrome "https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}"'.format(code, 'http://localhost:8000/home/about'))

time.sleep(5)

print '--------------------------------------------'

pocket_auth = requests.post('https://getpocket.com/v3/oauth/authorize',
                            data={'consumer_key': POCKET_CONSUMER_KEY,
                                  'code': code})
print pocket_auth.status_code
print pocket_auth.text
pocket_access_token = pocket_auth.text.split('=')[1].split('&')[0]
print '--------------------------------------------'

request_token = Pocket.get_request_token(consumer_key=POCKET_CONSUMER_KEY, redirect_uri=REDIRECT_URI)
print 1
# URL to redirect user to, to authorize your app
auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=REDIRECT_URI)
print 2
# os.system('chrome "{}"'.format(auth_url))
print auth_url
webbrowser.open_new_tab(auth_url)
user_credentials = Pocket.get_credentials(consumer_key=POCKET_CONSUMER_KEY, code=request_token)
time.sleep(3)
print 3
access_token = user_credentials['access_token']
print 4
pocket_instance = Pocket(POCKET_CONSUMER_KEY, access_token)




pocket_get = open('pocket_get.txt', 'w')


def recursive_keys(d, depth=0):
    for key in d:
        if isinstance(d[key], collections.Mapping):
            print ' ' * depth + key
            pocket_get.write(' ' * depth + key + '\n')
            recursive_keys(d[key], depth + 1)
        else:
            print ' ' * depth + key + ' ->' + unicode(d[key])
            pocket_get.write(' ' * depth + key + ' ->' + unicode(d[key]) + '\n')


d = pocket_instance.get()[0]['list']
for key in d:
    print d[key]['resolved_title'], d[key]['given_url']
# open('test.txt', 'w').write(str(pocket_instance.get()))

print '--------------------------------'

#access_token = 'd8830338-65cd-ef39-64db-ec5b99'

#pocket_instance = Pocket(POCKET_CONSUMER_KEY, access_token)

#sample = pocket_instance.get(detailType='complete')[0]
'''

with open('../result.json', 'r') as fp:
    pocket_request = json.load(fp)

pocket_posts = pocket_request['list']


def pretty(d, indent=0):
    for key, value in d.iteritems():
        print '  ' * indent + unicode(key)
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print '  ' * (indent + 1) + unicode(value)

data = {'posts': {}}

for post in pocket_posts:
    data['posts'][post] = {}
    data['posts'][post]['name'] = pocket_posts[post]['given_title']
    data['posts'][post]['embed_link'] = pocket_posts[post]['resolved_url']
    if 'tags' in pocket_posts[post]:
        data['posts'][post]['tags'] = [tag for tag in pocket_posts[post]['tags']]
    else:
        data['posts'][post]['tags'] = []

print data
# print [tag for tag in pocket_posts[post]]
'''
tags = []

for post in pocket_posts:
    #print post
    if 'tags' in pocket_posts[post]:
        tags.append(pocket_posts[post]['tags'])

print tags

pocket_api = requests.post('https://getpocket.com/v3/get',
                           data={'consumer_key': POCKET_CONSUMER_KEY,
                                 'access_token': access_token,
                                 'count': 30,
                                 'state': 'unread',
                                 'detailType': 'complete',
                                 })

# print pocket_api.headers

print pocket_api.text


e = json.loads(requests.post('https://getpocket.com/v3/get',
                             data={'consumer_key': POCKET_CONSUMER_KEY,
                                   'access_token': access_token,
                                   'count': 30,
                                   'state': 'unread',
                                   }).text)['list']
d = json.loads(pocket_api.text)['list']
for key in d:
    print set(d[key].keys()).difference(set(e[key].keys()))

e = [key]

# print d

# recursive_keys(pocket_instance.get()[0])
'''
