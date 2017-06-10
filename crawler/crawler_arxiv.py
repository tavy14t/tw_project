import os
import urllib2
import re
import traceback
import time
import pycurl
import urlparse
import tempfile
import json
import unicodedata
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO


base_link = 'https://arxiv.org'


def convert_pdf(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    ceva = retstr.getvalue()
    retstr.close()

    ceva = ceva.decode('utf-8', 'ignore')
    return ceva.encode('ascii', 'ignore')
    return ceva


def printfl(data, fn='1.html'):
    with open(fn, 'w') as f:
        f.write(data)


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


def get_tags_and_link(html_data):
    r = '<li><b>cs\.[A-Z][A-Z] - [a-zA-Z,\- ]+</b> \(<a href=\"[^\"]+\">'
    r += 'new</a>,'
    link_r = '<a href=\"([^\"]+)\">'
    tag_r = '[A-Z][A-Z] - ([a-zA-Z,\- ]+)</b>'
    dict_list = []
    all_data = re.findall(r, html_data)
    for entry in all_data:
        tag = re.findall(tag_r, entry)[0]
        link = re.findall(link_r, entry)[0]
        this_dict = {}
        this_dict['tag'] = tag
        this_dict['link'] = base_link + link.rsplit('/', 1)[0] + '/current'
        dict_list.append(this_dict)

    return dict_list


def get_pdf_link(html_data):
    # r = '.+\[1\].+title="Download PDF">pdf</a>, <a href="([^"]+)" title='
    r = '.+\[1\].+a href="([^"]+)" title="Download PDF">pdf</a>'
    pdf_link = re.findall(r, html_data)[0]
    if pdf_link.startswith('/format'):
        pdf_link = '/pdf' + pdf_link[7:]
    if not pdf_link.endswith('.pdf'):
        pdf_link += '.pdf'
    if pdf_link.startswith('/ps/'):
        return base_link + pdf_link, pdf_link[4:]
    return base_link + pdf_link, pdf_link[5:]

def get_pdf_links(html_data):
    '''
    # r = '.+\[1\].+title="Download PDF">pdf</a>, <a href="([^"]+)" title='
    r = '.+\[1\].+a href="([^"]+)" title="Download PDF">pdf</a>'
    pdf_link = re.findall(r, html_data)[0]
    if pdf_link.startswith('/format'):
        pdf_link = '/pdf' + pdf_link[7:]
    if not pdf_link.endswith('.pdf'):
        pdf_link += '.pdf'
    if pdf_link.startswith('/ps/'):
        return base_link + pdf_link, pdf_link[4:]
    return base_link + pdf_link, pdf_link[5:]
    '''
    pdf_names = [x.split('"')[1].split('/')[-1] for x in html_data.split('<span class="list-identifier">')[1:]]
    pdf_titles = [x.split('</div>')[0][:-1] for x in
                  html_data.split('<div class="list-title mathjax">\n<span class="descriptor">Title:</span> ')[1:]]
    pdf_tags = [x.splitlines()[0].split(";") for x in html_data.split(
        '<div class="list-subjects">\n<span class="descriptor">Subjects:</span> <span class="primary-subject">')[1:]]
    for i in range(len(pdf_tags)):
        pdf_tags[i] = [x.split("(")[0].strip() for x in pdf_tags[i]]
    list = []
    for name in pdf_names:
        d = {}
        d['link'] = 'https://arxiv.org/pdf/{}.pdf'.format(name)
        d['title'] = pdf_titles[i]
        d['tags'] = pdf_tags[i]
        list.append(d)
    return list


def download_file(url, fn, httpheaders):
    print 'VTF ' + url
    print 'DLD_SRC: {0}'.format(url)
    print 'DLD_DST: {0}'.format(fn)
    url = url.strip()
    print(fn)
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


def download_pdfs(d):
    for pdf in d:
        print('Downloading pdf: {}'.format(pdf['title']))
        download_file(pdf['link'], 'pdfs/{}_{}_{}.pdf'.format('_'.join(pdf['tags']), pdf['title'], pdf['link'].rsplit('/', 1)[-1]), ['User-Agent: "Mozilla/4.0"'])
        #os.rename('pdfs/{}'.format(, )

if not os.path.exists('pdfs'):
    os.makedirs('pdfs')

tags_and_links = get_tags_and_link(load_url('https://arxiv.org/archive/cs'))
for d in tags_and_links:
    link = d['link']
    download_pdfs(get_pdf_links(load_url(link)))
exit(1)

###<p  style=" margin: 12px auto 6px auto; font-family: Helvetica,Arial,Sans-serif; font-style: normal; font-variant: normal; font-weight: normal; font-size: 14px; line-height: normal; font-size-adjust: none; font-stretch: normal; -x-system-font: none; display: block;">   <a title="View Combinatorics_Computational Geometry_Mobile vs. Point Guards_1706.00091.PDF on Scribd" href="https://www.scribd.com/document/350813872/Combinatorics-Computational-Geometry-Mobile-vs-Point-Guards-1706-00091-PDF#from_embed"  style="text-decoration: underline;" >Combinatorics_Computational Geometry_Mobile vs. Point Guards_1706.00091.PDF</a> by <a title="View Anonymous 4TlipFwW94's profile on Scribd" href="https://www.scribd.com/user/360634909/Anonymous-4TlipFwW94#from_embed"  style="text-decoration: underline;" >Anonymous 4TlipFwW94</a> on Scribd</p><iframe class="scribd_iframe_embed" src="https://www.scribd.com/embeds/350813872/content?start_page=1&view_mode=scroll&access_key=key-M3KttBUl7t0uqQSFYNYu&show_recommendations=true" data-auto-height="false" data-aspect-ratio="0.7729220222793488" scrolling="no" id="doc_3063" width="100%" height="600" frameborder="0"></iframe>

new_dict_list = []
tags_and_links = get_tags_and_link(load_url('https://arxiv.org/archive/cs'))
for d in tags_and_links:
    link = d['link']
    pdf_link, pdf_name = get_pdf_link(load_url(link))
    download_file_redir(pdf_link, 'pdfs/' + pdf_name)

    ###########
    #d['text'] = convert_pdf('pdfs/' + pdf_name)
    #print len(d)
    ###########
    # try:
    #     d['text'] = convert_pdf('pdfs/' + pdf_name)
    new_dict_list.append(d)
    # except Exception:
    #     print 'this pdf (%s) is not ok' % pdf_name

printfl(json.dumps(new_dict_list, indent=4), 'text.txt')

'''
text = json.dumps(d, indent=4)
text = text.replace('\\n', '\n')
i = 0
while i < len(text):
    if re.findall('\\u.{4}', text[i:i + 6]):
        text = text[:i] + text[i + 6:]
        i -= 6
    i += 1
'''
