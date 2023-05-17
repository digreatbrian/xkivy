
from setuptools import setup
import re

r_sub=re.sub

def re_sub(pattern, repl, string, count=0 ,flags=0):
	#creating this function as re.sub to avoid setup error/bytes-like or string needed when calling old re.sub
	string=str(string)
	return r_sub(pattern,repl,string,count,flags)
	

#setting re.sub to our custom function to fix string to String type if in another format
re.sub=re_sub

if __name__ == '__main__':
    setup()
