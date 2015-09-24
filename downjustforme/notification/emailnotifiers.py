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
import logging
from smtplib import SMTP, SMTPException
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailNotifiers():

    config = ''

    @staticmethod
    def notify(state):
        logging.debug("EmailNotifier is notifying...")

        smtp_server = EmailNotifiers.config['smtp_server']
        smtp_port = EmailNotifiers.config['smtp_port']
        smtp_username = EmailNotifiers.config['smtp_username']
        smtp_password = EmailNotifiers.config['smtp_password']
        smtp_from = EmailNotifiers.config['smtp_from']
        smtp_to = EmailNotifiers.config['smtp_to']
        smtp_cc = None
        if 'smtp_cc' in EmailNotifiers.config.keys():
            smtp_cc = EmailNotifiers.config['smtp_cc']
        smtp_bcc = None
        if 'smtp_bcc' in EmailNotifiers.config.keys():
            smtp_bcc = EmailNotifiers.config['smtp_bcc']
        smtp_subject = EmailNotifiers.config['smtp_subject']
        smtp_body = EmailNotifiers.config['smtp_body']
        smtp_body = smtp_body.replace('XXX', '<p>' + state + '</p>')

        try:
            server = SMTP(smtp_server, smtp_port)
            server.set_debuglevel(False)

            msg = MIMEMultipart()
            msg['From'] = smtp_from
            msg['To'] = '; '.join(smtp_to)
            emails = [smtp_to]
            if smtp_cc is not None:
                msg['CC'] = '; '.join(smtp_cc)
                emails += smtp_cc
            if smtp_bcc is not None:
                msg['BCC'] = '; '.join(smtp_bcc)
                emails += smtp_bcc
            msg['Subject'] = smtp_subject

            body = MIMEText(smtp_body, 'html')
            msg.attach(body)

            logging.debug(msg.as_string())

            try:
                file = os.path.join(EmailNotifiers.config['dir_out'], EmailNotifiers.config['serial_file'])
                logging.debug("attaching file: '%s'" % (file))
                fp = open(file, 'rb')
                part = MIMEApplication(fp.read(), 'text/plain', filename=EmailNotifiers.config['serial_file'])
                part.add_header('Content-Disposition', 'attachment', filename=EmailNotifiers.config['serial_file'])
                msg.attach(part)
                fp.close()
            except OSError, e:
                logging.error("Error attaching file '%s': %s" % (file, e))
                raise OSError

            # identify ourselves, prompting server for supported features
            server.ehlo()

            # If we can encrypt this session, do it
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo() # re-identify ourselves over TLS connection

            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_from[0], emails, msg.as_string())
            logging.debug('Email sent...')
        except SMTPException, sme:
            logging.error("Error notifying results by email: %s" % (sme))
            raise OSError
        finally:
            server.quit()