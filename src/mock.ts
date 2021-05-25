import type { DOMWidgetModel } from '@jupyter-widgets/base';
import App from './App.svelte';

class MockModel {
  set() {}
  undo() {}
  on(variableName: string, callback: () => void, context: any) {}
  save_changes() {}
}

const app = new App({
  target: document.body,
  props: {
    model: (new MockModel() as unknown) as DOMWidgetModel,
  },
});

export default app;
