#################################################################
# MET v2 Metadate Explorer Tool
#
# This Software is Open Source. See License: https://github.com/TERENA/met/blob/master/LICENSE.md
# Copyright (c) 2012, TERENA All rights reserved.
#
# This Software is based on MET v1 developed for TERENA by Yaco Sistemas, http://www.yaco.es/
# MET v2 was developed for TERENA by Tamim Ziai, DAASI International GmbH, http://www.daasi.de
# Current version of MET has been revised for performance improvements by Andrea Biancini,
# Consortium GARR, http://www.garr.it
##########################################################################

import json
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from django.template.defaultfilters import slugify
from slackclient import SlackClient

from saml2.mdstore import InMemoryMetaData

from local_settings import HOSTNAME, SAML2DIR


def compare_filecontents(a, b):
    if a is None:
        return b is None
    if b is None:
        return a is None

    md5_a = hashlib.md5(a).hexdigest()
    md5_b = hashlib.md5(b).hexdigest()
    return md5_a == md5_b


def custom_slugify(obj):
    return slugify(str(obj).replace("://", "_").replace("/", "_").replace(".", "_"))


def _connect_to_smtp(server, port=25, login_type=None, username=None, password=None):
    smtp_send = smtplib.SMTP(server, port)
    smtp_send.ehlo()

    if smtp_send.has_extn('STARTTLS'):
        smtp_send.starttls()
        smtp_send.ehlo()

    if username and password:
        try:
            if login_type:
                smtp_send.esmtp_features['auth'] = login_type
            smtp_send.login(username, password)
        except Exception as errorMessage:
            print('Error occurred while trying to login to the email server with user {}: {}'.format(
                username, errorMessage))
            raise

    return smtp_send


def send_slack(message):
    slack_config_dict = getattr(settings, 'SLACK_CONFIG')
    if slack_config_dict and 'token' in slack_config_dict and slack_config_dict['token']:
        slack_token = slack_config_dict['token']
        slack_channel = slack_config_dict['channel'] if 'channel' in slack_config_dict else '#devops'
        sc = SlackClient(token=slack_token)

        sc.api_call(
            'chat.postMessage',
            channel=slack_channel,
            text=message
        )


def send_mail(from_email_address, subject, message):
    mail_config_dict = getattr(settings, 'MAIL_CONFIG')
    server = mail_config_dict['email_server']

    if server is None:
        return

    smtp_send = _connect_to_smtp(
        server,
        mail_config_dict['email_server_port'],
        mail_config_dict['login_type'],
        mail_config_dict['username'],
        mail_config_dict['password']
    )

    try:
        message = MIMEText(message.encode('utf-8'), 'plain', _charset='UTF-8')
        message['From'] = from_email_address
        message['To'] = ",".join(mail_config_dict['to_email_address'])
        message['Subject'] = subject

        smtp_send.sendmail(
            from_email_address,
            mail_config_dict['to_email_address'],
            message.as_string()
        )
    except Exception as errorMessage:
        print('Error occurred while trying to send an email to %s: %s' %
              (mail_config_dict['to_email_address'], errorMessage))
        raise
    finally:
        if smtp_send:
            smtp_send.quit()


def process_xml_entity_fed_info(federation_info):
    processed_fed_info = []
    for fed in federation_info:
        new_fed = {
            'name': fed[0],
            'url': fed[1]
        }
        processed_fed_info.append(new_fed)
    return processed_fed_info


def get_full_path_url(absolute_url):
    return "%s%s" % (HOSTNAME, absolute_url)


def get_canonical(data):
    canonical = data.get('en', data.get('es', data.get('de')))
    if not canonical:
        try:
            canonical = list(data.values())[0]
        except IndexError:
            pass

    return canonical.strip()


class EdugainIdPsDatabaseMetadataLoader(InMemoryMetaData):

    def __init__(self, attrc, metadata='', node_name=None,
                 check_validity=True, security=None, **kwargs):

        super(EdugainIdPsDatabaseMetadataLoader, self).__init__(None, **kwargs)

        filename = os.path.join(SAML2DIR, 'edugain_parsedmetadata.json')
        with open(filename) as f:
            self.entity = json.load(f)

    def load(self, *args, **kwargs):
        pass

    def __getitem__(self, item):
        return self.entity[item]
