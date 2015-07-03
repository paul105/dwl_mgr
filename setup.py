from setuptools import setup
import py2exe
import PyQt4
setup(windows=["main.py"], options={"py2exe": {
         "includes": ["sip", "PyQt4"]}})