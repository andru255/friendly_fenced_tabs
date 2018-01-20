#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This class focus for reorder the array data output
    that gives markdown and insert with useful data
    to read&parse the tabs
'''
from utils import Utils

class TabRecollector(object):
    def __init__(self):
        pass

    def get_lines_with_tabs(self, lines, reader_obj, tab_callback=None):
        content = ''
        output = []
        fenced_code_founded = []
        content_iterator = self._search_and_format(lines, reader_obj)
        for current_match, last_match in content_iterator:
            fenced_code_founded.append(current_match['line_found'])

        for index, line in enumerate(lines):
            if index in fenced_code_founded:
                output.insert(index, [ {"meta": "cool"} ])
            else:
                output.append(line)

        print("output", output)
        return output

    def _search_and_format(self, lines, reader_obj):
        content = '\n'.join(lines)
        last_match = None
        while True:
            match = reader_obj.match_code_content(content)
            if match:
                placeholder = '<friendly_fenced_tabs/>'
                content_initial_start = "{}\n".format(
                    content[:match.start()]
                )
                line_found = content_initial_start.split("\n")
                num_line_found = len(line_found) - 1
                current_match = {
                    "match": match,
                    "line_found": num_line_found
                }
                content = "{}\n{}\n{}".format(
                    content[:match.start()],
                    placeholder,
                    content[match.end():]
                )
                yield current_match, last_match
                last_match = current_match
            else:
                break

    def wrapper_with_tab(self, match, last_found, content):
        lines = content.split("\n")
        if last_found:
            print("LAST_FOUND", last_found.start(), last_found.end())
        print("CURRENT", match.start(), match.end())
        print("NUM_LINE_FOUND>>>>>", lines)
        print("LINES>>>>>", lines)
        return ":D"

    def with_tabs(self, group):
        for index, tab in enumerate(group):
            yield index, tab

    def _tab_is_sibling(self, lines, last_founded, meta_data):
        last_index_end = 0
        current_start_index = 0

        if 'end' in last_founded:
            last_index_end = last_founded['end']
        if 'index_start' in meta_data:
            current_start_index = meta_data['index_start']
        
        if last_index_end != 0 and current_start_index != 0:
            if self._is_only_whitespaces_in_range(lines, last_index_end + 1, current_start_index):
                return True

        return False
    
    def _is_only_whitespaces_in_range(self, lines, index_start, index_end):
        range_to_check = lines[index_start: index_end]
        for line in range_to_check:
            if line != u'':
                return False
        return True

    def _nothing_between_symbols(self, lines, last_founded, meta_data):
        last_index_end = 0
        current_start_index = 0
        range = []

        if 'end' in last_founded:
            last_index_end = last_founded['end']
        if 'index_start' in meta_data:
            current_start_index = meta_data['index_start']

        if last_index_end != 0 and current_start_index != 0:
            range = lines[last_index_end+1: current_start_index]
        print("range", range)
        return True if len(range) == 0 else False

    def _filter_tab_groups(self, group, lines):
        output = []
        for line in lines:
            if isinstance(line, dict):
                if 'group' in line:
                    if line['group'] == group:
                        output.append(line)
        return output