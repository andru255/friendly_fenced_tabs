#!/usr/bin/env python

"""
A litle demo to use friendly_fenced_tabs
================================
"""

import markdown
from extension import FriendlyFencedTabsExtension
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension

from utils import Utils
cwd = Utils.get_current_path()
text_main = Utils.get_str_from_content('tests/fixtures/block-mixed-002.md', cwd)

# main
#output = markdown.markdown(text_main,
#                           extensions=['extension:FriendlyFencedTabsExtension', 'markdown.extensions.codehilite:CodeHiliteExtension'],
#                           extension_configs = {
#                               'extension:FriendlyFencedTabsExtension': {
#                                   'single_block_as_tab': False
#                               },
#                               'CodehiliteExtension': {
#                                   'linenums': True
#                               }
#                           }
#)

output = markdown.markdown(text_main,
                           extensions=['extension:FriendlyFencedTabsExtension'],
                           extension_configs = {
                               'extension:FriendlyFencedTabsExtension': {
                                   'single_block_as_tab': False
                               }
                           }
)
print output