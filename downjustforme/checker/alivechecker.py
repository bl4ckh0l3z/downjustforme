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

import time
import logging
import urllib
import threading
from selenium import webdriver
from utils.utils import Utils
from socket import socket

class AliveChecker(threading.Thread):

    def __init__(self, thread_id, config, url):
        logging.debug("Instantiating the thread '%s' for the class '%s'" % (thread_id, self.__class__.__name__))
        self._cfg = config
        self._url = url
        self._thread_id = thread_id
        self.data = None
        self.display = None
        threading.Thread.__init__(self)

    def run(self):
        logging.debug("Thread '%s' is checking if the host '%s' is alive..." % (self._thread_id, self._url))
        browser = webdriver.Firefox()
        self.data = self._check_status(browser, self._url)
        browser.quit()
        return self.data

    def _check_status(self, browser, url):
        #logging.debug("Checking '%s'" % (url))
        data = dict()
        checks = []
        i = 1
        for i in range(1, self._cfg['fails_count']+1):
            #logging.debug('Check #%s' % (str(i)))
            check = dict()
            check['time_start'] = time.time()

            if 'http://' not in url and 'https://' not in url:
                url = 'http://' + url

            check['status_code_tcp'] = self._check_tcp(self._cfg['dir_in'], self._cfg['user_agent'], url)
            check['status_code_http'] = self._check_http(self._cfg['dir_in'], self._cfg['user_agent'], url)
            check['status_code_keywords'] = self._check_keywords(browser, self._cfg['dir_in'], self._cfg['user_agent'], url)

            check['time_end'] = time.time()
            check['time_elapsed'] = (check['time_end']-check['time_start'])/60
            #logging.debug('Elapsed: %s' % (str(check['time_elapsed'])))
            checks.append(check)
            i += 1
            time.sleep(self._cfg['check_frequency'])
        data[url] = checks
        return data

    def _check_tcp(self, proxy, user_agent, url):
        status_code = 'fails'
        port = 80
        if 'https' in url:
            port = 443
        cpos = url.find(':')
        host = Utils.extract_domain(url)
        try:
            sock = socket()
            sock.connect((host[cpos+3:], port))
            sock.close
            #logging.debug('Testing TCP --> ok')
            status_code = 'ok'
            return status_code
        except:
            logging.debug('Testing TCP --> fails')
            return status_code

    def _check_http(self, proxy, user_agent, url):
        status_code = ''
        try:
            response = urllib.urlopen(url)
            status_code = response.getcode()
            #logging.debug('Testing HTTP --> %s' % (str(status_code)))
            return status_code
        except:
            logging.debug('Testing HTTP --> %s' % (str(status_code)))
            return status_code

    def _check_keywords(self, browser, proxy, user_agent, url):
        status_code = 'fails'
        is_keywords = False
        try:
            browser.get(url)
            current_url = browser.current_url
            page = browser.page_source.encode('ascii', 'ignore').lower()

            if current_url != url:
                #logging.debug("'%s' redirects to '%s'" % (url, current_url))
                self._check_keywords(browser, proxy, user_agent, current_url)
            else:
                for keyword in self._cfg['keywords_to_check']:
                    if str(keyword) in str(page):
                        is_keywords = True
                        #logging.debug("found keyword: '%s'" % (keyword))
              
                if is_keywords:
                    #logging.debug('Testing KEYWORDS --> ok')
                    status_code = 'ok'
                else:
                    #logging.debug('Testing KEYWORDS --> fails')
                    status_code = 'fails'
            return status_code
        except:
            logging.debug('Testing KEYWORDS --> fails')
            return status_code
