<script>
  import { createEventDispatcher, onMount } from "svelte";

  export let width = 0;
  export let height = 0;
  export let x = 0;
  export let y = 0;
  export let label = "";
  export let colors = ["red"];
  export let classes = [];
  // export let strokeWidth = 2
  export let opacity = 0;
  export let toImageCoordinates;
  export let scaleX = 1;
  export let scaleY = 1;
  export let isActive = false;
  export let view_only = false;

  const dispatch = createEventDispatcher();

  let movingX0 = 0;
  let movingY0 = 0;
  let startX = 0;
  let startY = 0;
  let resizeX = false;
  let resizeY = false;
  let color = "rgb(255,64,64)";

  /**
   * Start moving a bbox
   * @param {MouseEvent} event
   */
  function startMoving(event) {
    if (event.button !== 0) {
      return;
    }
    event.stopPropagation();
    movingX0 = event.clientX;
    movingY0 = event.clientY;
    startX = x;
    startY = y;
    dispatch("move", view_only ? null : move);
  }

  /**
   * Move a bbox
   * @param {MouseEvent} event
   */
  function move(event) {
    event.stopPropagation();
    event.preventDefault();
    const dx = (event.clientX - movingX0) / scaleX;
    const dy = (event.clientY - movingY0) / scaleY;
    x = Math.round(startX + dx);
    y = Math.round(startY + dy);
  }
  /**
   * Start resizing a bbox
   * @param {MouseEvent} event
   * @param {String} edge - which edge was grabbed
   */
  function startResizing(event, edge) {
    if (event.button !== 0) {
      return;
    }
    event.stopPropagation();
    resizeX = false;
    resizeY = false;
    if (edge.includes("top")) {
      resizeY = true;
      startY = y + height;
    } else if (edge.includes("bottom")) {
      resizeY = true;
      startY = y;
    }
    if (edge.includes("left")) {
      resizeX = true;
      startX = x + width;
    } else if (edge.includes("right")) {
      resizeX = true;
      startX = x;
    }
    dispatch("move", resize);
  }
  /**
   * Resize a bbox
   * @param {MouseEvent} event
   */
  function resize(event) {
    event.stopPropagation();
    event.preventDefault();
    const imc = toImageCoordinates(event);
    const xm = Math.round(imc.x);
    const ym = Math.round(imc.y);
    if (resizeX) {
      x = Math.min(startX, xm);
      width = Math.max(startX, xm) - x;
    }
    if (resizeY) {
      y = Math.min(startY, ym);
      height = Math.max(startY, ym) - y;
    }
  }
  /**
   * Delete a bbox
   * @param {MouseEvent} event
   */
  function remove(event) {
    if (event.button !== 0) {
      return;
    }
    event.stopPropagation();
    dispatch("remove");
  }
  /**
   * Change bbox label
   * @param {MouseEvent} event
   */
  function relabel(event) {
    if (view_only) {
      return;
    }
    if (event.button !== 0) {
      return;
    }
    event.stopPropagation();
    dispatch("label");
  }

  onMount(() => {
    startX = x;
    startY = y;
    movingX0 = x;
    movingY0 = y;
    resizeX = true;
    resizeY = true;
    dispatch("create", resize);
  });

  $: color = colors[Math.max(0, classes.indexOf(label) % colors.length)];
</script>

<text filter="url(#bg-text)" fill="black" x={x * scaleX} y={y * scaleY - 4}
  >{label}</text
>
<text
  x={x * scaleX}
  y={y * scaleY - 4}
  fill="#333"
  on:mousedown={relabel}
  class:clickable={!view_only}
>
  {label}
</text>
<rect
  width={width * scaleX}
  height={height * scaleY}
  class:movable={!view_only}
  style="fill-opacity:{opacity};stroke-width:{isActive ? 3 : 2};stroke:{color};"
  shape-rendering="crispEdges"
  x={x * scaleX}
  y={y * scaleY}
  on:mousedown={startMoving}
/>
{#if !view_only}
  <line
    x1={x * scaleX}
    y1={y * scaleY}
    x2={(x + width) * scaleX}
    y2={y * scaleY}
    style="stroke-width:10px;stroke:black;stroke-opacity:0"
    class="top"
    on:mousedown={(e) => startResizing(e, "top")}
  />
  <line
    x1={x * scaleX}
    y1={(y + height) * scaleY}
    x2={(x + width) * scaleX}
    y2={(y + height) * scaleY}
    style="stroke-width:10px;stroke:black;stroke-opacity:0"
    class="bottom"
    on:mousedown={(e) => startResizing(e, "bottom")}
  />
  <line
    x1={x * scaleX}
    y1={y * scaleY}
    x2={x * scaleX}
    y2={(y + height) * scaleY}
    style="stroke-width:10px;stroke:black;stroke-opacity:0"
    class="left"
    on:mousedown={(e) => startResizing(e, "left")}
  />
  <line
    x1={(x + width) * scaleX}
    y1={y * scaleY}
    x2={(x + width) * scaleX}
    y2={(y + height) * scaleY}
    style="stroke-width:10px;stroke:black;stroke-opacity:0"
    class="right"
    on:mousedown={(e) => startResizing(e, "right")}
  />
  <circle
    cx={x * scaleX}
    cy={y * scaleY}
    r={6}
    fill-opacity="0"
    class="top-left"
    on:mousedown={(e) => startResizing(e, "top-left")}
  />
  <circle
    cx={(x + width) * scaleX}
    cy={y * scaleY}
    r={6}
    fill-opacity="0"
    class="top-right"
    on:mousedown={(e) => startResizing(e, "top-right")}
  />
  <circle
    cx={x * scaleX}
    cy={(y + height) * scaleY}
    r={6}
    fill-opacity="0"
    class="bottom-left"
    on:mousedown={(e) => startResizing(e, "bottom-left")}
  />
  <circle
    cx={(x + width) * scaleX}
    cy={(y + height) * scaleY}
    r={6}
    fill-opacity="0"
    class="bottom-right"
    on:mousedown={(e) => startResizing(e, "bottom-right")}
  />
  <!--Close icon-->
  <line
    x1={(x + width) * scaleX - 10}
    x2={(x + width) * scaleX}
    y1={y * scaleY - 13}
    y2={y * scaleY - 3}
    style="stroke-width:2;stroke:{color};"
  />
  <line
    x1={(x + width) * scaleX - 10}
    x2={(x + width) * scaleX}
    y1={y * scaleY - 3}
    y2={y * scaleY - 13}
    style="stroke-width:2;stroke:{color};"
  />
  <rect
    width="12"
    height="12"
    class="clickable"
    style="stroke-width:0;fill-opacity:0;"
    x={(x + width) * scaleX - 11}
    y={y * scaleY - 14}
    on:mousedown={remove}
  />
{/if}

<style>
  rect.movable {
    cursor: move;
  }
  .top,
  .bottom {
    cursor: row-resize;
  }
  .left,
  .right {
    cursor: col-resize;
  }
  .clickable {
    cursor: pointer;
  }
  .top-left {
    cursor: nw-resize;
  }
  .top-right {
    cursor: ne-resize;
  }
  .bottom-left {
    cursor: sw-resize;
  }
  .bottom-right {
    cursor: se-resize;
  }
</style>
