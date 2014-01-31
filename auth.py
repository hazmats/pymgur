#!/usr/bin/env python
import sys
import requests
import getpass

# Pull the name/pwd from CLI args/prompt
# The getpass lib pulls the library without it going into command history
# or being displayed on the screen. Strip anything weird.
imun  = sys.argv[1].strip()
impwd = getpass.getpass("imgur pwd: ").strip()

# Define some params
# host so we can switch to localhost for testing
# pdata is our POST data
# headers are static for now. Want to cycle through a list randomly in future.
host = 'imgur.com'
pdata = {'username': imun, 'password': impwd, 'remember': 'remember', 'submit_form': 'Sign+in' }
headers = {
   'Cache-Control': 'max-age=0',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Origin': 'https://imgur.com',
   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
   'Referer': 'https://imgur.com/include/signin-iframe.html'
}

gh = requests.get('http://imgur.com/', headers=headers)

login = requests.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers)
