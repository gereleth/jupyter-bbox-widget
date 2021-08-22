<script lang="ts">
  import BBox from './BBox.svelte';
  import Button from './Button.svelte';
  import { createValue } from './stores';
  import { fade } from 'svelte/transition';
  import type { Writable } from 'svelte/store';
  import type { BBoxModel } from './widget';

  export let model:BBoxModel;
  let wrapperDiv:HTMLDivElement
  let img:HTMLImageElement
  let imgHeight = 0
  let imgWidth = 0
  let naturalHeight = 0
  let naturalWidth = 0
  let showSVG = false
  let sortedBBoxes:TBBox[] = []
  let sortedIndexToOriginal:number[] = []
  let label = ''
  let moveFn = null
  let createdFromUI = false
  let moveDirections = new Set()

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
  let selected_index:Writable<number> = createValue(model, 'selected_index', -1)
  let view_only:Writable<boolean> = createValue(model, 'view_only', false)

  function getImageCoordinates(event: MouseEvent) {
    const rect = img.getBoundingClientRect()
    const x = (event.clientX - rect.left)*naturalWidth/imgWidth;
    const y = (event.clientY - rect.top)*naturalHeight/imgHeight;
    return { x: x, y: y }
  }

  function initSVG() {
    showSVG = true
    naturalWidth = img.naturalWidth
    naturalHeight = img.naturalHeight
    // Sometimes after rerunning a cell that outputs the widget
    // imgHeight and imgWidth are set to zero
    // And the svg is not displayed (has 0 size)
    // Don't know why bind:clientWidth works the first time
    // but not the second
    // Setting width and height here seems to work around this issue
    const rect = img.getBoundingClientRect()
    imgHeight = rect.height
    imgWidth = rect.width
  }

  function handleMouseDown(event: MouseEvent) {
    if (event.button!==0) {return}
    if ($view_only) {
      $selected_index = -1
      return
    }
    const {x, y} = getImageCoordinates(event)
    const bbox = {
      x: Math.round(x), y:Math.round(y), 
      width:0, height:0, label:label
    }
    createdFromUI = true
    $bboxes = [...$bboxes, bbox]
    $selected_index = $bboxes.length - 1
  }

  function handleMouseUp(event: MouseEvent) {
    if (event.button!==0) {return}
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
    // Use a workaround from 
    // https://github.com/jupyter-widgets/ipywidgets/issues/2916
    model.unset('bboxes', {silent:true})
    model.set('bboxes', $bboxes)
    model.save_changes()
  }

  function remove(b:TBBox):void {
    const index = $bboxes.indexOf(b)
    if ($selected_index>index) {
      $selected_index -= 1
    }
    if ($selected_index==$bboxes.length-1) {
      $selected_index = -1
    }
    $bboxes = $bboxes.filter(x=>x!==b)
  }

  function onCreateBBox(event: CustomEvent) {
    if (createdFromUI) {
      moveFn = event.detail
      createdFromUI = false
    }
  }


  const keyMapping = new Map([
    ['KeyW', 'up'],
    ['KeyA', 'left'],
    ['KeyS', 'down'],
    ['KeyD', 'right'],
    ['KeyQ', 'shrink-width'],
    ['KeyE', 'grow-width'],
    ['KeyR', 'grow-height'],
    ['KeyF', 'shrink-height'],
  ])

  function handleKeyDown(event: KeyboardEvent) {
    event.stopPropagation()
    event.preventDefault()
    if (event.code.startsWith('Digit')||/Numpad\d/.test(event.code)) {
      let num = Number(event.code.slice(-1))
      if (num===0) {num = 10}
      num -= 1
      if (num < $classes.length) {
        label = $classes[num]
      }
    } else if (event.code==="Escape") {
      wrapperDiv.blur()
    } else if (event.code==="Tab") {
      const delta = event.shiftKey ? -1 : 1
      $selected_index += delta
      if ($selected_index>=$bboxes.length) {
        $selected_index = -1
      } else if ($selected_index===-2) {
        $selected_index = $bboxes.length -1
      }
    } else if (event.code==="Space") {
      skip()
    } else if ((event.code==="Enter")||(event.code==="NumpadEnter")) {
      submit()
    }
    if (($selected_index>=0)&&(!$view_only)) {
      let direction = keyMapping.get(event.code)
      if (direction) {
        moveDirections.add(direction)
      }
      if (event.code==="Delete") {
        remove($bboxes[$selected_index])
      }
      if (event.code==="KeyC") {
        $bboxes[$selected_index].label = label
      }
      let delta = event.shiftKey ? 10 : 1
      let dx = 0
      let dy = 0
      let dw = 0
      let dh = 0
      for (let direction of moveDirections) {
        if (direction==='up') {dy -= delta}
        else if (direction==='down') {dy += delta}
        else if (direction==='right') {dx += delta}
        else if (direction==='left') {dx -= delta}
        else if (direction==='shrink-width') {dw -= 2*delta; dx += delta}
        else if (direction==='grow-width') {dw += 2*delta; dx -= delta}
        else if (direction==='shrink-height') {dh -= 2*delta; dy += delta}
        else if (direction==='grow-height') {dh += 2*delta; dy -= delta}
      }
      if ((dx!==0)||(dy!==0)||(dw!==0)||(dh!==0)) {
        $bboxes[$selected_index].x += dx
        $bboxes[$selected_index].y += dy
        $bboxes[$selected_index].width += dw
        $bboxes[$selected_index].height += dh
        updateBBoxes()
      }
    }
  }

  function skip() {
    model.send({type:'skip'}, {})
    wrapperDiv.focus()
  }
  function submit() {
    model.send({type:'submit'}, {})
    wrapperDiv.focus()
  }
  // choose first class as label when classes change
  $: label = $classes.length>0 ? $classes[0] : ''

  // When a bbox is active it should be drawn on top of others
  // So it has to be the last one in svg
  $: sortedBBoxes = $selected_index===-1 ? $bboxes : [
      ...$bboxes.filter((bbox, index) => index!==$selected_index), 
      $bboxes[$selected_index]
    ]
  function originalIndex(sortedIndex:number) : number {
    if ($selected_index===-1) {return sortedIndex}
    else if (sortedIndex===$bboxes.length-1) {return $selected_index}
    else if (sortedIndex<$selected_index) {return sortedIndex}
    else {return sortedIndex+1}
  }
  $: sortedIndexToOriginal = sortedBBoxes.map((_,i)=>originalIndex(i))
  
  // Guard against deletion of bboxes from the python side
  $: if ($selected_index >= $bboxes.length) {
      $selected_index = -1
    }
