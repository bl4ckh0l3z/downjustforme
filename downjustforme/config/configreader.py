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

import logging
import configparser
from utils.utils import Utils

class ConfigReader():

    CONFIG_FILE = './downjustforme/config/downjustforme.cfg'

    @staticmethod
    def run():
        config = configparser.ConfigParser()
        config.read(ConfigReader.CONFIG_FILE)
        cfg = dict()
        
        if not config.has_option('DownJustForMe', 'dir_in') or \
                not config.has_option('DownJustForMe', 'dir_out') or \
                not config.has_option('DownJustForMe', 'dir_archive') or \
                (not config.has_option('DownJustForMe', 'urls_to_check') and \
                        not config.has_option('DownJustForMe', 'keywords_to_check') and \
                        not config.has_option('DownJustForMe', 'fails_count') and \
                        not config.has_option('DownJustForMe', 'check_frequency') and \
                        not config.has_option('DownJustForMe', 'bandwidth_avail_factor') and \
                        not config.has_option('DownJustForMe', 'serial_file')):
            print("\n### ERROR ### Config element are not defined in the config file\n")
            exit()
        else:
            ### parse the config file
            logging.debug("Loading config from '%s'" % (ConfigReader.CONFIG_FILE))

            ### parse dir_in config
            cfg['dir_in'] = config.get('DownJustForMe', 'dir_in')
            logging.debug("Setting '%s' as input dir" % (cfg['dir_in']))

            ### parse dir_out config
            cfg['dir_out'] = config.get('DownJustForMe', 'dir_out')
            logging.debug("Setting '%s' as output dir" % (cfg['dir_out']))

            ### parse dir_archive config
            cfg['dir_archive'] = config.get('DownJustForMe', 'dir_archive')
            logging.debug("Setting '%s' as archive dir" % (cfg['dir_archive']))

            ### parse urls to check
            if config.has_option('DownJustForMe', 'urls_to_check'):
                cfg['urls_to_check'] = config.get('DownJustForMe', 'urls_to_check').split(',')
                logging.debug("Setting '%s' as urls to check" % (cfg['urls_to_check']))
            else:
                logging.debug("URLs to check are not defined")

            ### parse keywords to check
            if config.has_option('DownJustForMe', 'keywords_to_check'):
                cfg['keywords_to_check'] = config.get('DownJustForMe', 'keywords_to_check').split(',')
                logging.debug("Setting '%s' as keywords to check" % (cfg['keywords_to_check']))
            else:
                logging.debug("KEYWORDs to check are not defined")

            ### parse frequency of checks
            if config.has_option('DownJustForMe', 'check_frequency'):
                cfg['check_frequency'] = int(config.get('DownJustForMe', 'check_frequency'))
                logging.debug("Setting '%s' as frequency of checks" % (cfg['check_frequency']))
            else:
                logging.debug("Frequency of checks is not defined")

            ### parse the factor used to computer the tollerable variatio of bandwidth availability
            if config.has_option('DownJustForMe', 'bandwidth_avail_factor'):
                cfg['bandwidth_avail_factor'] = float(config.get('DownJustForMe', 'bandwidth_avail_factor'))
                logging.debug("Setting '%s' as bandwidth availability factor" % (cfg['bandwidth_avail_factor']))
            else:
                logging.debug("Bandwidth availability factor is not defined")

            ### parse fails count number
            if config.has_option('DownJustForMe', 'fails_count'):
                cfg['fails_count'] = int(config.get('DownJustForMe', 'fails_count'))
                logging.debug("Setting '%s' as fails count number" % (cfg['fails_count']))
            else:
                logging.debug("Fails count number is not defined")

            ### parse proxy config
            if config.has_option('DownJustForMe', 'proxy'):
                cfg['proxy'] = config.get('DownJustForMe', 'proxy')
                logging.debug("Setting '%s' as proxy" % (cfg['proxy']))
            else:
                logging.debug("Proxy is not defined")

            ### parse smtp config
            if config.has_option('DownJustForMe', 'smtp_server'):
                cfg['smtp_server'] = config.get('DownJustForMe', 'smtp_server')
                logging.debug("Setting '%s' as smtp_server" % (cfg['smtp_server']))
            else:
                logging.debug("SMTP server is not defined")

            if config.has_option('DownJustForMe', 'smtp_port'):
                cfg['smtp_port'] = int(config.get('DownJustForMe', 'smtp_port'))
                logging.debug("Setting '%s' as smtp_port" % (cfg['smtp_port']))
            else:
                logging.debug("SMTP port is not defined")

            if config.has_option('DownJustForMe', 'smtp_username'):
                cfg['smtp_username'] = config.get('DownJustForMe', 'smtp_username')
                logging.debug("Setting '%s' as smtp_username" % (cfg['smtp_username']))
            else:
                logging.debug("SMTP username is not defined")

            if config.has_option('DownJustForMe', 'smtp_password'):
                cfg['smtp_password'] = config.get('DownJustForMe', 'smtp_password')
                logging.debug("Setting '%s' as smtp_password" % (cfg['smtp_password']))
            else:
                logging.debug("SMTP password is not defined")

            if config.has_option('DownJustForMe', 'smtp_from'):
                cfg['smtp_from'] = config.get('DownJustForMe', 'smtp_from')
                logging.debug("Setting '%s' as smtp_from" % (cfg['smtp_from']))
            else:
                logging.debug("SMTP from-field is not defined")

            if config.has_option('DownJustForMe', 'smtp_to'):
                cfg['smtp_to'] = config.get('DownJustForMe', 'smtp_to').split(',')
                logging.debug("Setting '%s' as smtp_to" % (cfg['smtp_to']))
            else:
                logging.debug("SMTP to-field is not defined")

            if config.has_option('DownJustForMe', 'smtp_cc'):
                cfg['smtp_cc'] = config.get('DownJustForMe', 'smtp_cc').split(',')
                logging.debug("Setting '%s' as smtp_cc" % (cfg['smtp_cc']))
            else:
                logging.debug("SMTP cc-field is not defined")

            if config.has_option('DownJustForMe', 'smtp_bcc'):
                cfg['smtp_bcc'] = config.get('DownJustForMe', 'smtp_bcc').split(',')
                logging.debug("Setting '%s' as smtp_bcc" % (cfg['smtp_bcc']))
            else:
                logging.debug("SMTP bcc-field is not defined")

            if config.has_option('DownJustForMe', 'smtp_subject'):
                cfg['smtp_subject'] = config.get('DownJustForMe', 'smtp_subject')
                logging.debug("Setting '%s' as smtp_subject" % (cfg['smtp_subject']))
            else:
                logging.debug("SMTP subject is not defined")

            if config.has_option('DownJustForMe', 'smtp_body'):
                cfg['smtp_body'] = config.get('DownJustForMe', 'smtp_body')
                logging.debug("Setting '%s' as smtp_body" % (cfg['smtp_body']))
            else:
                logging.debug("SMTP body is not defined")

            ### parse user agent config
            if config.has_option('DownJustForMe', 'user_agent'):
                cfg['user_agent'] = config.get('DownJustForMe', 'user_agent')
                logging.debug("Setting '%s' as user_agent" % (cfg['user_agent']))
            else:
                logging.debug("User Agent is not defined")

            ### parse serial_file config
            if config.has_option('DownJustForMe', 'serial_file'):
                cfg['serial_file'] = config.get('DownJustForMe', 'serial_file')
                logging.debug("Setting '%s' as serial_file" % (cfg['serial_file']))
            else:
                logging.debug("The file for data serialization is not defined")

            logging.debug("######## done")
        return cfg