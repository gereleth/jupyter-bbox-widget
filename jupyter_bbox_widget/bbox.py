#!/usr/bin/env python
# coding: utf-8

# Copyright (c) gereleth.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Integer, List, Unicode, Bool
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
    view_only: boolean
        Show image and annotations in view only mode, without bbox interactions.
        default: False
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
    selected_index = Integer(-1).tag(sync=True)
    view_only = Bool(False).tag(sync=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_msg(self._handle_custom_msg)
        self.submit_callback = None
        self.skip_callback = None
        self._attached_widgets = {}
        self.observe(self._handle_select, names=['selected_index'])


    def on_submit(self, function):
        """Specify a function that will be called when the user presses Submit button

        The function will be called with no arguments.
        """
        self.submit_callback = function


    def on_skip(self, function):
        """Specify a function that will be called when the user presses Skip button

        The function will be called with no arguments.
        """
        self.skip_callback = function


    def _handle_custom_msg(self, content, buffers):
        if content['type'] == 'submit':
            if self.submit_callback:
                self.submit_callback()
        elif content['type'] == 'skip':
            if self.skip_callback:
                self.skip_callback()


    def attach(self, widget, name=None, default_value=None):
        """ Attach another widget to record additional bbox properties

        Assume bbox is the currently selected bbox.
        The attached widget's value will be set to bbox[name].
        When the attached widget's value is changed then the new value will
        be saved in bbox[name].
        When no bbox is selected then the attached widget will be disabled.

        Parameters:

        widget: ipywidgets widget
            any widget like a slider, a text field, a checkbox and so on
        name: str or None
            name of the property associated with this widget. 
            If None then will be taken from `widget.description`.
        default_value: any valid widget value or None
            default property value to set on bboxes that don't have it yet.
            If None then will be taken from `widget.value`.
        """
        if default_value is None:
            default_value = widget.value
        if name is None:
            name = widget.description
        self._attached_widgets[name] = (widget, default_value)
        def handle_change(change):
            value = change['new']
            if self.selected_index != -1:
                self._set_bbox_property(
                    self.selected_index, 
                    name, 
                    value
                )
        widget.observe(handle_change, names=['value'])
        # make attached widget consistent with current selected_index
        self._handle_select({'new': self.selected_index})


    def _handle_select(self, change):
        """Handle selected bbox change.

        Set values corresponding to the selected bbox on attached widgets.        
        """
        index = change['new']
        if index == -1:
            # no bbox selected, disable widgets
            for _, (widget, default_value) in self._attached_widgets.items():
                widget.value = default_value
                widget.disabled = True
        else:
            # bbox at index is selected
            for name, (widget, default_value) in self._attached_widgets.items():
                widget.disabled = False
                value = self.bboxes[index].get(name, None)
                if value is None:
                    self._set_bbox_property(index, name, default_value)
                    value = default_value
                widget.value = value


    def _set_bbox_property(self, index, name, value):
        """Set property name of bbox at index to value
        """
        # editing bboxes in place doesn't get changes synced to js
        # enter this trick that seems to do the job
        ls = [{**bbox} for bbox in self.bboxes]
        ls[index][name] = value
        self.bboxes = ls