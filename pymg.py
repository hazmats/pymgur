#!/usr/bin/env python
import sys
import requests
import getpass
from bs4 import BeautifulSoup

# Pull the name/pwd from CLI args/prompt
# The getpass lib pulls the library without it going into command history
# or being displayed on the screen. Strip anything weird.
imun  = sys.argv[1].strip()
impwd = getpass.getpass("imgur pwd: ").strip()

# Debugging proxies
prx = { 'http': 'http://192.168.1.213:8080', 'https': 'http://192.168.1.213:8080' }

# Define some params
# host so we can switch to localhost for testing
# pdata is our POST data
# headers are static for now. Want to cycle through a list randomly in future.
host = 'imgur.com'
headers = {
   'Cache-Control': 'max-age=0',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Origin': 'https://imgur.com',
   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
   'Referer': 'https://imgur.com/include/signin-iframe.html'
}

# login will submit the username/password, validate a successful auth response, and return the session object.
# The session object will maintain cookies/auth status across requests.

def login():
	pdata = {'username': imun, 'password': impwd, 'remember': 'remember', 'submit_form': 'Sign+in' }
	# Create a session object to snag cookies and authenticate.
	s = requests.Session()
	try:
		#login = s.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, allow_redirects=False)
		login = s.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, proxies=prx, verify=False, allow_redirects=False)
	except:
		print 'Some shit be bad.'
		print login
	if login.status_code == 302:
		#return dict(s.cookies.get_dict())
		return s
	else:
		print 'fail omg'
		print login.status_code
		exit(2)

# Begin the session and authenticate.
# Remove the Referer header, hoping requests will take care of this
session = login()
del headers['Referer']

# The 'sid' value is passed on up/down votes. Slurp it out of the soup.
# Create the list for comment IDs
#sid = soup.find('input' id='sid')['value']
cmnts = []

def get_profile(target):
	# Hit the profile page of our target and return the soup object.
	# Also return current reputation score.
	prof = session.get('http://'+host+'/user/'+target, headers=headers, proxies=prx)
	if prof.status_code == 404:
		print "User %s not found.\nExiting." % target
		exit(2)
	else:
		soup = BeautifulSoup(prof.text)
		return soup, soup.find('span', class_='stat').text

def get_comments(soup):
	# Append all of the comment IDs to the cmnts list and return how many
	# were found. This lets us know when we reach the last page.
	found = 0
	for x in soup.find_all('div', class_='caption'):
		cmnts.append(x['data'])
		found += 1
	return found

def page_comments(page, target):
	# Comments are returned 20 per page, so submit a request for the next page.
	soup = BeautifulSoup(s.get('http://'+host+'/user/'+target+'/index/newest/page/'+page+'?scrolling'))
	return soup

user = get_profile(sys.argv[2])
print user[1]
