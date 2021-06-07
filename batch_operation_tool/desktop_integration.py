#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:35:57 2018

@author: eric
"""


def add_start_menu_shortcut():

    from shortcutter import ShortCutter
    s = ShortCutter()
    s.create_menu_shortcut("BatchOperationToolUI")
    print('Menu shortcut created.')


if __name__ == '__main__':
    add_start_menu_shortcut()
