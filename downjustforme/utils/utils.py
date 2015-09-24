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
import re
import logging
import shutil
import httplib
import datetime

class Utils():

    @staticmethod
    def timestamp_to_string(timestamp):
        st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')
        return st

    @staticmethod
    def is_internet_up():
        data = []
        urls = ['www.google.it', 'www.repubblica.it']
        is_up = False
        check_count = 3
        count = 0

        while count < check_count and is_up is False:
            logging.debug('Check internetUp, number: %s' % (count+1))
            try:
                for url in urls:
                    conn = httplib.HTTPConnection(url)
                    conn.request("HEAD", "/")
                    res = conn.getresponse()
                    data.append(res.status)
                    logging.debug('%s %s %s' % (res.status, res.reason, url))
                if data[0] != 200 and data[1] != 200:
                    is_up = False
                    logging.debug('Internet might be down!')
                else:
                    is_up = True
            except:
                is_up = False
                logging.debug('Internet might be down!')
            finally:
                count += 1
        return is_up

    @staticmethod
    def remove_dir_content(dir):
        try:
            for elem in os.listdir(dir):
                elem_path = os.path.join(dir, elem)
                if os.path.isdir(elem_path):
                    shutil.rmtree(elem_path)
                else:
                    if '.placeholder' not in elem:
                        Utils.remove_file(dir, elem)
        except OSError, e:
            logging.error("Error removing dir '%s' content: %s" % (dir, e))
            raise OSError

    @staticmethod
    def remove_file(path_in, file):
        try:
            os.remove(os.path.join(path_in, file).encode('utf-8').strip())
        except OSError, e:
            logging.error("Error removing file '%s': %s" % (os.path.join(path_in, file), e))
            raise OSError

    @staticmethod
    def rename_file(path_in, path_out, file_in, file_out):
        logging.debug("Renaming file '%s'" % (os.path.join(path_in, file_in)))
        try:
            os.rename(os.path.join(path_in, file_in).strip(),
                os.path.join(path_out, file_out).strip())
        except OSError, e:
            logging.error("Error renaming file '%s': %s" % (os.path.join(path_in, file_in), e))
            raise OSError

    @staticmethod
    def compute_file_number(dir):
        file_number = 0
        try:
            for item in os.listdir(dir):
                item_path = os.path.join(dir, item)
                if os.path.isfile(item_path):
                    file_number += 1
                elif os.path.isdir(item_path):
                    file_number += Utils.compute_file_number(item_path)
        except OSError, e:
            logging.error("Error computing file number in '%s': %s" % (dir, e))
            raise OSError
        return file_number

    @staticmethod
    def extract_domain(url):
        regexp_match = re.search('(http\:\/\/|https\:\/\/)?(www\.)?([a-zA-Z0-9\.\-_]*)', url)
        domain = 'null'
        if regexp_match:
            domain = regexp_match.group(0)
            if domain[-1] == '/':
                domain = domain[:-1]
        return domain

    @staticmethod
    def compute_wma(value_list):
        wma = 0.0
        index = 0.0
        sum = 0.0
        for v in value_list:
            index += 1.0
            wma += (float(v)*index)
            sum += index
        return round(float(wma/sum), 5)