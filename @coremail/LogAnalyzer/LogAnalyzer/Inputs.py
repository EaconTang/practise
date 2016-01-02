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
import datetime
from Utils import MyConfigParser, convert_to_logfiles
import settings


class BaseInputs(object):
    def __init__(self):
        self.vars_dict = {}

    @property
    def _vars(self):
        return self.vars_dict

    @_vars.setter
    def _vars(self, key_value):
        assert isinstance(key_value, dict)
        self._vars.update(key_value)

    def default_vars(self):
        raise NotImplementedError

    def command_args(self):
        raise NotImplementedError

    def read_conf(self):
        raise NotImplementedError

    def read_log_file(self):
        raise NotImplementedError


class DefaultSetting(BaseInputs):
    def __init__(self):
        super(DefaultSetting, self).__init__()
        self._default_vars_list = []
        self._default_vars = {}

    @property
    def default_var_list(self):
        self._default_vars_list = filter(lambda x: x == x.upper(), dir(settings))
        return self._default_vars_list

    @property
    def default_vars(self):
        var_list = self.default_var_list
        var_vals = vars(settings)
        for each in var_list:
            self._default_vars[each] = var_vals.get(each)
        return self._default_vars


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
        parser.add_option('-T', '--tabulate', dest='SAVE_TABULATE',
                          help='use this flag to save the results to the file,defaults to under "~/LogMiner/results"',
                          action='store_true', default=False)
        parser.add_option('-t', '--tabulate-file', dest='TABULATE_FILE',
                          help='specify a file to save the tabulate table')
        parser.add_option('-O', '--omit', dest='SAVE_OMIT',
                          help='use this flag to save the omit info that were not classified.' +
                               'It would be saved under "~/LogMiner/results"',
                          action='store_true', default=False)
        parser.add_option('-o', '--omit-file', dest='OMIT_FILE',
                          help='specific a filename to save the omit info,defaults to "rmi_api.omit.{LogDate}"')
        parser.add_option('-Y', '--yesterday-log', dest='YESTERDAY',
                          help='plus this flag to specify yesterday\'s log file, based on the file specify by \'-f\'',
                          action='store_true', default=False)
        parser.add_option('-D', dest='DOMAIN_CONNECT_INFO',
                          help='use this flag to calculate domain success ratio',
                          action='store_true', default=False)
        parser.add_option('--datetime', dest='TIME_PERIOD',
                          help='specify a time period as format "YYYYMMDD:YYYYMMDD"')
        return parser

    @property
    def command_args(self):
        """return a dict contains args uesd from command line
        """
        parser = self.arg_parser
        # (options, args) = parser.parse_args()
        (options, args) = parser.parse_args(
            ['-f', 'files/rmi_api.log.2015-11-11', '-c', 'conf/rmi.cf'])
        options_list = [('FILE', options.FILE),
                        ('CONFIG', options.CONFIG),
                        ('OMIT_FILE', options.OMIT_FILE),
                        ('SAVE_OMIT', options.SAVE_OMIT),
                        ('TABULATE_FILE', options.TABULATE_FILE),
                        ('SAVE_TABULATE', options.SAVE_TABULATE),
                        ('YESTERDAY', options.YESTERDAY),
                        ('DOMAIN_CONNECT_INFO', options.DOMAIN_CONNECT_INFO),
                        ('TIME_PERIOD', options.TIME_PERIOD),
                        ]
        used_options = [option for option in options_list if option[1]]
        return dict(used_options)


class ConfFile(BaseInputs):
    def __init__(self):
        super(ConfFile, self).__init__()

    def read_conf(self, conf_file):
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
        return {'INI': config}

    def read_json(self, conf_file):
        raise NotImplementedError

    def read_yaml(self, cong_file):
        raise NotImplementedError


class LogFile(BaseInputs):
    def __init__(self):
        super(LogFile, self).__init__()

    def read_log_file(self, log_file, yesterday=False, time_period=None):
        # read yesterday's logfile
        if yesterday:
            YESTERDAY = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
            return {
                'FILE_GEN': self.file_gen(self.vars_dict['FILE']),
                'FILE': '.'.join([log_file, str(YESTERDAY)]),
            }
        # read log files specified by datetime
        if time_period:
            files = convert_to_logfiles(time_period, log_file)
            return {
                'FILE_GEN': self.files_gen(files),
                'FILE': files
            }

        return {'FILE_GEN': self.file_gen(log_file)}

    @staticmethod
    def file_gen(filename):
        """a generator that each time gens a line for a single file
        """
        with open(filename) as f:
            for line in f:
                yield line

    @staticmethod
    def files_gen(filenames):
        """a generator that each time gens a line for multi files
        """
        def _gens(filename_list):
            # return a generator that gens generator(file_gen)
            for filename in filename_list:
                yield LogFile.file_gen(filename)

        gs = _gens(filenames)
        for g in gs:
            for line in g:
                yield line


class Inputs(DefaultSetting, CommandArgs, ConfFile, LogFile):
    def __init__(self):
        super(Inputs, self).__init__()

    def process(self):
        """
        1. load default vars to vars dict
        2. updates command args to vars dict
        3. load config instance to vars dict
        4. load file(s) generator to vars dict
        :return: vars dict
        """
        self._vars = self.default_vars
        self._vars = self.command_args
        self._vars = self.read_conf(self.vars_dict['CONFIG'])
        self._vars = self.read_log_file(self.vars_dict['FILE'],
                                        self.vars_dict['YESTERDAY'],
                                        self.vars_dict['TIME_PERIOD'])

        return self._vars


if __name__ == '__main__':
    inputs = Inputs()
    print inputs.process()
    log_file = inputs.vars_dict['FILE']
    print log_file
    f_gen = inputs.vars_dict['FILE_GEN']
    print f_gen.next()

