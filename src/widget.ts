// Copyright (c) gereleth
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import BBoxWidget from './BBoxWidget.svelte';

export class BBoxModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: BBoxModel.model_name,
      _model_module: BBoxModel.model_module,
      _model_module_version: BBoxModel.model_module_version,
      _view_name: BBoxModel.view_name,
      _view_module: BBoxModel.view_module,
      _view_module_version: BBoxModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'BBoxModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'BBoxView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class BBoxView extends DOMWidgetView {
  render() {
    new BBoxWidget({
      target: this.el,
      props: {
        model: this.model,
      },
    });
  }
}
