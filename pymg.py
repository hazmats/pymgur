#!/usr/bin/env python
import sys
import requests
import getpass
import time
import random
from bs4 import BeautifulSoup

# Pull the name/pwd from CLI args/prompt
# The getpass lib pulls the library without it going into command history
# or being displayed on the screen. Strip anything weird.
imun  = sys.argv[1].strip()
#impwd = getpass.getpass("imgur pwd: ").strip()

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

# login will submit the username/password, validate a successful auth response, and return the session object.
# The session object will maintain cookies/auth status across requests.
session = requests.Session()

def login():
	"""
	Authenticates existing session object with host using provided username and password.
	Expects no input.
	Returns None.
	"""
	pdata = {'username': imun, 'password': impwd, 'remember': 'remember', 'submit_form': 'Sign+in' }
	# Create a session object to snag cookies and authenticate.
	try:
		#login = s.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, allow_redirects=False)
		login = session.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, proxies=prx, verify=False, allow_redirects=False)
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

# The 'sid' value is passed on up/down votes. Slurp it out of the soup.
# Create the list for comment IDs
sid = soup.find('input' id='sid')['value']

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
		if page % 10 == 0:
			sleeptime = random.uniform(0.203, 0.522)
			print "Sleeping for %.3f." % sleeptime
			time.sleep(sleeptime)
	print "Response Times"
	print rsptimes
	print "Average Response Times:"
	print sum(rsptimes) / float(len(rsptimes))


def vote(commid, action, itype, reps=len(commid)):
	"""
	Accepts list of commentIDs, which type of vote to perform, type of comment.  Uses session to send post data
	and cycles through list of ID's and up/down votes until end of list.
	"""
	pdata = {'sid': sid, 'vote': action, 'type': itype} 
	maxcmnts = 0
	#to use later when done testing: while maxcmnts != reps:
	while testcmnts == True: #while loop to limit # of downvotes to test times
		for comment in commid:
			dv = session.post('/gallery/action/vote/'+comment, data=pdata)
			print dv.elapsed
			maxcmnts += 1
			if maxcmnts >= 6: #limiting test to 5 cycles
				testcmnts = False

get_all_comments(sys.argv[2])
