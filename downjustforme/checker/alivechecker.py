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
import urllib2
import threading
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from utils.utils import Utils
from socket import socket

class AliveChecker(threading.Thread):

    def __init__(self, thread_id, config, url):
        logging.debug("Instantiating the thread '%s' for the class '%s'" % (thread_id, self.__class__.__name__))
        self._cfg = config
        self._url = url
        self._thread_id = thread_id
        self.data = None
        self.log = None
        self.browser = webdriver.Firefox()
        LOGGER.setLevel(logging.WARNING)
        threading.Thread.__init__(self)

    def run(self):
        logging.debug("Thread '%s' is checking if the host '%s' is alive..." % (self._thread_id, self._url))
        #browser = webdriver.Firefox()
        self.data = self._check_status(self.browser, self._url)
        #browser.quit()
        return self.data, self.log

    def _check_status(self, browser, url):
        self.log = "Checking '%s'\n" % (url)
        data = dict()
        checks = []
        i = 1
        for i in range(1, self._cfg['fails_count']+1):
            self.log += 'Check #%s\n' % (str(i))
            check = dict()
            check['time_start'] = time.time()

            if 'http://' not in url and 'https://' not in url:
                url = 'http://' + url

            check['status_code_tcp'] = self._check_tcp(self._cfg['dir_in'], self._cfg['user_agent'], url)
            check['status_code_http'] = self._check_http(self._cfg['dir_in'], self._cfg['user_agent'], url)
            check['status_code_keywords'] = self._check_keywords(browser, self._cfg['dir_in'], self._cfg['user_agent'], url)

            check['time_end'] = time.time()
            check['time_elapsed'] = (check['time_end']-check['time_start'])/60

            self.log += 'Elapsed: %s\n' % (str(check['time_elapsed']))
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
            sock.settimeout(self._cfg['time_out_sec'])
            sock.connect((host[cpos+3:], port))
            sock.close
            self.log += 'Testing TCP --> ok\n'
            status_code = 'ok'
            return status_code
        except:
            self.log += 'Testing TCP --> fails\n'
            return status_code

    def _check_http(self, proxy, user_agent, url):
        status_code = 0
        try:
            response = urllib2.urlopen(url, timeout=self._cfg['time_out_sec'])
            status_code = response.getcode()
            self.log += 'Testing HTTP --> %s\n' % (str(status_code))
            return status_code
        except:
            self.log += 'Testing HTTP --> %s\n' % (str(status_code))
            return status_code

    def _check_keywords(self, browser, proxy, user_agent, url):
        status_code = 'fails'
        is_keywords = False
        try:
            browser.set_page_load_timeout(self._cfg['time_out_sec'])
            browser.get(url)
            current_url = browser.current_url
            page = browser.page_source.encode('ascii', 'ignore').lower()

            if current_url != url:
                self.log += "'%s' redirects to '%s'\n" % (url, current_url)
                return self._check_keywords(browser, proxy, user_agent, current_url)
            else:
                for keyword in self._cfg['keywords_to_check']:
                    if str(keyword) in str(page):
                        is_keywords = True
                        self.log += "found keyword: '%s'\n" % (keyword)
              
                if is_keywords:
                    self.log += 'Testing KEYWORDS --> ok\n'
                    status_code = 'ok'
                else:
                    self.log += 'Testing KEYWORDS --> fails\n'
                    status_code = 'fails'
            return status_code
        except:
            self.log += 'Testing KEYWORDS --> fails\n'
            return status_code
