#!/usr/bin/env python3

"""This program is used to format a banner message with a surrounding border"""

import sys

def banner(message, border='-'):
	"""Input:  A message for the banner and *optionally a character for the border.  
	* If no border character is specified, it will use the default '-'
	
	Output:  
	-------
	message
	-------"""
	maxlinelen(message)
	line_len = maxlinelen(message) / len(border)
	line = int(line_len) * border
	print(line)
	print(message)
	print(line)
	
def maxlinelen(lines):
	ls = lines.split("\n")
	linelen = 0
	for l in ls:
		if len(l) > linelen:
			linelen = len(l)
	return(linelen)
		
testmsg = "Hi There Hi There! Nice to see you John"
		
if __name__ == '__main__':
	try:
		banner(sys.argv[1],sys.argv[2])
	except:
		try:
			banner(sys.argv[1])
		except:
			banner(testmsg)
