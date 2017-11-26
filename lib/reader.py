#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This module focus into read and prepare
'''

import re
from collections import OrderedDict as odict

KWARGS_REGEXES = odict((
    ('friendly_params', re.compile(r'''
        friendly_params=(?P<quot>"|')(?P<friendly_params>.*?)(?P=quot)
        ''', re.VERBOSE)),
    ('friendly_title', re.compile(r'''
        friendly_title=(?P<quot>"|')(?P<friendly_title>.*?)(?P=quot)
        ''', re.VERBOSE)),
    ('friendly_no_title', re.compile(r'''
        friendly_no_title=(?P<quot>"|')(?P<friendly_no_title>.*?)(?P=quot)
        ''', re.VERBOSE))
))

class Reader(object):
    '''
        That class only focus to analyze a text and get useful content
        to assemble the final output
    '''
    def __init__(self, **kwargs):
        ''' nothing to initialize at the moment'''

    def match_fenced_symbol(self, content):
        clean_content = self._filter_content(content)
        block_regex = re.compile(r'''
          (?P<fence>^(?:~{3,}|`{3,}))[ ]*
        ''', re.VERBOSE)
        return block_regex.search(clean_content)

    def match(self, content):
        ''' return a match by a string content'''
        clean_content = self._filter_content(content)
        block_regex = re.compile(r'''
        # Opening ``` or ~~~
         (?P<fence>
            ^(?:~{3,}|`{3,}))[ ]*

         # Check the language defined
         (\{?\.?(?P<language>[\w#.+-]*))?[ ]*

         # Optional friendly title, single- or double-quote-delimited
         (friendly_title=(?P<fct_quot>"|')(?P<friendly_title>.*?)(?P=fct_quot))?[ ]*

         # Optional closing }
         }?[ ]*\n 

         # checking the body
         (?P<code>.*?)(?<=\n)
         (?P=fence)[ ]*$
        ''', re.MULTILINE | re.DOTALL | re.VERBOSE)
        return block_regex.search(clean_content)

    def kwargs_from_content(self, content):
        ''' returns the settings defined by a block of content
            Only detects 'friendly_title', 'friendly_no_title', 'friendly_params'
        '''
        kwargs = {}
        for param, regex in KWARGS_REGEXES.items():
            param_match = regex.search(content)
            try:
                kwargs = self._filter_param_to_kwargs(param, param_match, kwargs)
            except ValueError:
                print ValueError
        return kwargs

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

    def _filter_param_to_kwargs(self, param, content, kwargs):
        result_kwargs = {}
        if kwargs:
            result_kwargs = kwargs
        if content:
            if content.group(param):
                result_kwargs[param] = content.group(param)
            else:
                raise Exception('{} needs an argument within in \n {}'.format(param, content))
        return result_kwargs
