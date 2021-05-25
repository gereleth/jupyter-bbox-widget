<script lang="ts">
  export let model;

  // Creates a Svelte store (https://svelte.dev/tutorial/writable-stores) that syncs with the named Traitlet in widget.ts and example.py.
  import { createValue } from './stores';
  let value = createValue(model, 'value', 0);
</script>

<style>
  h1 {
    color: purple;
  }
</style>

<h1>The value is: {$value}</h1>
<button on:click={() => value.update((d) => d + 1)}>update val</button>
<br />
