#!/usr/bin/env python
import httplib as ht
import urllib as url
import sys

imcookie = sys.argv[1]
imgid = sys.argv[2]

imghost = "imgur.com"
#imghost = "localhost:81"

def imgfav(imcookie, imgid, imghost):
   headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain", "Referer": "http://imgur.com/", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0", "Cookie" : "IMGURSESSION=%s" % imcookie, "X-Requested-With": "XMLHttpRequest"}
   params = url.urlencode({"ajax": "true"})
   conn = ht.HTTPConnection(imghost)
   conn.request("POST", "/%s/fav.json" % imgid, params, headers)
   resp = conn.getresponse()
   print resp.status
   print resp.getheaders()
#   body = resp.read()
#   print body
   conn.close

imgfav(imcookie, imgid, imghost)
