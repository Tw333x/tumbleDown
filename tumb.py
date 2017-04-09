import os, sys
from shutil import copyfileobj
from urllib import urlopen
from xml.etree import ElementTree as ET
from termcolor import colored

# colors for output
ok = 'green'
success = 'cyan'
warn = 'magenta'
info = 'yellow'
alert = 'red'

# lets make a nice clean interface to start
os.system('clear')

if len(sys.argv) != 2:
    print >> sys.stderr, "Pass tumblr name as argument"
    sys.exit()

tumblr_name = sys.argv[1]
api_endpoint = 'http://%s.tumblr.com/api/read' % tumblr_name
start = 0
num = 50
post_count = 1

grabbed = 0

print colored ('Researching : %s' %tumblr_name, success)

path = 'reddit/tumb/%s' %tumblr_name

# make the directory if it does not exists already
if not os.path.exists(path):
    os.makedirs(path, 0777)

# make the thumbs directory too
if not os.path.exists(path + '/_thumbs/'):
    os.makedirs(path + '/_thumbs/')
    os.chmod(path+ '/_thumbs', 0777)

while post_count:
    resp = urlopen("%s?type=photo&start=%s&num=%s" % (api_endpoint, start, num))
    content = resp.read()
    tree = ET.fromstring(content)
    post_tags = tree.findall(".//post")
    post_count = len(post_tags)
    for post_tag in post_tags:
        post_id = post_tag.attrib['id']
        post_date = post_tag.attrib['date-gmt'].split(" ")[0]
        outname = "reddit/tumb/%s/%s-%s.jpg" % (tumblr_name, post_date, post_id)
        if os.path.exists(outname):
            print "%s already downloaded" % outname
            continue
        for photo_tag in post_tag.findall(".//photo-url"):
            if photo_tag.attrib['max-width'] == "1280":
                photo_url = photo_tag.text
                resp = urlopen(photo_url)
                outfile = open(outname, 'w')
                copyfileobj(resp, outfile)
                outfile.close()
                
                grabbed = grabbed + 1
                print colored('%s' %(grabbed), info)
                print "Downloaded %s to %s" % (photo_url, outname)
    start += num
