#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This class focus for reorder the array data output
    that gives markdown and insert with useful data
    to read&parse the tabs
'''

class TabRecollector(object):
    def __init__(self):
        pass

    def get_lines_with_tabs(self, lines, reader_obj):
        cleaned_lines = self._remove_whitespaces(lines)
        lines_to_buffer = []
        tab_meta = {}
        opened_fenced_expr = False
        last_founded = {}
        group = 0

        for index, line in enumerate(cleaned_lines):
            match = reader_obj.match_fenced_symbol(line)
            if match:
                # check if is opened
                if opened_fenced_expr:
                    # close the block founded
                    tab_meta['index_end'] = index
                    opened_fenced_expr = False
                else:
                    # open if is False
                    opened_fenced_expr = True
                    tab_meta['index_start'] = index

                # append
                if 'content' in tab_meta:
                    tab_meta['content'] += line

                    # grouping
                    if self._tab_is_sibling(last_founded, tab_meta):
                        tab_meta['group'] = last_founded['group']
                    else:
                        tab_meta['group'] = group
                        last_founded['group'] = tab_meta['group']
                        group += 1
                    # for new line and don't contains into a paragraph
                    lines_to_buffer.append(u'\n')
                    # adding the metadata
                    lines_to_buffer.append(tab_meta)
                    last_founded['start'] = tab_meta['index_start']
                    last_founded['end'] = tab_meta['index_end']
                    tab_meta = {}
                else:
                    tab_meta['content'] = '%s\n' % line
            else:
                if opened_fenced_expr:
                    tab_meta['content'] += '%s\n' % line
                else:
                    lines_to_buffer.append(line)
                    tab_meta = {}
                    continue

        # sorting
        output = lines_to_buffer[:]
        registered_groups = []
        for index, line in enumerate(lines_to_buffer):
            if 'group' in line:
                groups = self._filter_tab_groups(line['group'], lines_to_buffer)
                if not line['group'] in registered_groups:
                    output[index] = groups
                    registered_groups.append(line['group'])
                else:
                    output[index] = u''
        return output

    def with_tabs(self, group):
        for index, tab in enumerate(group):
            yield index, tab

    def _remove_whitespaces(self, lines):
        return list(filter(lambda line: line != u'', lines))

    def _tab_is_sibling(self, last_founded, meta_data):
        last_index_end = 0
        current_start_index = 0

        if 'end' in last_founded:
            last_index_end = last_founded['end']
        if 'index_start' in meta_data:
            current_start_index = meta_data['index_start']

        if last_index_end == current_start_index - 1:
            return True

        return False

    def _filter_tab_groups(self, group, lines):
        output = []
        for line in lines:
            if 'group' in line:
                if line['group'] == group:
                    output.append(line)
        return output
