#!/usr/bin/env python
# coding: utf-8

import re
import sys


_PLATFORM = sys.platform


class Platform(object):

    @staticmethod
    def detail():
        return _PLATFORM

    @staticmethod
    def is_win():
        return _PLATFORM.startswith('win')

    @staticmethod
    def is_linux():
        return _PLATFORM.startswith('linux')

    @staticmethod
    def is_mac():
        return _PLATFORM.startswith('darwin')
