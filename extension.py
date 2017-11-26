#!/usr/bin/env python

"""
Fenced code tabs extension for python markdown
================================
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import deque
from markdown.extensions import Extension
import lib
from utils import Utils
from markdown.preprocessors import Preprocessor

reader = lib.Reader()
parser = lib.Parser()
tab_recollector = lib.TabRecollector()

class FriendlyPreprocessor(Preprocessor):
    '''
    Class for process content from markdown
    '''
    def __init__(self, md, extension_config=None):
        self.extension_config = extension_config
        default_config = {
            'single_block_as_tab'       : self.extension_config['single_block_as_tab'],
            'template_container'        : Utils.get_str_from_content('template/default_container.html'),
            'template_header_container' : Utils.get_str_from_content('template/default_header_container.html'),
            'template_header_item'      : Utils.get_str_from_content('template/default_header_item.html'),
            'template_content_container': Utils.get_str_from_content('template/default_content_container.html'),
            'template_content_item'     : Utils.get_str_from_content('template/default_content_item.html'),
            'template_block_no_tab'     : Utils.get_str_from_content('template/default_block_no_tab.html')
        }
        self.compiler = lib.Compiler(default_config)
        super(FriendlyPreprocessor, self).__init__(md)

    def _check_Extension(self, extensions):
        pass

    def _get_html_group_tabs(self, line):
        tab_headers = ""
        tab_contents = ""
        for tab in tab_recollector.with_tabs(line):
            match = reader.match(tab['content'])
            if match:
                tab_config = reader.kwargs_from_content(tab['content'])
                token = match.groupdict()
                tab_node = parser.generate_node(token)
                tab_headers += self.compiler.header_output(tab_config, tab_node)
                tab_contents += self.compiler.content_output(tab_config, tab_node)
                tab_html = self.compiler.compile(tab_headers, tab_contents)
                yield tab_html

    def _get_html_group_one_tab(self, line):
        for tab in tab_recollector.with_tabs(line):
            match = reader.match(tab['content'])
            if match:
                tab_config = reader.kwargs_from_content(tab['content'])
                token = match.groupdict()
                tab_node = parser.generate_node(token)
                tab_html = self.compiler.compile_one_tab(tab_config, tab_node)
                yield tab_html

    def run(self, lines):
        lines_with_tabs = tab_recollector.get_lines_with_tabs(lines, reader)
        for index, line in enumerate( lines_with_tabs ):
            if isinstance( line , list):
                #if found a group of one tab
                if len(line) == 1:
                    for tab_html in self._get_html_group_one_tab(line):
                       lines_with_tabs[index] = self.markdown.htmlStash.store(tab_html, safe=True)
                #if found a group of more than one tab
                else:
                    for tab_html in self._get_html_group_tabs(line):
                        lines_with_tabs[ index ] = self.markdown.htmlStash.store(tab_html, safe=True) 
        return lines_with_tabs

class FriendlyFencedTabsExtension(Extension):
    def __init__(self, *args, **kwargs):
        #Defining the config options and defaults
        self.config = {
            'single_block_as_tab': [False, 'Enable single_block_as_tab']
        }
        #Call the parent class's __init__ method to configure options
        super(FriendlyFencedTabsExtension, self).__init__(*args, **kwargs)

    def to_bool(self, param):
        the_bool = param
        if isinstance(param, str):
            the_bool = False if param.lower() is 'false' else True
        return the_bool

    def extendMarkdown(self, md, md_globals):
        self.setConfig('single_block_as_tab', self.to_bool(
            self.getConfig('single_block_as_tab')
        ))
        md.registerExtension(self)
        md.preprocessors.add('fenced_code_block', 
          FriendlyPreprocessor(md, self.getConfigs()),
          '>normalize_whitespace')

    def makeExtension(*args, **kwargs):
        return FriendlyFencedTabsExtension(*args, **kwargs)