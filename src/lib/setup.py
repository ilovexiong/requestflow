import os
from setuptools import setup
import re
import sys



MIN_PYTHON_VERSION = (2, 5)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'requestflow'))
from version import VERSION


if __name__=="__main__":
    if sys.version_info < MIN_PYTHON_VERSION:
        args = (NAME, VERSION, ".".join([str(x) for x in MIN_PYTHON_VERSION]))
        raise Exception, "%s-%s requires Python %s or higher." % args 
    setup(name="requestflow",
          version=VERSION,
          description="Tracking the id ",
          author="Hulu",
          author_email="the-core@hulu.com",
          packages=['requestflow'],
          install_requires=['python-json-logger==0.1.4'],
          classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'Programming Language :: Python',
              'Topic :: Software Development :: Libraries'])
