from pyslideshare2 import pyslideshare

api_key = 'YqGq6EaQ'
secret_key = 'hMhd6iP1'

obj = pyslideshare.pyslideshare(locals(), verbose=True)
json = obj.get_slideshow_by_tag(tag='java', limit='5')

if not json:
    import sys

    print >> sys.stderr, 'No response. Perhaps slideshare down?'
    sys.exit(1)

print 'Total slideshows for this Tag : ', json.Tag.count
slideshows = json.Tag.Slideshow
for show in slideshows:
    print 'Name : %s, Views : %s' % (show.Title, show.Views)


