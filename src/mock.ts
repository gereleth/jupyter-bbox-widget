import type { DOMWidgetModel } from '@jupyter-widgets/base';
import BBoxWidget from './BBoxWidget.svelte';

class MockModel {
  set() {}
  undo() {}
  on(variableName: string, callback: () => void, context: any) {}
  save_changes() {}
  get(name: string) {
    if (name === 'image') {
      return 'https://images.unsplash.com/photo-1612200538165-26e793ae757f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1867&q=80';
    } else if (name === 'classes') {
      return ['apple', 'orange', 'pear'];
    }
    return undefined;
  }
}

const app = new BBoxWidget({
  target: document.body,
  props: {
    model: (new MockModel() as unknown) as DOMWidgetModel,
  },
});

export default app;
