#!/usr/bin/python

"""
py2app/py2exe build script
Will automatically ensure all build prereqs are avail via ez_setup

Usage: (Mac OS X):
	python setup.py py2app

Usage: (Windows)
	python setup.py py2exe
"""

import os
import time
import sys
import shutil
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

def clean():
	try:
		shutil.rmtree('dist')
		shutil.rmtree('build')
	except:
		print OSError

print "Cleaning build directories...."
clean()

DATA_FILES=[]
for files in os.listdir('icons/'):
    f1 = 'icons/' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'icons', [f1]
        DATA_FILES.append(f2)

APP = ['Launcher.py']
APP_NAME='MacWxPythonApp'
if sys.platform == "darwin":
    print "Building for Mac OS X"
    time.sleep(3)
    OPTIONS = {
	   'iconfile':'icons/elephant_256_Bfn_icon.icns',
    	'plist': {
    		'CFBundleName': 'MacWxPythonApp',
    		'CFBundleShortVersionString': '1.0.0',
    		'CFBundleVersion': '1.0.0',
    	}
    }

    setup(
    	app=APP,
    	data_files=DATA_FILES,
    	name=APP_NAME,
    	options={'py2app': OPTIONS},
    	setup_requires=["py2app"],
    )

elif sys.platform == "win32":
    print "Building for Windows"
    time.sleep(3)
    OPTIONS = {
        'iconfile':'icons/elephant_256_Bfn_icon.ico',
    }
    
    setup(
        app=APP,
        data_files=DATA_FILES,
        name=APP_NAME,
        options={'py2exe':OPTIONS},
        setup_requires=["py2exe"],
    )

else:
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=[APP],
     )