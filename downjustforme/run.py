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
import sys
import time
import getopt
import logging
from pyvirtualdisplay import Display
from config.configreader import ConfigReader
from dependencies.checkdependencies import CheckDependencies
from persistence.jsonadapter import JSONAdapter
from checker.alivechecker import AliveChecker
from evaluate.evaluator import Evaluator
from notification.emailnotifiers import EmailNotifiers
from utils.utils import Utils

class Core:

    def __init__(self, emailnotifiers, is_check_tcp, is_check_http, is_check_keywords, is_check_bandwidth):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))

        self._emailnotifiers = emailnotifiers
        self._is_check_tcp = is_check_tcp
        self._is_check_http = is_check_http
        self._is_check_keywords = is_check_keywords
        self._is_check_bandwidth = is_check_bandwidth

        check_passed = CheckDependencies.run()
        if not check_passed:
            exit()
        else:
            self._cfg = ConfigReader.run()
            self._evaluator = Evaluator(self._cfg, self._is_check_tcp, self._is_check_http, self._is_check_keywords, self._is_check_bandwidth)
            JSONAdapter.config = self._cfg
            if self._emailnotifiers:
                EmailNotifiers.config = self._cfg

    def run(self):
        print("Running...")

        os.system('ls -i -t ' + self._cfg['dir_archive'] +'/* | cut -d\' \' -f2 | tail -n+1 | xargs rm -f')

        data_old = JSONAdapter.load(self._cfg['dir_in'], self._cfg['serial_file'])

        if data_old is not None:
            data_file_name_new = data_old[0] + '_' + self._cfg['serial_file']
            Utils.rename_file(self._cfg['dir_in'], self._cfg['dir_archive'], \
                              self._cfg['serial_file'], data_file_name_new)
        else:
            data_old = []

        if Utils.is_internet_up() is True:
            urls = self._cfg['urls_to_check']
            data_new = []
            data_new.insert(0, Utils.timestamp_to_string(time.time()))
            thread_id = 0
            threads = []
            display = Display(visible=0, size=(1024, 768))
            display.start()
            for url in urls:
                thread_id += 1
                alivechecker_thread = AliveChecker(thread_id, self._cfg, url)
                threads.append(alivechecker_thread)
                alivechecker_thread.start()

            # Waiting for all threads to complete
            for thread in threads:
                thread.join()
            display.stop()

            for thread in threads:
                data_new.append(thread.data)
                logging.debug('%s\n' % (thread.log))
                thread.browser.quit()

            if len(data_new) > 0:
                JSONAdapter.save(data_new, self._cfg['dir_in'], self._cfg['serial_file'])

                data_all = []
                if len(data_old) > 0:
                    data_all.append(data_old)
                data_all.append(data_new)
                JSONAdapter.save(data_all, self._cfg['dir_out'], self._cfg['serial_file'])

                state = self._evaluator.run(data_all)
                logging.debug('Final state: %s' % (state))

                if self._emailnotifiers and state != '':
                    EmailNotifiers.notify(state)
            else:
                logging.debug('Empty data')
        else:
            logging.error('Internet is definitely down!')
            sys.exit(2)

        print("Done...")

def usage():
    print "\nThis is the usage function\n"
    print 'Usage: ./run_downjustforme.sh [options]'
    print '\n-h Show this help'
    print '-t Check TCP'
    print '-p Check HTTP'
    print '-k Check Keywords'
    print '-b Check Bandwidth'
    print '-e Send the results by email'
    print '\nDefault ./run_downjustforme.sh -t -p -k -b\n'

def options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hetpkb", ["help", "Email", "TCP", "HTTP", "Keywords", "Bandwidth"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    emailnotifiers = False
    is_check_tcp = True
    is_check_http = True
    is_check_keywords = True
    is_check_bandwidth = True
    is_first = True
    for o, a in opts:
        if (o in ("-t", "--tcp") or o in ("-p", "--http") or o in ("-b", "--bandwidth") or o in ("-k", "--keywords")) and is_first == True:
            is_first = False
            is_check_tcp = False
            is_check_http = False
            is_check_keywords = False
            is_check_bandwidth = False

        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--email"):
            emailnotifiers = True
        elif o in ("-t", "--tcp"):
            is_check_tcp = True
        elif o in ("-p", "--http"):
            is_check_http = True
        elif o in ("-k", "--keywords"):
            is_check_keywords = True
        elif o in ("-b", "--bandwidth"):
            is_check_bandwidth = True
        else:
            assert False, "Unhandled option"
    return emailnotifiers, is_check_tcp, is_check_http, is_check_keywords, is_check_bandwidth

def main():
    emailnotifiers, is_check_tcp, is_check_http, is_check_keywords, is_check_bandwidth = options()
    log_file = './logs/downjustforme.log'
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d-%m-%Y %H:%M')
    logging.debug("Setting '%s' as log file" % (log_file))

    logging.debug('######################################')
    logging.debug('#####   Starting DownJustForMe   #####')
    logging.debug('######################################')
    core = Core(emailnotifiers, is_check_tcp, is_check_http, is_check_keywords, is_check_bandwidth)
    core.run()

if __name__ == "__main__":
    main()
