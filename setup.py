import os
from setuptools import setup,find_packages
import re

r_sub=re.sub

def re_sub(pattern, repl, string, count=0 ,flags=0):
	#creating this function as re.sub to avoid setup error/bytes-like or string needed when calling old re.sub
	string=str(string)
	return r_sub(pattern,repl,string,count,flags)
	

#setting re.sub to our custom function to fix string to String type if in another format
re.sub=re_sub

def get_version():
	version_file=os.path.join(os.path.abspath(os.path.dirname(__file__)),"xkivy", "version.py")
	with open(version_file,"r") as fd:
		r=fd.read()
		r=r.split('\n')
		for x in r:
			if x.startswith('version'):
				a,b=x.split('=')
				version=b
				return version

if __name__ == '__main__':
    setup(
        version=get_version(),
        packages=find_packages(
            include=["xkivy","xkivy.*"], exclude=["__pycache__"]
        ),
        package_dir={"xkivy": "xkivy"},
        setup_requires=["kivy>=2.0.0", "kivymd>=1.2.0.dev0" ],
        python_requires=">=3.7",
    )
