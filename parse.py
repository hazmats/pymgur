#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(description='Do some imgr')
megroup = parser.add_mutually_exclusive_group()
megroup.add_argument('source', help='Source username from which to submit votes.')
megroup.add_argument('-l', '--logins', help='File containing login credentials for source accounts')
parser.add_argument('target', help='Target username')
parser.add_argument('action', help='Accepts up, down, or veto.')

args = parser.parse_args()

print "Targeting %s with %s votes from account %s" % (args.target, args.action, args.source)
