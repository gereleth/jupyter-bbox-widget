#!/usr/bin/env python
# coding: utf-8

# Copyright (c) gereleth.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import List, Unicode
from ._frontend import module_name, module_version


class BBoxWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('BBoxModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('BBoxView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    image = Unicode('').tag(sync=True)
    classes = List(Unicode).tag(sync=True)
    colors = List(Unicode, [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
      ]).tag(sync=True)
    bboxes = List().tag(sync=True)
