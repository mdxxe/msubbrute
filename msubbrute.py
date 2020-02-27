#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from modules import resolve
from modules import wildcard
from multiprocessing import Pool

import json

def loadfile_wordlist(filename):
	filename = open(filename,'r')
	wlist = filename.read().split('\n')
	filename.close
	return filter(None, wlist)

def check_subdomain(item):
	subdomain_target = item+'.'+target
	subdomain_resolve = json.loads(resolve.resolve(subdomain_target))
	if subdomain_resolve['hostname']:
		try:
			status_code = subdomain_resolve['http_response']['status']['code']
		except:
			status_code = ''

		if wildcard_json['enabled']:
			wildcard_code = wildcard_json['detected']['status_code']
			if str(status_code) != '' and str(wildcard_code) != '' and str(status_code) == str(wildcard_code):
				try:
					content_length = str(subdomain_resolve['http_response']['http_headers']['content-length'])
				except:
					content_length = ''
				try:
					wildcard_content_length = wildcard_json['http_response']['http_headers']['content-length']
				except:
					wildcard_content_length = ''
				if content_length == '0' or str(content_length) == str(wildcard_content_length):
					pass
				else:
					return(subdomain_resolve['target'])
			else:
				return(subdomain_resolve['target'])
		else:
			return(subdomain_resolve['target'])

def scan_multiprocessing(item):
	result = check_subdomain(item)
	if result != None:
		print(result)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', default='google.com', help='input file')
parser.add_argument('-i', '--inputfile', default='domains.txt', help='input file')
parser.add_argument('-o', '--outputfile', default='output.txt', help='output file')
parser.add_argument('-t', '--threads', default=40, help='threads')
args = parser.parse_args()

DOMAIN=args.domain
INPUTFILE=args.inputfile
MAXPROCESSES=int(args.threads)
OUTPUTFILE=args.outputfile

target = DOMAIN

subdomain_list = []
wildcard_json = json.loads(wildcard.test_wildcard(target))

word_list = loadfile_wordlist(INPUTFILE)
word_list = [item.lower() for item in word_list]
subdomain_list = subdomain_list + word_list
subdomain_list = list(set(subdomain_list))
subdomain_list = sorted(subdomain_list)
wordlist_count = len(subdomain_list)

subdomains_json_list = []

pool = Pool(processes=MAXPROCESSES)
pool.map(scan_multiprocessing, subdomain_list)
pool.close()
pool.join()
