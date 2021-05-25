<script  lang="ts">
    import {createEventDispatcher, onMount} from 'svelte'
    
    export let width = 0
    export let height = 0
    export let x = 0
    export let y = 0
    export let label = ''
    export let colors:string[] = ['red']
    export let classes:string[] = []
    export let strokeWidth = 2
    export let opacity = 0
    export let toImageCoordinates

    const dispatch = createEventDispatcher()

    let movingX0 = 0
    let movingY0 = 0
    let startX = 0
    let startY = 0
    let resizeX = false
    let resizeY = false
    let color = 'rgb(255,64,64)'

function startMoving(event: MouseEvent) {
    event.stopPropagation()
    movingX0 = event.clientX
    movingY0 = event.clientY
    startX = x
    startY = y
    dispatch('moveFn', move)
}

export function move(event: MouseEvent) {
    const dx = event.clientX - movingX0
    const dy = event.clientY - movingY0
    x = startX + dx
    y = startY + dy
}

function startResizing(event: MouseEvent, edge:string) {
    event.stopPropagation()
    resizeX = false
    resizeY = false
    if (edge.includes("top")) {
        resizeY = true
        startY = y+height
    } else if (edge.includes("bottom")) {
        resizeY = true
        startY = y
    }
    if (edge.includes("left")) {
        resizeX = true
        startX = x+width
    } else if (edge.includes("right")) {
        resizeX = true
        startX = x
    }
    dispatch('moveFn', resize)
}

export function resize(event: MouseEvent) {
    const imc = toImageCoordinates(event)
    const xm = imc.x
    const ym = imc.y
    if (resizeX) {
        x = Math.min(startX, xm)
        width = Math.max(startX, xm) - x
    }
    if (resizeY) {
        y = Math.min(startY, ym)
        height = Math.max(startY, ym) - y
    }
}

function remove(event: MouseEvent) {
    event.stopPropagation()
    dispatch('remove')
}

function reclassify(event: MouseEvent) {
    event.stopPropagation()
    dispatch('class')
}

onMount(()=>{
    startX = x
    startY = y
    movingX0 = x
    movingY0 = y
    resizeX = true
    resizeY = true
    dispatch('create', resize)
})

$: color = colors[Math.max(0, classes.indexOf(label)%colors.length)]
</script>


<rect width="{width}" 
    height="{height}"
    style="fill-opacity:{opacity};stroke-width:{strokeWidth};stroke:{color};" 
    x={x}
    y={y}
    on:mousedown={startMoving}
    />
<line x1="{x}" y1="{y}" x2="{x+width}" y2="{y}" 
    style="stroke-width:10px;stroke:black;stroke-opacity:0" 
    class="top"
    on:mousedown={e=>startResizing(e, "top")}
    />
<line x1="{x}" y1="{y+height}" x2="{x+width}" y2="{y+height}" 
    style="stroke-width:10px;stroke:black;stroke-opacity:0" 
    class="bottom"
    on:mousedown={e=>startResizing(e, "bottom")}
    />
<line x1="{x}" y1="{y}" x2="{x}" y2="{y+height}" 
    style="stroke-width:10px;stroke:black;stroke-opacity:0" 
    class="left"
    on:mousedown={e=>startResizing(e, "left")}
    />
<line x1="{x+width}" y1="{y}" x2="{x+width}" y2="{y+height}" 
    style="stroke-width:10px;stroke:black;stroke-opacity:0" 
    class="right"
    on:mousedown={e=>startResizing(e, "right")}
    />
<circle cx={x} cy={y} r={6} fill-opacity="0"
    class="top-left"
    on:mousedown={e=>startResizing(e, "top-left")}
    />
<circle cx={x+width} cy={y} r={6} fill-opacity="0"
    class="top-right"
    on:mousedown={e=>startResizing(e, "top-right")}
    />
<circle cx={x} cy={y+height} r={6} fill-opacity="0"
    class="bottom-left"
    on:mousedown={e=>startResizing(e, "bottom-left")}
    />
<circle cx={x+width} cy={y+height} r={6} fill-opacity="0"
    class="bottom-right"
    on:mousedown={e=>startResizing(e, "bottom-right")}
    />
<text x="{x}" y="{y-4}" fill="{color}" on:mousedown={reclassify}>{label}</text>
<text x="{x+width-13}" y="{y-4}" fill="{color}" on:mousedown={remove}>🗙</text>

<style>
    rect {
        cursor: move;
    }
    .top, .bottom {
        cursor: row-resize;
    }
    .left, .right {
        cursor: col-resize;
    }
    text {
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