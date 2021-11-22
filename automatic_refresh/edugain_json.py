#!/usr/bin/env python

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
#########################################################################################

import dotenv
import os
import sys
import logging
import logging.config


dotenv.read_dotenv(os.environ.get('DOTENV_FILE', '/home/pitbulk/proyectos/met-private/.env'))

os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs/'

current_directory = os.path.join(os.path.dirname(__file__), '..')

sys.path.append(current_directory)
sys.path.append(os.path.join(current_directory, 'met'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'met.settings'

import django
from saml2.mdstore import InMemoryMetaData
from met.metadataparser.models import Entity
from local_settings import HOSTNAME, SAML2DIR
import json


django.setup()


class SingleRun(object):
    class InstanceRunningException(Exception):
        pass

    def __init__(self, lock_file):
        # define the lock file name
        self.lock_file = '/tmp/%s.pid' % lock_file

    def __call__(self, func):
        def fnc(*args, **kwargs):
            if os.path.exists(self.lock_file):
                # get process id, if lock file exists
                pid = open(self.lock_file, 'rt').read()
                if not os.path.exists('/proc/%s' % pid):
                    # if process is not alive remove the lock file
                    os.unlink(self.lock_file)
                else:
                    # process is running
                    raise self.InstanceRunningException(pid)

            try:
                # store process id
                open(self.lock_file, 'wt').write(str(os.getpid()))
                # execute wrapped function
                func(*args, **kwargs)
            finally:
                if os.path.exists(self.lock_file):
                    os.unlink(self.lock_file)
        return fnc


class GetEdugainJson(object):
    @classmethod
    def process(cls):
        metPar = InMemoryMetaData(None)
        entities = Entity.objects.filter(federations__slug="edugain", types__xmlname="IDPSSODescriptor")
        for entity in entities:
            try:
                metPar.parse(entity.xml)
            except:
                print("Error processing: %s" % entity.entityid)
        # Serializing json  
        json_object = json.dumps(metPar.entity)
        filename = os.path.join(SAML2DIR, 'edugain_parsedmetadata.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(metPar.entity, f, ensure_ascii=False)


@SingleRun(lock_file='met-edugainjs')
def commandline_call(convert_class=GetEdugainJson):
    obj_convert = convert_class()
    obj_convert.process()


if __name__ == '__main__':
    commandline_call()
