#!/usr/bin/env python
import sys
import requests
import random
import getpass
import argparse
from bs4 import BeautifulSoup

# Begin arg parsing with argparse.
parser = argparse.ArgumentParser(description='Do some imgr')
parser.add_argument('source', help='Source username from which to submit votes.', default='qazZAQQ')
parser.add_argument('target', help='Target username')
parser.add_argument('action', help='Accepts up, down, or veto.')
parser.add_argument('type', help='Accepts "image" or "caption"', default="caption")
args = parser.parse_args()


# Debugging proxies
prx = { 'http': 'http://192.168.1.213:8080', 'https': 'http://192.168.1.213:8080' }

# Define some params
# host so we can switch to localhost for testing
# pdata is our POST data
host = 'imgur.com'
cmnts = []
ctxt = {}

# login will submit the username/password, validate a successful auth response, and return the session object.
# The session object will maintain cookies/auth status across requests.
session = requests.Session()

# A list of User-Agent headers we can pull randomly from
userAgents = [
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; Deepnet Explorer 1.5.3; Smart 2x2; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Deepnet Explorer 1.5.3; Smart 2x2; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.1)',
	'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.13) Gecko/2009073022 EnigmaFox/3.0.13',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
	'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0',
	'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1',
	'Mozilla/5.0 (X11; Linux) KHTML/4.9.1 (like Gecko) Konqueror/4.9',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
	'Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
	'Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
	]

# Create the headers for our requests, randomly selecting the user-agent
headers = {
   'Cache-Control': 'max-age=0',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Origin': 'https://imgur.com',
   'User-Agent': random.choice(userAgents),
   'Referer': 'https://imgur.com/include/signin-iframe.html'
}
def login(srcuser):
	"""
	Authenticates existing session object with host using provided username and password.
	Expects no input.
	Returns None.
	"""
	impwd = getpass.getpass("imgur pwd: ").strip()
	pdata = {'username': srcuser, 'password': impwd, 'remember': 'remember', 'submit_form': 'Sign+in' }
	# Create a session object to snag cookies and authenticate.
	try:
		login = session.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, allow_redirects=False)
		#login = session.post('https://'+host+'/signin?redirect=http://imgur.com/', data=pdata, headers=headers, proxies=prx, verify=False, allow_redirects=False)
	except:
		print 'Some shit be bad.'
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
	for comment in commid:
		#dv = session.post('http://'+host+'/gallery/action/vote/'+comment, data=pdata, proxies=prx)
		dv = session.post('http://'+host+'/gallery/action/vote/'+comment, data=pdata)
		print "Submitted for..."
		print comment
		print dv.elapsed

print "Logging in..."
login(args.source)
print "Logged in."
get_all_comments(args.target)
print "Comments fetched. Now %svoting..." % args.action
vote(cmnts, args.action, 'caption')
