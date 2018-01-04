#!/usr/bin/env python

"""
A litle demo to use friendly_fenced_tabs
================================
"""

import markdown
from friendly_fenced_tabs import FriendlyFencedTabsExtension
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension

from friendly_fenced_tabs import Utils
cwd = Utils.get_current_path()
text_main = Utils.get_str_from_content('tests/fixtures/block-mixed-002.md', cwd)

# main
output = markdown.markdown(text_main,
                           extensions=['friendly_fenced_tabs:FriendlyFencedTabsExtension', 'markdown.extensions.codehilite:CodeHiliteExtension'],
                           extension_configs = {
                               'friendly_fenced_tabs:FriendlyFencedTabsExtension': {
                                   'single_block_as_tab': False
                               },
                               'markdown.extensions.codehilite:CodeHiliteExtension': {
                                   'linenums': True
                               }
                           }
)

print output