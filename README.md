#### wxpython-wizard

This is a basic wizard interface with several sample screens. It is designed as a publisher/subscriber MVC program. 

#####Platforms
* Mac OS X El Capitan
* Windows 2008 Server

#####Files

`Launcher.py` is the main controller

`GUI.py` holds the main gui panels

`PanelTracker.py` is a linked list implementation to track the current, previous and next panels

#####Building

To build, run `python setup.py py2app` (mac), `python setup.py py2app` (win)

Run by `python Launcher.py`

Application built using Eclipse for Mac, PyDev 4.5.3, Python 2.7.1 and wxPython 3.0.1

