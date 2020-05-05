#!/usr/bin/env python
#
#    weewx --- A simple, high-performance weather station server
#
#    Copyright (c) 2009-2020 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Customized setup file for weewx.

For more debug information, set the environment variable DISTUTILS_DEBUG
before running.

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import with_statement

import fnmatch
import os.path
import shutil
import subprocess
import sys
from distutils import log
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.core import setup
from distutils.debug import DEBUG

VERSION = "4.0.0"

if sys.version_info < (2, 7):
    log.fatal('WeeWX requires Python V2.7 or greater.')
    log.fatal('For earlier versions of Python, use WeeWX V3.9.')
    sys.exit("Python version unsupported.")

this_file = os.path.join(os.getcwd(), __file__)
this_dir = os.path.abspath(os.path.dirname(this_file))


# ==============================================================================
# utilities
# ==============================================================================
def find_files(directory, prefix="weewx", file_excludes=['*.pyc', "junk*"], dir_excludes=['*/__pycache__']):
    """Find all files under a directory, honoring some exclusions.

    Returns:
        A list of two-way tuples (directory_path, file_list), where file_list is a list
        of relative file paths.
    """
    # First recursively create a list of all the directories
    dir_list = []
    for dirpath, _, _ in os.walk(directory):
        # Make sure the directory name doesn't match the excluded pattern
        if not any(fnmatch.fnmatch(dirpath, d) for d in dir_excludes):
            dir_list.append(dirpath)

    data_files = []
    # Now search each directory for all files
    for d_path in dir_list:
        file_list = []
        # Find all the files in this directory
        for fn in os.listdir(d_path):
            filepath = os.path.join(d_path, fn)
            # Make sure it's a file, and that it's name doesn't match the excluded pattern
            if os.path.isfile(filepath) \
                    and not any(fnmatch.fnmatch(filepath, f) for f in file_excludes):
                file_list.append(filepath)
        # Add the directory and the list of files in it, to the list of all files.
        data_files.append((os.path.join(prefix, d_path), file_list))
    print(data_files)
    return data_files


# ==============================================================================
# main entry point
# ==============================================================================

if __name__ == "__main__":
    setup(name='weewx',
          version=VERSION,
          description='The WeeWX weather software system',
          long_description="WeeWX interacts with a weather station to produce graphs, reports, "
                           "and HTML pages.  WeeWX can upload data to services such as the "
                           "WeatherUnderground, PWSweather.com, or CWOP.",
          author='Tom Keffer',
          author_email='tkeffer@gmail.com',
          url='http://www.weewx.com',
          license='GPLv3',
          py_modules=['daemon'],
          package_dir={'': 'bin'},
          packages=['schemas',
                    'user',
                    'weecfg',
                    'weedb',
                    'weeimport',
                    'weeplot',
                    'weeutil',
                    'weewx',
                    'weewx.drivers'],
          scripts=['bin/wee_config',
                   'bin/wee_database',
                   'bin/wee_debug',
                   'bin/wee_device',
                   'bin/wee_extension',
                   'bin/wee_import',
                   'bin/wee_reports',
                   'bin/weewxd',
                   'bin/wunderfixer'],
          data_files=[('weewx', ['LICENSE.txt', 'README.md', 'weewx.conf']), ]
                      + find_files('docs')
                      + find_files('examples')
                      + find_files('skins')
                      + find_files('util'),
          )
