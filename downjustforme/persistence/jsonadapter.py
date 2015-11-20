#coding:utf-8;
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

__author__ = 'bl4ckh0l3'
__license__ = 'GPL v2'
__maintainer__ = 'bl4ckh0l3'
__email__ = 'bl4ckh0l3z@gmail.com'

import os
import json
import logging

class JSONAdapter():

    config = ''

    @staticmethod
    def load(path, file_name):
        logging.debug("JSONAdapter is loading old data '%s'" % (file_name))
        if os.path.exists(os.path.join(path, file_name)):
            try:
                with open(os.path.join(path, file_name)) as file:
                    datas = json.load(file)
                return datas
            except OSError, e:
                logging.error("Error loading old data from json file: %s" % (e))
                raise OSError
        else:
            logging.debug("The file '%s' containing old data doesn't exist" % (os.path.join(path, file_name)))
            return None

    @staticmethod
    def save(data, path, file_name):
        logging.debug("JSONAdapter is storing new data '%s'" % (file_name))
        try:
            file = open(os.path.join(path, file_name), 'w')
            file.write(json.dumps(data, indent=4, encoding='utf-8'))
            file.close()
        except OSError, e:
            logging.error("Error saving new data from json file: %s" % (e))
            raise OSError
