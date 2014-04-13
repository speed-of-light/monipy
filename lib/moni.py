import urllib2, base64, cStringIO
import os, datetime
from PIL import Image

class Moni:
  def __init__(self, dvr_root, port, user, pw, chn):
    reqs = []
    for ch in range(chn):
      req = urllib2.Request("http://{}:{}/cgi-bin/net_jpeg.cgi?ch={}".format(dvr_root, port, ch))
      base64string = base64.encodestring("{}:{}".format(user, pw)).replace('\n', '')
      req.add_header("Authorization", "Basic %s" % base64string)
      reqs.append(req)
    self.reqs = reqs

  def save_cap(self, ch):
    resp = urllib2.urlopen(self.reqs[ch])
    dtn = datetime.datetime.now()
    html = resp.read()
    img = Image.open(cStringIO.StringIO(html))
    self.__check_and_save(ch, img, dtn)

  def __check_and_save(self, ch, img, now):
    slug = "tmp/ch{}/{}".format(ch, now.hour)
    if not os.path.exists(slug):
      os.makedirs(slug)
    img.save("{}/{}.jpg".format(slug, now.strftime("%M%S")), 'jpeg')

