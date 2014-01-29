#!/usr/bin/env python
import httplib as ht
import urllib as url
import sys

# Get command line arguments for use later
imcookie = sys.argv[1]
imgid = sys.argv[2]

# In case we decide to change this (also for testing)
imghost = "imgur.com"
#imghost = "localhost:81"

# Begin function to add the image to your favorites
def imgfav(imcookie, imgid, imghost):
   # Add some headers to try to look normal. Also the cookie passed in from CLI that is our auth token
   headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain", "Referer": "http://imgur.com/", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0", "Cookie" : "IMGURSESSION=%s" % imcookie, "X-Requested-With": "XMLHttpRequest"}
   # Some ajax stuff in each request...
   params = url.urlencode({"ajax": "true"})
   # Fire up the connection and send a POST request with the image ID, parameters, and headers
   conn = ht.HTTPConnection(imghost)
   conn.request("POST", "/%s/fav.json" % imgid, params, headers)
   # Get the response and print it.
   resp = conn.getresponse()
   print resp.status
   print resp.getheaders()
#   body = resp.read()
#   print body
   conn.close

# Call the above function
imgfav(imcookie, imgid, imghost)
