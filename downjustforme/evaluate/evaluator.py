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
import datetime
from utils.utils import Utils

class Evaluator():

    def __init__(self, config, is_check_tcp, is_check_http, is_check_keywords, is_check_bandwidth):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._cfg = config
        self._is_check_tcp = is_check_tcp
        self._is_check_http = is_check_http
        self._is_check_keywords = is_check_keywords
        self._is_check_bandwidth = is_check_bandwidth

    def run(self, data):
        logging.debug("Merging the availability indicators of the web-sites...")
        merged_data = self._merge(data)

        logging.debug("Evaluating the availability of the web-sites...")
        state = self._evaluate(merged_data)
        return state

    def _merge(self, data):
        merged_data = dict()
        for d in data:
            timestamp = str(d[0])
            for e in d[1:]:
                for s in e:
                    checks = e[s]
                    if s not in merged_data.keys():
                        merged_data[s] = dict()
                        (merged_data[s])['status_code_tcp'] = dict()
                        (merged_data[s])['status_code_http'] = dict()
                        (merged_data[s])['status_code_keywords'] = dict()
                        (merged_data[s])['time_elapsed'] = dict()

                    ((merged_data[s])['status_code_tcp'])[timestamp] = []
                    ((merged_data[s])['status_code_http'])[timestamp] = []
                    ((merged_data[s])['status_code_keywords'])[timestamp] = []
                    ((merged_data[s])['time_elapsed'])[timestamp] = []
                    for c in checks:
                        (((merged_data[s])['status_code_tcp'])[timestamp]).append(str(c['status_code_tcp']))
                        (((merged_data[s])['status_code_http'])[timestamp]).append(c['status_code_http'])
                        (((merged_data[s])['status_code_keywords'])[timestamp]).append(str(c['status_code_keywords']))
                        (((merged_data[s])['time_elapsed'])[timestamp]).append(c['time_elapsed'])
        return merged_data

    def _evaluate(self, data):
        state = ''

        for d in data.keys():
            logging.debug('site: %s' % (d))
            key_list = sorted(((data[d])['status_code_tcp']).keys())

            tcp_check_1 = ((data[d])['status_code_tcp'])[key_list[0]]
            tcp_check_2 = None
            http_check_1 = ((data[d])['status_code_http'])[key_list[0]]
            http_check_2 = None
            keywords_check_1 = ((data[d])['status_code_keywords'])[key_list[0]]
            keywords_check_2 = None
            time_elapsed_check_1 = ((data[d])['time_elapsed'])[key_list[0]]
            time_elapsed_check_2 = None
            if len(key_list) > 1:
                tcp_check_2 = ((data[d])['status_code_tcp'])[key_list[1]]
                http_check_2 = ((data[d])['status_code_http'])[key_list[1]]
                keywords_check_2 = ((data[d])['status_code_keywords'])[key_list[1]]
                time_elapsed_check_2 = ((data[d])['time_elapsed'])[key_list[1]]

            tcp_changed = http_changed = keywords_changed = bandwidth_changed = False
            if self._is_check_tcp == True:
                tcp_changed, tcp_state = self._evaluate_tcp_availability(tcp_check_1, tcp_check_2)
            if self._is_check_http == True:
                http_changed, http_state = self._evaluate_http_availability(http_check_1, http_check_2)
            if self._is_check_keywords == True:
                keywords_changed, keywords_state = self._evaluate_keywords_availability(keywords_check_1, keywords_check_2)
            if self._is_check_bandwidth == True:
                bandwidth_changed, bandwidth_state = self._evaluate_bandwidth_availability(time_elapsed_check_1, time_elapsed_check_2)

            if tcp_changed or http_changed or keywords_changed or bandwidth_changed:
                state += ' %s </br> ****************************************************************** </br> %s </br> %s </br> %s </br> %s </br> ****************************************************************** </br>' % (d, tcp_state, http_state, keywords_state, bandwidth_state)

        return state

    def _evaluate_tcp_availability(self, check_1, check_2):
        fails_num = 0
        state = ''
        changed = False

        state_1 = 'TCP availability --> ok'
        for c in check_1:
            if str(c) == 'fails':
                fails_num += 1
        if fails_num == len(check_1):
            state_1 = 'TCP availability --> fails'
        logging.debug('TCP check_1: %s' % (state_1))

        state = state_1
        if check_2 is not None:
            state_2 = 'TCP availability --> ok'
            fails_num = 0
            for c in check_2:
                if str(c) == 'fails':
                    fails_num += 1
            if fails_num == len(check_2):
                state_2 = 'TCP availability --> fails'

            logging.debug('TCP check_2: %s' % (state_2))

            if state_1 != state_2:
                state = state_2 + '   <b style="color: red;">(!!! NEW !!!)</b>'
                changed = True
            else:
                state = state_2
        logging.debug('TCP check_final: %s' % (state))
        return changed, state        

    def _evaluate_http_availability(self, check_1, check_2):
        fails_num = 0
        fails_code = ''
        state = ''
        changed = False

        state_1 = 'HTTP availability --> ok'
        for c in check_1:
            if c != 200:
                fails_num += 1
                fails_code += str(c) + ', '
        fails_code = fails_code[:-2]
        if fails_num == len(check_1):
            state_1 = 'HTTP availability --> fails [' + fails_code + ']'
        logging.debug('HTTP check_1: %s' % (state_1))

        state = state_1
        if check_2 is not None:
            state_2 = 'HTTP availability --> ok'
            fails_num = 0
            fails_code = ''
            for c in check_2:
                if c != 200:
                    fails_num += 1
                    fails_code += str(c) + ', '
            fails_code = fails_code[:-2]
            if fails_num == len(check_2):
                state_2 = 'HTTP availability --> fails [' + fails_code + ']'
       
            logging.debug('HTTP check_2: %s' % (state_2))

            if state_1 != state_2:
                state = state_2 + '   <b style="color: red;">(!!! NEW !!!)</b>'
                changed = True
            else:
                state = state_2
        logging.debug('HTTP check_final: %s' % (state))
        return changed, state

    def _evaluate_keywords_availability(self, check_1, check_2):
        fails_num = 0
        state = ''
        changed = False

        state_1 = 'KEYWORDS availability --> ok'
        for c in check_1:
            if str(c) == 'fails':
                fails_num += 1
        if fails_num == len(check_1):
            state_1 = 'KEYWORDS availability --> fails'
        logging.debug('KEYWORDS check_1: %s' % (state_1))

        state = state_1
        if check_2 is not None:
            state_2 = 'KEYWORDS availability --> ok'
            fails_num = 0
            for c in check_2:
                if str(c) == 'fails':
                    fails_num += 1
            if fails_num == len(check_2):
                state_2 = 'KEYWORDS availability --> fails'
       
            logging.debug('KEYWORDS check_2: %s' % (state_2))

            if state_1 != state_2:
                state = state_2 + '   <b style="color: red;">(!!! NEW !!!)</b>'
                changed = True
            else:
                state = state_2
        logging.debug('KEYWORDS check_final: %s' % (state))
        return changed, state

    def _evaluate_bandwidth_availability(self, check_1, check_2):
        state = ''
        changed = False

        wma_1 = Utils.compute_wma(check_1)
        logging.debug('BANDWIDTH wma_1: %s' % (wma_1))

        if check_2 is not None:
            wma_2 = Utils.compute_wma(check_2)
            logging.debug('BANDWIDTH wma_2: %s' % (wma_2))

            wma_diff = wma_2 - wma_1
            wma_diff_abs = abs(wma_diff)
            variation = round(float(wma_diff_abs/wma_1*100), 1)
            logging.debug('BANDWIDTH variation: %s' % (variation))

            if variation >= float(self._cfg['bandwidth_avail_factor']):
                variation_dim = 'accretion'
                if wma_diff > 0.0:
                    variation_dim = 'degradation'

                state = 'BANDWIDTH availability --> %s%% %s   <b style="color: red;">(!!! NEW !!!)</b>' % (variation, variation_dim)
                changed = True
            else:
                state = 'BANDWIDTH availability --> %s' % (wma_2)
        else:
            state = 'BANDWIDTH availability --> %s' % (wma_1)

        logging.debug('BANDWIDTH check_final: %s' % (state))
        return changed, state
