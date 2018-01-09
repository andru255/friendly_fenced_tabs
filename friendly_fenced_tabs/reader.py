#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This module focus into read and prepare
'''

import re

class Reader(object):
    '''
        That class only focus to analyze a text and get useful content
        to assemble the final output
    '''
    def match_fenced_symbol(self, content):
        clean_content = self._filter_content(content)
        block_regex = re.compile(r'''
          (?P<fence>^(?:~{3,}|`{3,}))[ ]*
        ''', re.VERBOSE)
        return block_regex.search(clean_content)

    def match(self, content):
        ''' return a match by a string content'''
        data = {
            'language': self.match_language(content),
            'options': self.match_options(content),
            'code': self.match_code_content(content)
        }
        return data

    def match_language(self, content):
        result = None
        str_regex = r'''
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*
            (\{?\.?(?P<language>[\w#.\+\-\\!]+[^\w_\=]))?
        '''
        clean_content = self._filter_content(content)
        block_regex = re.compile(str_regex, re.VERBOSE)
        match = block_regex.search(clean_content)
        if match:
            result = match.groupdict()['language']
            if result:
                result = result.strip()
        return result

    def match_options(self, content):
        result = []
        str_regex = r'''
            (?P<key_name>\w*)=(?P<quot>['|"]?)(?P<value>[\w\d,\. ]+)?(?P=quot)[ ]?
        '''
        clean_content = self._filter_content(content)
        block_regex = re.compile(str_regex, re.VERBOSE)
        for match in re.finditer(block_regex, clean_content):
            if match:
                result.append(match.groupdict())
        return result

    def match_code_content(self, content):
        result = None
        str_regex = r'''
             # Opening ``` or ~~~
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*
             # Optional {, and lang
            (\{?\.?[\w#.+-\\!\\/]*)?[ ]*
             # options
            (\w*=(?P<fct_quot>[ "|' ]?).*?(?P=fct_quot))?[ ]*
            \}?[ ]*\n
            (?P<code>.*?)(?<=\n)
            (?P=fence)[ ]*$
        '''
        clean_content = self._filter_content(content)
        block_regex = re.compile(str_regex, re.MULTILINE| re.DOTALL | re.VERBOSE)
        match = block_regex.search(clean_content)
        if match:
            result = match.groupdict()['code']
        return result

    def _filter_content(self, content):
        string_block = content.replace(u'\u2018', '&lsquo;') #‘
        string_block = string_block.replace(u'\u2019', '&rsquo;') #’
        string_block = string_block.replace(u'\u201c', '&ldquo;') #“
        string_block = string_block.replace(u'\u201d', '&rdquo;') #”
        string_block = string_block.replace(u'\u2013', '&rdquo;') #–
        string_block = string_block.replace(u'\xa0', '') # whitespace

        try:
            string_block = string_block.decode('ascii', 'remove')
        except ValueError:
            string_block = content

        return string_block
