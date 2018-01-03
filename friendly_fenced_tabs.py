#!/usr/bin/env python

"""
Fenced code tabs extension for python markdown
================================
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from jinja2 import Template

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension
from markdown.extensions.codehilite import parse_hl_lines

import lib
from utils import Utils

READER = lib.Reader()
PARSER = lib.Parser()
TAB_RECOLLECTOR = lib.TabRecollector()

class FriendlyPreprocessor(Preprocessor):
    '''
    Class for process content from markdown
    '''
    def __init__(self, md, extension_config=None):
        #setting the template
        str_template = extension_config['template']
        self.template = Template(str_template)

        #setting the compiler
        self.compiler = lib.Compiler(extension_config, extra_extensions={
            'Codehilite'     : CodeHilite,
            'parse_hl_lines' : parse_hl_lines
        })
        super(FriendlyPreprocessor, self).__init__(md)

    def _check_Codehilite(self):
       for ext in self.markdown.registeredExtensions:
           if isinstance(ext, CodeHiliteExtension):
               yield ext.config
               break

    def _get_html_group_tabs(self, line):
        headers = []
        contents = []

        for index, tab in TAB_RECOLLECTOR.with_tabs(line):
            token = READER.match(tab['content'])
            tab_node = PARSER.generate_node(token)
            tab_node['active_class'] = ''
            if index == 0:
                tab_node['active_class'] = 'active'

            headers.append(self.compiler.header_output(tab_node, token['options']))
            contents.append(self.compiler.content_output(tab_node, token['options']))

            tab_html = self.template.render(
                group = tab['group'],
                friendly_config= self.compiler.settings,
                headers=headers,
                contents=contents
            )
            yield tab_html

    def run(self, lines):
        #prepare the config
        for config in self._check_Codehilite():
            self.compiler.update_settings('codehilite_config', config)

        #preprocessing the lines
        lines_with_tabs = TAB_RECOLLECTOR.get_lines_with_tabs(lines, READER)
        for index, line in enumerate( lines_with_tabs ):
            if isinstance( line , list):
                for tab_html in self._get_html_group_tabs(line):
                    lines_with_tabs[ index ] = self.markdown.htmlStash.store(tab_html, safe=True) 

        return lines_with_tabs

class FriendlyFencedTabsExtension(Extension):
    def __init__(self, *args, **kwargs):
        #Defining the config options and defaults
        self.config = {
            'single_block_as_tab'       : [False, 'Enable single_block_as_tab'],
            'active_class'              : ['active', 'css class name to the active tab'],
            'template'                  : [ Utils.get_str_from_content('template.html') , 'template for container tabs on jinja syntax'],
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