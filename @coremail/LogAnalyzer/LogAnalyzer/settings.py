"""
default settings for programs;
all custom vars should be capital;
all could be cover by command line args and configure files;
"""

import os

import datetime


# log file path
RMI_LOG = '/home/coremail/logs/rmi_api.log'
WMS_LOG = '/home/coremail/logs/wmsvr.log'

FILE = RMI_LOG   # default file is rmi_api.log


# config files folder
CONFIG_FOLDER = os.path.join(os.path.curdir,'config')


# config file names
RMI_EXCEPT = 'rmi_exceptions.cf'
WMS_EXCEPT = 'wms_exceptions.cf'

CONFIG = os.path.join(CONFIG_FOLDER, RMI_EXCEPT)    # default config is rmi_exceptions.cf


# results file folder
RESULT_FOLDER = os.path.join(os.getcwd(), 'results')


# omit file
SAVE_OMIT = False
OMIT_FILE = os.path.join(RESULT_FOLDER, 'exceptions.omit')


# tabulate file
SAVE_TABULATE = False
TABULATE_FILE = os.path.join(RESULT_FOLDER, 'error.tabulate')


# domain connect info
DOMAIN_CONNECT_INFO = False


# use regex to grep log?
USE_REGEX = False


# log time
YESTERDAY = False
TIME_PERIOD = None

