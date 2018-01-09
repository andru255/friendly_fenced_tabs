#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This class returns a readable node
    ready to compile them
'''
from .utils import Utils

class Parser(object):
    def generate_node(self, token):
        title = 'untitled'

        # if lenguage defined exists, take it to title
        language = token['language']
        if language:
            title = language

        # if 'friendly_title' exists on token
        options = token['options']
        friendly_title = Utils.get_value_by_key_name(options, 'friendly_title')
        if friendly_title:
            title = friendly_title

        # body scaped content
        code = token['code']
        scaped_body = self._escape(code)
        title_value = self._format_title(title)

        data = {
            "title": title_value,
            "code": scaped_body,
            "language": language,
            "slug": self._hypenize(title_value)
        }
        return data

    def _format_title(self, value):
        capitalized = value.capitalize()
        formated_title = capitalized.replace('-', ' ')
        return formated_title

    def _hypenize(self, value):
        lower_value = value.lower()
        hypen_value = lower_value.replace(' ', '-')
        return hypen_value

    def _escape(self, text):
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        return text
