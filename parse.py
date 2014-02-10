#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(description='Do some imgr')
megroup = parser.add_mutually_exclusive_group()
parser.add_argument('source', help='Source username from which to submit votes.')
parser.add_argument('-l', '--logins', help='File containing login credentials for source accounts')
parser.add_argument('target', help='Target username')
parser.add_argument('action', help='Accepts up, down, or veto.')
parser.add_argument('type', help='Accepts "image" or "caption"', default="caption")

args = parser.parse_args()

if not args.type:
	print "ERRRRRRR"
	exit(2)

print "Targeting %s's %ss with %s votes from account %s" % (args.target, args.type, args.action, args.source)
