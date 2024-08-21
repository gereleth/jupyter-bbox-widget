import "./app.css";
import BBoxWidget from "./BBoxWidget.svelte";

function render({ model, el }) {
  let widget = new BBoxWidget({ target: el, props: { model } });
  return () => widget.$destroy();
}

export default { render };
