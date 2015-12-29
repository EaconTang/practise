"""
Input module
including:
    1. default settings from file <settings.py>
    2. command line args
    3. configuration from conf/*.conf
    4. log file streams
"""
from optparse import OptionParser
from Util import MyConfigParser
import setting


class BaseInput(object):
    def __init__(self):
        self._default_vars = []
        pass

    def default_setting(self):
        pass

    def parse_command_args(self):
        pass

    def read_conf_file(self, cf):
        pass

    def read_log_file(self, log):
        pass


class DefaultSetting(BaseInput):
    @property
    def default_setting(self):
        self._default_vars = dir(setting)
        self._default_vars = filter(lambda x: x == x.upper(), self._default_vars)
        return self._default_vars


class CommandArgs(BaseInput):
    @property
    def arg_parser(self):
        """
        give optional arguments while execute the program
        :return: a option parser
        """
        usage = "usage: python %prog [-h] [-f value] [-c value] [-t] [-T value] [-o] [-O value] [-y]"
        usage += " [-D]"
        usage += " [--datetime value]"
        parser = OptionParser(usage)

        parser.add_option('-f', '--file', dest='FILE',
                          help='specify a log file to be scan, defaults to today\'s rmi_api.log')
        parser.add_option('-c', '--config', dest='CONFIG',
                          help='specify a config file to be load,defaults to ~/LogMiner/conf/rmi_exceptions.cf')
        parser.add_option('-t', '--tabulate', dest='TABULATE_SAVE',
                          help='use this flag to save the results to the file,defaults to under "~/LogMiner/results"',
                          action='store_true', default=False)
        parser.add_option('-T', '--tabulate-file', dest='TABULATE',
                          help='specify a file to save the tabulate table,defaults to "rmi_api_error.tabulate"')
        parser.add_option('-o', '--omit', dest='OMIT_SAVE',
                          help='use this flag to save the omit info that were not classified.' +
                               'It would be saved under "~/LogMiner/results"',
                          action='store_true', default=False)
        parser.add_option('-O', '--omit-file', dest='OMIT',
                          help='specific a filename to save the omit info,defaults to "rmi_api.omit.{LogDate}"')
        parser.add_option('-y', '--yesterday-log', dest='YESTERDAY_LOG',
                          help='plus this flag to specify yesterday\'s log file, based on the file specify by \'-f\'',
                          action='store_true', default=False)
        parser.add_option('-D', dest='DOMAIN_RATIO',
                          help='use this flag to calculate domain success ratio',
                          action='store_true', default=False)
        parser.add_option('--datetime', dest='DATETIME',
                          help='specify a time period as format "YYYYMMDD:YYYYMMDD"')
        return parser

    def parse_command_args(self):
        """
        deal with command line args
        """
        parser = CommandArgs().arg_parser
        (options, args) = parser.parse_args()

        cf = options.CONFIG if options.CONFIG else setting.CONFIG
        log = options.FILE if options.FILE else setting.LOG
        log = ".".join(
            [str(log), str(setting.YESTERDAY)]) if options.YESTERDAY_LOG else log  # turn the log to yesterday's
        omit_file = options.OMIT if options.OMIT else setting.OMIT  # program would add file date as suffix
        tabulate_file = os.path.join(setting.RESULT_FOLDER, options.TABULATE) if options.TABULATE else setting.TABULATE
        datetime_period = options.DATETIME

        # return [cf,log,omit_file,tabulate_file,datetime_period]
        return {
            'cf': cf,
            'log': log,
            'omit_file': omit_file,
            'tabulate_file': tabulate_file,
            'datetime_period': datetime_period,
        }


class ConfFile(BaseInput):
    def read_conf_file(self, cf):
        config = MyConfigParser()
        config.read(cf)
        return config


class LogFile(BaseInput):
    def read_log_file(self, log):
        pass


class Input(BaseInput,CommandArgs,ConfFile,):
    pass


if __name__ == '__main__':
    cf = Input()
    # default_var_list = cf.default_setting
    var_dict = cf.parse_command_args()
    cf.read_conf_file(var_dict['cf'])

    # execfile('setting.py')
    # print dir()
    # print RMI_LOG
    # import setting
    # print setting.RMI_LOG
