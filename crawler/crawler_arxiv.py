import urllib2
import traceback
import time


base_link = 'https://arxiv.org'


def load_url(url):
    retry_max = 5
    retry = 0
    while retry < retry_max:
        retry += 1
        try:
            print 'QUERY: {0}'.format(url)
            request = urllib2.Request(
                url, None, {'User-agent': 'Mozilla/4.0 (compatible; ' +
                            'MSIE 5.5; Windows NT)'})
            data = urllib2.urlopen(request)
            data = data.read()
            return data
        except Exception:
            print '[ov] <', traceback.format_exc(), '>'
            time.sleep(10)
    return None
