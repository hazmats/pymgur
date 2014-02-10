#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(description='Do some imgr')
parser.add_argument('source', help='Source username from which to submit votes.')
parser.add_argument('target', help='Target username')
parser.add_argument('action', help='Accepts up, down, or veto.')

args = parser.parse_args()

print "Targeting %s with %s votes from account %s" % (args.target, args.action, args.source)
