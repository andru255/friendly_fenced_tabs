#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fenced code tabs extension for python markdown
================================
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from htmlmin import minify
from jinja2 import Template

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension
from markdown.extensions.codehilite import parse_hl_lines

from .reader import Reader
from .parser import Parser
from .tab_recollector import TabRecollector
from .compiler import Compiler
from .utils import Utils

READER = Reader()
PARSER = Parser()
TAB_RECOLLECTOR = TabRecollector()

class FriendlyPreprocessor(Preprocessor):
    '''
    Class for process content from markdown
    '''
    def __init__(self, md, extension_config=None):
        #setting the template
        str_template = extension_config['template']
        self.template = Template(str_template, trim_blocks=True, lstrip_blocks=True)
        #getting the active_class from config
        self.active_class = extension_config['active_class']

        #setting the compiler
        self.compiler = Compiler(extension_config, extra_extensions={
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
                tab_node['active_class'] = self.active_class

            headers.append(self.compiler.header_output(tab_node, token['options']))
            contents.append(self.compiler.content_output(tab_node, token['options']))

            tab_html = self.template.render(
                group=tab['group'],
                friendly_config=self.compiler.settings,
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
        for index, line in enumerate(lines_with_tabs):
            if isinstance(line, list):
                for tab_html in self._get_html_group_tabs(line):
                    trimed_html = minify(tab_html.decode("utf-8"),
                                         remove_empty_space=True,
                                         remove_comments=True)
                    lines_with_tabs[index] = self.markdown.htmlStash.store(trimed_html, safe=True)
        return lines_with_tabs

class FriendlyFencedTabsExtension(Extension):
    def __init__(self, *args, **kwargs):
        current_path = os.path.dirname(__file__)
        default_template = "{}/{}".format(current_path, 'template.html')
        #Defining the config options and defaults
        self.config = {
            'single_block_as_tab'       : [False, 'Enable single_block_as_tab'],
            'active_class'              : ['active', 'css class name to the active tab'],
            'template'                  : [default_template, 'template for tabs on jinja syntax']
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
        template_file = self.getConfig('template')
        self.setConfig('template', Utils.get_str_from_content(template_file))

        md.registerExtension(self)
        md.preprocessors.add('fenced_code_block',
                             FriendlyPreprocessor(md, self.getConfigs()),
                             '>normalize_whitespace')

    # important to register our extension
    # if invoke makeExtension func into this class,
    # friendly_fenced_tabs:FriendlyFencedTabsExtensions is register
    #def makeExtension(*args, **kwargs):
    #    return FriendlyFencedTabsExtension(*args, **kwargs)

# important to register our extension
# if invoke makeExtension func directly, friendly_fenced_tabs register directly
def makeExtension(*args, **kwargs):
    return FriendlyFencedTabsExtension(*args, **kwargs)
