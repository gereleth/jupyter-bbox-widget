#!/usr/bin/env python
# coding: utf-8

# Copyright (c) gereleth
# Distributed under the terms of the Modified BSD License.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'jupyter_bbox_widget',
        'require': 'jupyter_bbox_widget/extension'
    }]
