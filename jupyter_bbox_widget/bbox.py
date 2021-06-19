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
    """A widget for adding bounding box annotations to an image

    Parameters
    ----------
    image: string
        Path to the image file or image url.
    classes: list of string
        A list of classes.
    colors: list of string
        The colors to use for bounding boxes. 
        Default value is 10 colors from matplotlib.cm.Tab10 colormap.
    bboxes: list of dict
        Annotations to display in the widget.
        Expected keys for each annotation are `x`, `y`, `width`, `height` and `label`.
        Example annotation could look like this:
        `{'x': 100, 'y': 200, 'width': 100, 'height':200, 'label':'something'}`
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


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_msg(self._handle_custom_msg)
        self.submit_callback = None
        self.skip_callback = None


    def on_submit(self, function):
        self.submit_callback = function


    def on_skip(self, function):
        self.skip_callback = function


    def _handle_custom_msg(self, content, buffers):
        if content['type'] == 'submit':
            if self.submit_callback:
                self.submit_callback()
        elif content['type'] == 'skip':
            if self.skip_callback:
                self.skip_callback()