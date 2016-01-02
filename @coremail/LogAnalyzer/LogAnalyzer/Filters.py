"""
filter part;
deal with file stream;
"""
from Inputs import Inputs
from Utils import MyConfigParser
import ast
import re


class BaseFilter(object):
    def __init__(self):
        self.vars_dict = {}

    @property
    def _vars(self):
        return self.vars_dict

    @_vars.setter
    def _vars(self, key_value):
        assert isinstance(key_value, dict)
        self.vars_dict.update(key_value)

    def trans_config(self):
        raise NotImplementedError

    def match_pattern(self):
        raise NotImplementedError

    def traverse_file(self):
        raise NotImplementedError

    def find_omit(self):
        raise NotImplementedError

    def result(self):
        raise NotImplementedError

    def domain_conn_info(self):
        raise NotImplementedError


class IniFilter(BaseFilter):
    def __init__(self):
        super(IniFilter, self).__init__()
        self.res = {}

    def trans_config(self, ini_config):
        """
        trans ini_config to iterable datastructs like:
            (
                (section_name,
                    (
                        (key, value),
                        ...
                    )
                ),
                ...
            )
        """
        assert isinstance(ini_config, MyConfigParser)
        self.sections = sorted(ini_config.sections())
        self.section_items = ((section, ini_config.items(section)) for section in self.sections)
        return self.section_items

    @staticmethod
    def match_pattern(pattern, line, do_eval=True, use_regex=False):
        """Core method
        """
        if use_regex and re.match(r'r".*"', pattern):
            return re.match(pattern, line)
        if do_eval:
            pattern = ast.literal_eval(pattern)
        if isinstance(pattern, str) or isinstance(pattern, unicode):
            return pattern in line
        if isinstance(pattern, list):
            return all([p in line for p in pattern])
        if isinstance(pattern, tuple):
            return any([p in line for p in pattern])

    @staticmethod
    def gen_lines(gen):
        return [line for line in gen]

    @staticmethod
    def gen_len(gen):
        return len(self.gen_lines(gen))

    def traverse_file(self, file_gen, config_data, use_gen=True):
        """Core method
        """
        if use_gen:
            self.iter_file_gen(file_gen, config_data)
        else:
            self.iter_file_lines(file_gen, config_data)

    def iter_file_gen(self, file_gen, config_data):
        for section in config_data:
            section_name, items = section
            if self.res.has_key(section_name):
                file_gen = self.res.get(section_name).get('gen')
            for k, v in items:
                match_lines = (line.rstrip('\n') for line in file_gen if
                               self.match_pattern(v, line, True, self.vars_dict['USE_REGEX']))
                # lines = list(match_lines)
                # counts = len(lines)
                self.res['/'.join([section_name, k])] = {'gen': match_lines,
                                                         # 'lines': lines,
                                                         # 'counts': counts
                                                         }

    def iter_file_lines(self, file_gen, config_data):
        pass

    def find_omit(self):
        pass

    @property
    def result(self):
        return {'RESULT': self.res}


class DomainInfo(BaseFilter):
    def __init__(self):
        super(DomainInfo, self).__init__()

    @property
    def domain_conn_info(self):
        if self.vars_dict['DOMAIN_CONNECT_INFO']:
            raise NotImplementedError
        return {'DOMAIN_CONNECT': None}


class Filters(IniFilter, DomainInfo):
    def __init__(self, inputs_res):
        super(Filters, self).__init__()
        self._vars = inputs_res

    def process(self):
        config_data = self.trans_config(self.vars_dict['INI'])
        self.traverse_file(self.vars_dict['FILE_GEN'], config_data)
        self._vars = self.result
        self._vars = self.domain_conn_info
        return self.vars_dict


if __name__ == '__main__':
    filters = Filters(Inputs().process())
    all_vars = filters.process()
    print all_vars
