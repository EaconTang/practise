"""
Filter part: deal with file stream, return analysis result
Template Method Pattern
"""
from Utils import MyConfigParser, log_info
from ast import literal_eval
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

    def trans_config(self, *args, **kwargs):
        raise NotImplementedError

    def match_pattern(self, *args, **kwargs):
        raise NotImplementedError

    def traverse_file(self, *args, **kwargs):
        raise NotImplementedError

    def find_omit(self, *args, **kwargs):
        raise NotImplementedError

    def result(self, *args, **kwargs):
        raise NotImplementedError

    def domain_conn_info(self, *args, **kwargs):
        raise NotImplementedError


class IniFilter(BaseFilter):
    def __init__(self):
        super(IniFilter, self).__init__()
        self.res = {}
        self.res_lines = {}
        self.res_counts = {}
        self.omit_lines = {}

    @log_info()
    def trans_config(self, ini_config):
        """
        trans ini_config to iterable datastruct like:
            [(section_name,((key, value),...)),...]
        """
        assert isinstance(ini_config, MyConfigParser)
        self.sections = sorted(ini_config.sections())
        self.section_items = [(section, ini_config.items(section)) for section in self.sections]
        return self.section_items

    @staticmethod
    def match_pattern(pattern, line, do_eval=True, use_regex=False):
        """
        Core method(Deprecated)
        But this method calls function too much, cause the times of function call depends on filelines number
        """
        if use_regex and re.match(r'r".*"', pattern):
            return re.match(pattern, line)
        if do_eval:
            pattern = literal_eval(pattern)
        if isinstance(pattern, str) or isinstance(pattern, unicode):
            return pattern in line
        if isinstance(pattern, list):
            return all([p in line for p in pattern])
        if isinstance(pattern, tuple):
            return any([p in line for p in pattern])

    @staticmethod
    def grep_lines(pattern, file_lines, do_eval=True, use_regex=False):
        """
        Core method
        This old method is faster, times of function call depends on config options' number
        """
        if use_regex and re.match(r'r".*"', pattern):
            lines = [line.rstrip('\n') for line in file_lines if re.match(pattern, line)]
        # pattern = eval(pattern)        # out of security concern
        if do_eval:
            pattern = literal_eval(pattern)
        if isinstance(pattern, str) or isinstance(pattern, unicode):
            lines = [line.rstrip('\n') for line in file_lines if pattern in line]
        elif isinstance(pattern, list):
            lines = [line.rstrip('\n') for line in file_lines if all([p in line for p in pattern])]
        elif isinstance(pattern, tuple):
            lines = [line.rstrip('\n') for line in file_lines if any([p in line for p in pattern])]
        else:
            exit('Error: wrong format in config file, some values are neither list nor string?')
        return lines

    @log_info()
    def traverse_file(self, config_data, filename, file_gen):
        """Core method
        """
        for lines in file_gen:
            self.iter_file_lines(lines, config_data)
        if self.vars_dict.get('SAVE_OMIT'):
            self.save_omit(config_data, self.res_lines, self.res_counts)

    def iter_file_lines(self, file_lines, config_data):
        """Core method
        """
        section_root = self.vars_dict.get('ROOT_NAME', 'All')
        self.res_lines[section_root] = self.res_lines.get(section_root, []) + map(lambda x: x.rstrip('\n'), file_lines)
        self.res_counts[section_root] = self.res_counts.get(section_root, 0) + len(file_lines)
        for section_name, items in config_data:
            if self.res_lines.has_key(section_name):
                file_lines = self.res_lines.get(section_name)
            for k, v in items:
                match_lines = self.grep_lines(v, file_lines)
                full_name = '/'.join([section_name, k])
                self.res_lines[full_name] = self.res_lines.get(full_name, []) + match_lines
                self.res_counts[full_name] = self.res_counts.get(full_name, 0) + len(match_lines)

    @log_info()
    def save_omit(self, config_data, res_lines, res_counts):
        """Core method
        """
        omit_name = self.vars_dict.get('OMIT_NAME', '(OMIT)')
        for section_name, items in config_data:
            parent_lines = res_lines.get(section_name)
            child_lines = []
            for k, v in items:
                child_lines.extend(res_lines.get('/'.join([section_name, k])))
            # set operation would remove duplicates
            omit_lines = set(parent_lines) - set(child_lines)
            if len(omit_lines) != 0:
                key = '/'.join([section_name, omit_name])
                res_lines[key] = list(omit_lines)
                res_counts[key] = len(omit_lines)

    @property
    def result(self):
        return {'RESULT':
                    {'RESULT_LINES': self.res_lines,
                     'RESULT_COUNTS': self.res_counts,
                     'OMIT_LINES': self.omit_lines,
                     }
                }


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
        self.traverse_file(config_data, self.vars_dict['FILE_PATH'], self.vars_dict['FILE_GEN'])
        self._vars = self.result
        self._vars = self.domain_conn_info
        return self.vars_dict


if __name__ == '__main__':
    import Inputs
    filters = Filters(Inputs.Inputs().process())
    all_vars = filters.process()

