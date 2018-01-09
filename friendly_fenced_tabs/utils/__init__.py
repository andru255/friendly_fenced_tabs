#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Miscelaneous functions
"""
import os

class Utils(object):
    @staticmethod
    def get_str_from_content(file_path, base_path=''):
        pwd = Utils.get_current_path()
        if base_path:
            pwd = base_path
        file_path = os.path.join(pwd, file_path)
        file_self = open(file_path)
        str_content = file_self.read()
        file_self.close()
        return str_content

    @staticmethod
    def get_current_path():
        current_path = os.getcwd()
        return current_path

    @staticmethod
    def get_value_by_key_name(dict_options, key_name):
        result = ""
        for option in dict_options:
            if option['key_name'] == key_name:
                result = option['value']
        return result
