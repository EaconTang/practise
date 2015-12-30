"""
Input module
including:
    1. default settings from file <settings.py>
    2. command line args
    3. configuration from conf/*.conf
    4. log file streams
"""
import os
from optparse import OptionParser
from Util import MyConfigParser
import setting


class BaseInputs(object):
    def __init__(self):
        # self.vars_dict = vars_dict
        # self.file_lines = file_lines

    def load_default(self):
        raise NotImplementedError

    def parse_command_args(self):
        raise NotImplementedError

    def read_conf_file(self, cf):
        raise NotImplementedError

    def read_log_file(self, log):
        raise NotImplementedError

    def returns(self):
        raise NotImplementedError


class DefaultSetting(BaseInputs):
    def __init__(self):
        super(DefaultSetting, self).__init__()
        self._default_vars = []

    @staticmethod
    @property
    def default_vars(self):
        default_vars = dir(setting)
        default_vars = filter(lambda x: x == x.upper(), default_vars)
        return default_vars

    def load_default(self):
        self._default_vars = self.default_vars


class CommandArgs(BaseInputs):
    def __init__(self):
        super(CommandArgs, self).__init__()

    @property
    def arg_parser(self):
        """
        provide optional arguments when starting the program
        :return: an option parser
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
        according to command line args and default setting, conclude final vars
        :return: vars <dict>, used by following steps
        """
        parser = self.arg_parser
        (options, args) = parser.parse_args()

        cf = options.CONFIG if options.CONFIG else setting.CONFIG
        log = options.FILE if options.FILE else setting.LOG
        log = ".".join(
            [str(log), str(setting.YESTERDAY)]) if options.YESTERDAY_LOG else log  # turn the log to yesterday's
        omit_file = options.OMIT if options.OMIT else setting.OMIT  # program would add file date as suffix
        tabulate_file = os.path.join(setting.RESULT_FOLDER, options.TABULATE) if options.TABULATE else setting.TABULATE
        datetime_period = options.DATETIME

        _vars = {
            'cf': cf,
            'log': log,
            'omit_file': omit_file,
            'tabulate_file': tabulate_file,
            'datetime_period': datetime_period,
        }
        return _vars


class ConfFile(BaseInputs):
    def __init__(self):
        super(ConfFile, self).__init__()

    def read_conf_file(self, conf_file):
        if conf_file.endswith('ini') or conf_file.endswith('conf') or conf_file.endswith('cf'):
            return self.read_ini(conf_file)
        elif conf_file.endswith('json'):
            return self.read_json(conf_file)
        elif conf_file.endswith('yaml'):
            return self.read_yaml(conf_file)
        else:
            exit('[Error]Unsupported config file format?')

    def read_ini(self, conf_file):
        config = MyConfigParser()
        config.read(conf_file)
        return {
            'sections': sorted(config.sections())
        }

    def read_json(self, conf_file):
        raise NotImplementedError

    def read_yaml(self, cong_file):
        raise NotImplementedError


class LogFile(BaseInputs):
    def __init__(self):
        super(LogFile, self).__init__()

    def read_log_file(self, log):
        pass
        return {
            'filelines': None
        }


class Inputs(DefaultSetting, CommandArgs, ConfFile, LogFile):
    def __init__(self):
        super(Inputs,self).__init__()

    @property
    def returns(self):
        return [self.vars, self]


if __name__ == '__main__':
    print vars(setting)
    all_vars = {}
    inputs = Inputs()

    some_vars = inputs.parse_command_args()
    all_vars.update(some_vars)

    sections = inputs.read_conf_file(all_vars['cf'])
    all_vars.update(sections)

    filelines = inputs.read_log_file(all_vars['log'])
    all_vars.update(filelines)


    # execfile('setting.py')
    # print dir()
    # print RMI_LOG
    # import setting
    # print setting.RMI_LOG
