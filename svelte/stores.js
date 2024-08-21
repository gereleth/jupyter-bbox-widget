import { writable } from "svelte/store";

export function createValue(model, name_, value_) {
  const name = name_;
  // use value from python if it is set when creating widget
  const modelValue = model.get(name);
  const curVal = writable(modelValue === undefined ? value_ : modelValue);
  model.on("change:" + name, () => curVal.set(model.get(name)), null);

  return {
    set: (v) => {
      curVal.set(v);
      model.set(name, v);
      model.save_changes();
    },
    subscribe: curVal.subscribe,
    update: (func) => {
      curVal.update((v) => {
        let out = func(v);
        model.set(name, out);
        model.save_changes();
        return out;
      });
    },
  };
}
