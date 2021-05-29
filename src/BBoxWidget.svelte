<script lang="ts">
  import BBox from './BBox.svelte';
  import { createValue } from './stores';
  import { fade } from 'svelte/transition';
  import type { Writable } from 'svelte/store';

  export let model;
  let img:HTMLImageElement
  let imgHeight = 0
  let imgWidth = 0
  let naturalHeight = 0
  let naturalWidth = 0
  let showSVG = false

  type TBBox = {
    x: number,
    y: number,
    width: number,
    height: number,
    label: string,
  }

  // Creates a Svelte store (https://svelte.dev/tutorial/writable-stores) 
  // that syncs with the named Traitlet in widget.ts and example.py.
  let image:Writable<string> = createValue(model, 'image', '')
  let classes:Writable<string[]> = createValue(model, 'classes', [''])
  let colors:Writable<string[]> = createValue(model, 'colors', [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
      ])
  let bboxes:Writable<TBBox[]> = createValue(model, 'bboxes', [])

  function getImageCoordinates(event: MouseEvent) {
    const rect = img.getBoundingClientRect()
    const x = (event.clientX - rect.left)*naturalWidth/imgWidth;
    const y = (event.clientY - rect.top)*naturalHeight/imgHeight;
    return { x: x, y: y }
  }

  let label = ''
  let moveFn = null
  let createdFromUI = false

  function initSVG() {
    showSVG = true
    naturalWidth = img.naturalWidth
    naturalHeight = img.naturalHeight
  }

  function handleMouseDown(event: MouseEvent) {
    event.preventDefault()
    const {x, y} = getImageCoordinates(event)
    const bbox = {
      x: Math.round(x), y:Math.round(y), 
      width:0, height:0, label:label
    }
    createdFromUI = true
    $bboxes = [...$bboxes, bbox]
  }

  function handleMouseUp(event: MouseEvent) {
    event.preventDefault()
    moveFn = null
    updateBBoxes()
  }

  function handleMouseMove(event: MouseEvent) {
    if (moveFn===null) {return}
    else {
      moveFn(event)
    }
  }
  function updateBBoxes() {
    // python value doesn't get updated unless length of array changes
    // don't know why
    // I add and remove a dummy bbox to transfer changes to python
    const dummy = {x:0,y:0,width:0,height:0,label:''}
    $bboxes = [...$bboxes, dummy]
    $bboxes = $bboxes.slice(0, -1)
  }
  function remove(b:TBBox):void {
    $bboxes = $bboxes.filter(x=>x!==b)
  }
  function onCreateRect(event: CustomEvent) {
    if (createdFromUI) {
      moveFn = event.detail
      createdFromUI = false
    }
  }
  // choose first class as label when classes change
  $: label = $classes.length>0 ? $classes[0] : ''
</script>

<div class="wrapper">
  <div class="image"
    bind:clientHeight={imgHeight}
    bind:clientWidth={imgWidth}
  >
    <img src="{$image}" 
      alt="annotate me" 
      bind:this={img}
      on:load={initSVG}
  />
  </div>
  {#if showSVG}
    <svg width="{imgWidth}" height="{imgHeight}"
      on:mousedown={handleMouseDown}
      on:mousemove={handleMouseMove}
      on:mouseup={handleMouseUp}
      >
      <defs>
        <filter x="0" y="0" width="1" height="1" id="bg-text">
          <feFlood flood-color="rgba(255,255,255,0.5)"/>
          <feComposite in="SourceGraphic" operator="xor" />
        </filter>
      </defs>
      {#each $bboxes as bbox, i}
      <g transition:fade={{duration:100}}>
        <BBox 
          bind:x={bbox.x} 
          bind:y={bbox.y} 
          bind:width={bbox.width} 
          bind:height={bbox.height} 
          bind:label={bbox.label}
          toImageCoordinates={getImageCoordinates}
          classes={$classes}
          colors={$colors}
          scaleX={imgWidth/naturalWidth}
          scaleY={imgHeight/naturalHeight}
          on:remove={()=>remove(bbox)}
          on:move={(event)=>moveFn=event.detail}
          on:create={onCreateRect}
          on:label={()=>{bbox.label=label; updateBBoxes()}}
          />
        </g>
      {/each}
    </svg>
  {/if}
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