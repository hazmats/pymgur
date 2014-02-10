#!/usr/bin/env python
import sys
import requests
import getpass
from bs4 import BeautifulSoup

# Pull the name/pwd from CLI args/prompt
# The getpass lib pulls the library without it going into command history
# or being displayed on the screen. Strip anything weird.
imun  = sys.argv[1].strip()

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
cmnts = []
ctxt = {}

# login will submit the username/password, validate a successful auth response, and return the session object.
# The session object will maintain cookies/auth status across requests.
session = requests.Session()

def login():
	"""
	Authenticates existing session object with host using provided username and password.
	Expects no input.
	Returns None.
	"""
	impwd = getpass.getpass("imgur pwd: ").strip()
	pdata = {'username': imun, 'password': impwd, 'remember': 'remember', 'submit_form': 'Sign+in' }
	# Create a session object to snag cookies and authenticate.
	try:
		login = s.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, allow_redirects=False)
		#login = session.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, proxies=prx, verify=False, allow_redirects=False)
	except:
		print 'Some shit be bad.'
		print login
	if login.status_code == 302:
		#return dict(s.cookies.get_dict())
		return True
	else:
		print 'fail omg'
		print login.status_code
		exit(2)
	# Remove the Referer header, hoping requests will take care of this
	del headers['Referer']


def get_profile(target):
	"""
	Hit the profile page of our target and return the soup object.
	Expects the username to be passed in as 'target'
	Returns a list of the BS profile soup and current reputation.
	"""
	prof = session.get('http://'+host+'/user/'+target, headers=headers, proxies=prx)
	if prof.status_code == 404:
		print "User %s not found.\nExiting." % target
		exit(2)
	else:
		soup = BeautifulSoup(prof.text)
		return soup, soup.find('span', class_='stat').text

def extract_comments(soup):
	"""
	Expects a BeautifulSoup object of a comments page.
	Append all of the comment IDs to the cmnts list and return how many
	were found. This lets us know when we reach the last page.
	"""
	found = 0
	for x in soup.find_all('div', class_='caption'):
		cmnts.append(x['data'])
		ctxt[x['data'] = x.find_all('div', class_='usertext textbox first1')[0].find_all('span')[2].string.strip()
		found += 1
	return found

def get_all_comments(target):
	getmore = True
	page = 0
	rsptimes = []
	while getmore == True:
		req = session.get('http://'+host+'/user/'+target+'/index/newest/page/'+str(page))
		rsptimes.append(req.elapsed)
		csoup = BeautifulSoup(req.text)
		fetched = extract_comments(csoup)
		page += 1
		print "[%d comments collected]" % (len(cmnts))
		if fetched != 20:
			getmore = False
			print "Last fetch returned %d comments. Last page reached." % fetched
			print str(len(cmnts)) + " total comments."
			break
	# The 'sid' value is passed on up/down votes. Slurp it out of the soup.
	# Create the list for comment IDs
	global sid 
	sid = csoup.find('input', id='sid')['value']


def vote(commid, action, itype, reps=len(cmnts)):
	"""
	Accepts list of commentIDs, which type of vote to perform, type of comment.  Uses session to send post data
	and cycles through list of ID's and up/down votes until end of list.
	"""
	pdata = {'sid': sid, 'vote': action, 'type': itype} 
	testcmnts = True
	maxcmnts = 0
	#to use later when done testing: while maxcmnts != reps:
	for comment in commid[0:5]:
		#dv = session.post('http://'+host+'/gallery/action/vote/'+comment, data=pdata, proxies=prx)
		dv = session.post('http://'+host+'/gallery/action/vote/'+comment, data=pdata)
		print "Submitted for..."
		print comment
		print dv.elapsed

print "Logging in..."
login()
print "Logged in..."
get_all_comments(sys.argv[2])
print "Comments fetched."
vote(cmnts, sys.argv[3], 'caption')
