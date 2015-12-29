"""
default settings for programs;
all custom vars should be capital;
all could be cover by command line args and configure files;
"""

import os

import datetime

CONFIG_FOLDER = os.path.join(os.path.curdir,'config')

# RESULT_FOLDER = os.path.join(os.path.curdir,'results')

RMI_LOG = '/home/coremail/logs/rmi_api.log'
WMS_LOG = '/home/coremail/logs/wmsvr.log'

FUZZY_MATCH = {

}


#################
CONFIG = os.path.join(os.getcwd(), 'conf', 'rmi_exceptions.cf')
YESTERDAY = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
# LOG = '/home/coremail/logs/rmi_api.log.{0}'.format(YESTERDAY)
LOG = '/home/coremail/logs/rmi_api.log'
RESULT_FOLDER = os.path.join(os.getcwd(), 'results')
OMIT = os.path.join(RESULT_FOLDER, 'rmi_api.omit')
TABULATE = os.path.join(RESULT_FOLDER, 'rmi_api_error.tabulate')



print dir()