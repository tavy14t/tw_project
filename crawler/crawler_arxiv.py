import urllib2
import traceback
import time
import tempfile
import pycurl
import re
import urlparse

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


def download_file(url, fn, httpheaders):
    print 'DLD_SRC: {0}'.format(url)
    print 'DLD_DST: {0}'.format(fn)
    url = url.strip()
    fh = open(fn, 'wb')
    fh_temp = tempfile.TemporaryFile()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, fh.write)
    curl.setopt(curl.HEADERFUNCTION, fh_temp.write)
    curl.setopt(curl.HTTPHEADER, httpheaders)
    curl.setopt(curl.FRESH_CONNECT, 1)
    curl.setopt(curl.FOLLOWLOCATION, 1)
    curl.setopt(curl.SSL_VERIFYPEER, 0)
    curl.setopt(curl.SSL_VERIFYHOST, 0)
    curl.setopt(curl.TIMEOUT, 60 * 15)
    curl.setopt(curl.FAILONERROR, 1)
    curl.setopt(curl.FORBID_REUSE, 1)
    curl.perform()
    curl.close()
    fh.close()
    fh_temp.seek(0)
    headers = fh_temp.read()
    fh_temp.close()
    return headers


def download_file_redir(url, fn, httpheaders=None):
    if httpheaders is None:
        httpheaders = ['User-Agent: "Mozilla/4.0"']
    url2 = url
    while True:
        headers = download_file(url2, fn, httpheaders)
        for line in headers.split('\n'):
            if "Location" in line:
                print 'DLD_REDIR_HTTP: {0}'.format(
                    line.split(": ", 1)[1].strip())
        data = open(fn, 'rb').read(4 * 1024)
        urls = re.findall('<meta[^>]*?url=(.*?)["\']',
                          data, flags=re.IGNORECASE)
        if urls:
            for item in urls:
                print 'DLD_REDIR_META: {0}'.format(item)
            url2 = urlparse.urljoin(url, urls[0].strip())
        else:
            return url2
