import vimeo
import json

VIMEO_ACCESS_TOKEN = 'c1b4884633f99182e479270afc801dc8'
VIMEO_CLIENT_ID = 'd7b506963366fc024915e0a74b341361c08233bd'
VIMEO_CLIENT_SECRET = 'u3xHs+ff/PhLvQB/SxG/bY02xYIXCS1zD3s+CTzRonk2Od77JsI2Zq2CP5X0F22uPG3N' \
                      '+mTFulsTAaQuSO36RvYOYCqFvwdSI2ZFfj6XlmZiVR977UDFJtoRgOqhoboh'
'''
v = vimeo.VimeoClient(
    token=VIMEO_ACCESS_TOKEN,
    key=VIMEO_CLIENT_ID,
    secret=VIMEO_CLIENT_SECRET)

# Make the request to the server for the "/me" endpoint.
about_me = v.get('/me')

assert about_me.status_code == 200  # Make sure we got back a successful response.

with open('vimeo_result.json', 'r') as fp:
    about_me = json.load(fp)
    #json.dump(about_me.json(), fp)

for key in about_me:
    print key

print about_me['preferences']
'''

code = '8d8b8063c2e9d16380130ea33e208be30e4aaa01'

v = vimeo.VimeoClient(
    key=VIMEO_CLIENT_ID,
    secret=VIMEO_CLIENT_SECRET)

v.exchange_code(code, '')




#a = 'https://api.vimeo.com/oauth/authorize?scope=public+private&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fpocket%2Flogin&response_type=code&client_id=d7b506963366fc024915e0a74b341361c08233bd'
#b = 'https://api.vimeo.com/oauth/authorize?client_id=XXXXX&response_type=code&redirect_uri=XXXX.YYY/ZZZZZ&state=XXXXXX'