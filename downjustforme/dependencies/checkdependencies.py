# This file is part of DownJustForMe.
#
# bl4ckh0l3 <bl4ckh0l3z at gmail.com>
#
# DownJustForMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# DownJustForMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DownJustForMe. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = 'bl4ckh0l3z'
__license__ = 'GPL v2'
__maintainer__ = 'bl4ckh0l3z'
__email__ = 'bl4ckh0l3z@gmail.com'

import os
import sys
import logging
import subprocess
import configparser

class CheckDependencies():

    DEPENDENCIES_FILE = './downjustforme/dependencies/dependencies.cfg'

    @staticmethod
    def run():
        config = configparser.ConfigParser()
        config.read(CheckDependencies.DEPENDENCIES_FILE)

        check_passed = None
        logging.debug("Check dependencies...")
        print("Check dependencies...")
        if not CheckDependencies._python_version_check(config) or \
                not CheckDependencies._python_modules_check(config):
            check_passed = False
            logging.error("Check dependencies failed")
            print("Check dependencies failed")
        else:
            check_passed = True
            logging.info("Check dependencies passed")
            print("Check dependencies passed")
        return check_passed

    # Python version check (anyway there is dedicated virtualenv)
    @staticmethod
    def _python_version_check(config):
        exit_status = None
        if not config.has_option('DownJustForMe', 'python_version_major') \
                or not config.has_option('DownJustForMe', 'python_version_minor'):
            logging.error("No config values for 'python_version_major' and/or 'python_version_minor'")
            exit_status = False
        else:
            py_major, py_minor = sys.version_info[:2]
            py_version = sys.version.split()[0]
            if py_major != int(config.get('DownJustForMe', 'python_version_major')) and \
                    py_minor != int(config.get('DownJustForMe', 'python_version_minor')):
                logging.error("You are using python %s, but version 2.7 is required" % (py_version))
                exit_status = False
            else:
                exit_status = True
        return exit_status

    # Python modules check (anyway there is dedicated virtualenv)
    @staticmethod
    def _python_modules_check(config):
        exit_status = 0
        if not config.has_option('DownJustForMe', 'python_modules'):
            logging.error("No config value for 'python_modules'")
            exit_status = 1
        else:
            modules = config.get('DownJustForMe', 'python_modules').split(',')
            for module in modules:
                try:
                    __import__(module)
                except ImportError:
                    logging.error("No module '%s'" % (module))
                    exit_status += 1
        if exit_status > 0:
            exit_status = False
        else:
            exit_status = True
        return exit_status