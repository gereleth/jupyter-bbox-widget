<script lang="ts">
  import Rectangle from './Rectangle.svelte';
  import { createValue } from './stores';
  import { tick } from 'svelte';
  import { fade } from 'svelte/transition';

  export let model;
  let img:HTMLImageElement
  let imgHeight = 0
  let imgWidth = 0

  // Creates a Svelte store (https://svelte.dev/tutorial/writable-stores) 
  // that syncs with the named Traitlet in widget.ts and example.py.
  let image = createValue(model, 'image', '')
  let classes = createValue(model, 'classes', [''])
  let colors = createValue(model, 'colors', [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
      ])
  let rects = createValue(model, 'bboxes', [])

  function getImageCoordinates(event: MouseEvent) {
    const rect = img.getBoundingClientRect()
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    }
  }

  let label = ''
  let moveFn = null
  let createdFromUI = false

  function handleMouseDown(event: MouseEvent) {
    event.preventDefault()
    const {x, y} = getImageCoordinates(event)
    const rect = {
      x: Math.round(x), y:Math.round(y), 
      width:0, height:0, label:label
    }
    createdFromUI = true
    $rects = [...$rects, rect]
  }

  function handleMouseUp(event: MouseEvent) {
    event.preventDefault()
    moveFn = null
    updateRects()
  }

  function handleMouseMove(event: MouseEvent) {
    if (moveFn===null) {return}
    else {
      moveFn(event)
    }
  }
  function updateRects() {
    // python value doesn't get updated unless length of array changes
    // don't know why
    // I add and remove a dummy bbox to transfer changes
    const dummy = {x:0,y:0,width:0,height:0,label:''}
    $rects = [...$rects, dummy]
    $rects = $rects.slice(0, -1)
  }
  function remove(r) {
    $rects = $rects.filter(x=>x!==r)
  }
  function onCreateRect(event) {
    if (createdFromUI) {
      moveFn = event.detail
      createdFromUI = false
    }
  }
  // choose first class as label when classes change
  $: label = $classes.length>0 ? $classes[0] : ''
  // clear bboxes when image changes
  // $: $image, $rects = [];
</script>

<div class="wrapper">
  <div class="image"
    bind:clientHeight={imgHeight}
    bind:clientWidth={imgWidth}
  >
    <img src="{$image}" 
      alt="annotate me" 
      bind:this={img}
  />
  </div>
  
  <svg width="{imgWidth}" height="{imgHeight}"
    on:mousedown={handleMouseDown}
    on:mousemove={handleMouseMove}
    on:mouseup={handleMouseUp}
    >
    {#each $rects as r, i}
    <g transition:fade={{duration:200}}>
      <Rectangle 
        bind:x={r.x} 
        bind:y={r.y} 
        bind:width={r.width} 
        bind:height={r.height} 
        bind:label={r.label}
        toImageCoordinates={getImageCoordinates}
        classes={$classes}
        colors={$colors}
        on:remove={()=>remove(r)}
        on:moveFn={(event)=>moveFn=event.detail}
        on:create={onCreateRect}
        on:class={()=>{r.label=label; updateRects()}}
        />
      </g>
    {/each}
  </svg>
  <div class="classes">
    <p>Classes:</p>
    {#each $classes as _class, i}
      <span
        class="class-label"
        style="color:{$colors[i%$colors.length]};border:{_class===label?1:0}px solid {$colors[i%$colors.length]}"
        on:click={()=>label=_class}
        >
        {_class}
      </span>
    {/each}
  </div>
</div>

<style>
  .wrapper {
    position: relative;
  }
  .image {
    display: table;
  }
  img {
    display: block;
  }
  svg {
    position: absolute;
    top: 0;
    left: 0;
  }
  .class-label {
    cursor: pointer;
    border-radius: 4px;
    padding: 4px;
    margin: 4px;
  }
  .classes {
    margin-bottom: 10px;
  }
</style>