</script>

<div class="wrapper" 
  tabindex="0"
  bind:this={wrapperDiv}
  on:keydown={(e)=>handleKeyDown(e)}
  on:keyup={(e)=>moveDirections.delete(keyMapping.get(e.code))}
  on:blur={()=>moveDirections.clear()}
>
  <div class="buttons">
    <Button 
      text="Skip" 
      icon="arrow-right" 
      tooltip="Keyboard shortcut: Space"
      on:click={skip}
    />
    <Button 
      text="Submit" 
      icon="check" 
      style="success"
      tooltip="Keyboard shortcut: Enter"
      on:click={submit}
    />
  </div>
  <div class="image">
    <div class="image-measure"
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
        {#each sortedBBoxes as bbox, i (sortedIndexToOriginal[i])}
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
            isActive={sortedIndexToOriginal[i]===$selected_index}
            view_only={$view_only}
            on:remove={()=>remove(bbox)}
            on:move={(event)=>{moveFn=event.detail; $selected_index=sortedIndexToOriginal[i]}}
            on:create={onCreateBBox}
            on:label={()=>{bbox.label=label; updateBBoxes()}}
            />
          </g>
        {/each}
      </svg>
    {/if}
  </div>
  <div class="classes">
    <p>Classes:</p>
    {#each $classes as _class, i}
      <div
        class="class-label"
        style="color:{$colors[i%$colors.length]};border:{_class===label?1:0}px solid {$colors[i%$colors.length]}"
        on:click={()=>label=_class}
        >
        {_class}
        {#if i<=9}
          <span class="key">{ (i+1)%10 }</span>
        {/if}
      </div>
    {/each}
  </div>
</div>

<style>
  .wrapper {
    position: relative;
    margin: 1px;
    padding: 4px;
  }
  .image {
    position: relative;
  }
  .image-measure {
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
    display: inline-block
  }
  .classes {
    margin-bottom: 10px;
  }
  .buttons {
    margin-bottom: 10px;
  }
  span.key {
    border: 1px solid lightgray;
    color: gray;
    padding: 0px 3px;
    font-size: 80%;
    border-radius: 2px;
  }
</style>