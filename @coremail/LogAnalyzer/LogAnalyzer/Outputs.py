"""
Outputs modulr:
    1. outputs to console
    2. save outputs to file
Template Method Pattern
"""
import datetime
import Utils
from Filters import IniFilter
from Utils import log_info


class BaseOutputs(object):
    def __init__(self):
        self.vars_dict = {}

    @property
    def _vars(self):
        return self.vars_dict

    @_vars.setter
    def _vars(self, key_value):
        assert isinstance(key_value, dict)
        self.vars_dict.update(key_value)

    def to_file(self):
        raise NotImplementedError

    def to_console(self):
        raise NotImplementedError


class PrettyTableOutputs(BaseOutputs):
    def __init__(self):
        super(PrettyTableOutputs, self).__init__()

    @staticmethod
    def dict_to_table(res, sortby_count=False):
        assert isinstance(res, dict)
        table = Utils.MyTable(['Type', 'Count'])
        table.align['Type'] = "l"
        for k, v in res.iteritems():
            table.add_row([k, v])
        if not sortby_count:
            return table.get_string(sortby='Type')
        else:
            return table.get_string(sortby='Count', reversesort=True)

    def dict_to_table_horizontal(self, res):
        assert isinstance(res, dict)
        keys, values = zip(*[(k, v) for k, v in sorted(res.iteritems())])

        table_title = ['LogDate']
        table_title.extend(keys)
        table_title.append('WriteTime')
        table = Utils.MyTable(table_title)

        table_row = [self.vars_dict.get('FILE_DATE')]
        table_row.extend(values)
        table_row.append(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        table.add_row(table_row)

        return table


class FileOutputs(PrettyTableOutputs):
    def __init__(self):
        super(FileOutputs, self).__init__()

    def to_file(self, res):
        if self.vars_dict.get('SAVE_OMIT'):
            self.save_omit(res, self.vars_dict.get('OMIT_FILE'))
        if self.vars_dict.get('SAVE_TABULATE'):
            self.save_tabulate(res, self.vars_dict.get('TABULATE_FILE'))

    @log_info()
    def save_omit(self, res, filename):
        to_write = ''

        if not self.vars_dict.get('USE_PRETTYTABLE'):
            to_write += Utils.dict_to_json(res.get('RESULT_COUNTS')) + '\n'
        else:
            to_write += self.dict_to_table(res.get('RESULT_COUNTS')) + '\n'
            to_write += self.dict_to_table(res.get('RESULT_COUNTS'), True) + '\n'

        omit_key = '/'.join([self.vars_dict['ROOT_NAME'], 'Exception', self.vars_dict['OMIT_NAME']])
        to_write += '\nOmit exceptions lines info:\n\n'
        to_write += Utils.list_to_json(res.get('RESULT_LINES').get(omit_key))

        with open(filename, 'w') as f:
            f.write(to_write)

    @log_info()
    def save_tabulate(self, res, filename):
        section_name = self.vars_dict.get('TABULATE_SECTION')
        res_table = {}
        for k, v in res.get('RESULT_COUNTS').iteritems():
            if k == section_name:
                short_key = k
                res_table[short_key] = v
                continue
            if k.startswith(section_name) and not k.endswith(self.vars_dict.get('OMIT_NAME')):
                short_key = k[len(section_name) + 1:]
                res_table[short_key] = v

        table = self.dict_to_table_horizontal(res_table)

        try:
            tabulate_file_lines = open(filename).readlines()
        except IOError:
            tabulate_file_lines = []

        tabulate_file_titles = IniFilter.grep_lines('LogDate', tabulate_file_lines, False)

        if not tabulate_file_lines:
            # means a new file
            to_write = table.get_title_with_bar() + '\n' + \
                       table.get_row_data(1) + '\n'
        elif tabulate_file_titles != [] and table.get_row_data(0) != tabulate_file_titles[-1]:
            # means config updated
            to_write = '\n###############config file is updated##############\n' + \
                       table.get_title_with_bar() + '\n' + \
                       table.get_row_data(1) + '\n'
        else:
            # just add it
            to_write = table.get_row_data(1) + '\n'

        with open(filename, 'a+') as f:
                f.write(to_write)


class ConsoleOutputs(PrettyTableOutputs):
    def __init__(self):
        super(ConsoleOutputs, self).__init__()

    def to_console(self, res):
        if not self.vars_dict.get('USE_PRETTYTABLE'):
            print Utils.dict_to_json(res.get('RESULT_COUNTS'))
        else:
            print self.dict_to_table(res.get('RESULT_COUNTS'))


class Outputs(ConsoleOutputs, FileOutputs):
    def __init__(self, filters_res):
        super(Outputs, self).__init__()
        self._vars = filters_res
        self.res = self.vars_dict.get('RESULT')

    def process(self):
        if self.vars_dict.get('TO_CONSOLE'):
            self.to_console(self.res)
        if self.vars_dict.get('TO_FILE'):
            self.to_file(self.res)


if __name__ == '__main__':
    from Inputs import Inputs
    from Filters import Filters

    filter_res = Filters(Inputs().process()).process()
    Outputs(filter_res).process()
