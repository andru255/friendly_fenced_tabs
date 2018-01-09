#!/usr/bin/env python

"""
A litle demo to use friendly_fenced_tabs
================================
"""

import markdown
import friendly_fenced_tabs
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension

from friendly_fenced_tabs import Utils
cwd = Utils.get_current_path()
text_main = Utils.get_str_from_content('tests/fixtures/block-mixed-001.md', cwd)

# main
output = markdown.markdown(text_main,
                           extensions=['friendly_fenced_tabs'],
                           extension_configs={
                               'friendly_fenced_tabs': {
                                   'single_block_as_tab': False
                               }
                           }
)

print output