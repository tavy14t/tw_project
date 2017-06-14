import json
import urllib2

from datetime import date


class Lanyrd(object):
    def __init__(self):
        pass

    def search(self, query):
        results = []
        for row in self._get("search/?q=%s" % (query))['sections']:
            results = results + row['rows']
        return results

    def popular(self):
        results = []
        for row in self._get("search/")['sections']:
            results = results + row['rows']
        return results

    def event(self, slug, year=date.today().year):
        return self._get("%s/%s/" % (year, slug))

    def speakers(self, slug, year=date.today().year):
        results = []
        for row in self._get("%s/%s/speakers/" % (year, slug))['sections']:
            results = results + row['rows']
        return results

    def attendees(self, slug, year=date.today().year):
        results = []
        for row in self._get("%s/%s/attendees/" % (year, slug))['sections']:
            results = results + row['rows']
        return results

    def schedule(self, slug, year=date.today().year):
        results = []
        for row in self._get("%s/%s/schedule/" % (year, slug))['sections']:
            results = results + row['rows']
        return results

    def profile(self, username):
        return self._get("profile/%s/" % (username))

    def future_events(self, username):
        return self._get("profile/%s/action/" % (username))['events']

    def _get(self, path):
        url = 'http://lanyrd.com/' + path
        print url
        response = urllib2.urlopen(url)
        #print response.read()
        data = response.read()
        json_data = json.loads(data)
        response.close()
        return json_data


lanyrd = Lanyrd()
#attendees = lanyrd.attendees("socallinuxexpo","2013")
profile = lanyrd.profile("garethgreenaway")