import time, sys

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


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
		
		
		