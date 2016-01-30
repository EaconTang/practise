"""
Outputs modulr:
    1. outputs to console
    2. save outputs to file
Template Method Pattern
"""
import datetime
import os
import Utils
from Filters import CoreFilter
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

    def to_html(self):
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

        tabulate_file_titles = CoreFilter.grep_lines('LogDate', tabulate_file_lines, False)

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


class VisualizationOutputs(PrettyTableOutputs):
    def __init__(self):
        super(VisualizationOutputs, self).__init__()

    @property
    def res_counts(self):
        result = self.vars_dict.get('RESULT')
        result_counts = result['RESULT_COUNTS']
        del result_counts['All']    # remove 'ALL'
        del result_counts['All/Exception']
        type_counts = []
        assert isinstance(result_counts, dict)
        for type, count in sorted(result_counts.iteritems()):
            type_counts.append([type, count])
        return type_counts

    def get_tabulate_data(self, lastdays=-1):
        try:
            with open(self.vars_dict.get('TABULATE_FILE')) as f:
                data_lines = f.readlines()
            data_lines = filter(lambda x: '|' in x, data_lines)
            data_lines = map(lambda x: x.strip().lstrip('|').rstrip('|').split('|'), data_lines)
            data_lines_new = []
            for n, data_line in enumerate(data_lines):
                if n == 0:
                    data_lines_new.append(data_line[:-1])
                else:
                    del data_line[-1]
                    tmp_list = []
                    for i, data in enumerate(data_line):
                        if i != 0: data = int(data)
                        tmp_list.append(data)
                    data_lines_new.append(tmp_list)
            if 0 < lastdays <= len(data_lines_new) - 1:
                data_lines_lastdays = data_lines_new[-lastdays:]
                data_lines_lastdays.insert(0, data_lines_new[0])
                return data_lines_lastdays
            return data_lines_new
        except IOError, e:
            print e.message
            return None

    def google_api_htmls(self, res):
        if self.vars_dict.get('LINE_DATA'):
            chart_type = 'line_chart'
            curve_datas = self.get_tabulate_data(self.vars_dict.get('LAST_DAYS'))
            title = self.vars_dict.get('TABULATE_FILE')
            html_text = Utils.google_charts_html(chart_type, curve_datas, title, 2000, 1000)
            return html_text
        chart_type = 'both'
        rows = self.res_counts
        title = self.vars_dict.get('FILE_PATH')
        width = 2000
        height = len(rows)*50
        html_text = Utils.google_charts_html(chart_type, rows, title, width, height)
        return html_text

    def d3js_htmls(self, res):
        raise NotImplementedError

    @log_info()
    def to_visual_htmls(self, res):
        html_text = self.google_api_htmls(res)
        file_path = os.path.join(self.vars_dict.get('RESULT_FOLDER'), 'visualization.html')
        with open(file_path, 'w') as f:
            f.write(html_text)


class Outputs(ConsoleOutputs, FileOutputs, VisualizationOutputs):
    def __init__(self, filters_res):
        super(Outputs, self).__init__()
        self._vars = filters_res
        self.res = self.vars_dict.get('RESULT')

    def process(self):
        if self.vars_dict.get('TO_CONSOLE'):
            self.to_console(self.res)
        if self.vars_dict.get('TO_FILE'):
            self.to_file(self.res)
        if self.vars_dict.get('DATA_VISUALIZATION'):
            self.to_visual_htmls(self.res)


if __name__ == '__main__':
    from Inputs import Inputs
    from Filters import Filters

    filter_res = Filters(Inputs().process()).process()
    Outputs(filter_res).process()



