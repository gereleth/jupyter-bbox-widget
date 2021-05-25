import type { DOMWidgetModel } from '@jupyter-widgets/base';
import BBoxWidget from './BBoxWidget.svelte';

class MockModel {
  set() {}
  undo() {}
  on(variableName: string, callback: () => void, context: any) {}
  save_changes() {}
}

const app = new BBoxWidget({
  target: document.body,
  props: {
    model: (new MockModel() as unknown) as DOMWidgetModel,
  },
});

export default app;
