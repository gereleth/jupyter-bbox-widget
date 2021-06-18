<script lang="ts">
  export let text = ''
  export let icon = ''
  export let style = ''
  export let tooltip = ''
</script>

<button 
    on:click 
    class="{style}"
    title="{tooltip}"
>
    <!-- Icons are there in ipywidgets, hopefully we can just use them here -->
    {#if icon!==''}
        <i class="fa fa-{icon}"></i>
    {/if}
    {text}
</button>

<style>
    button {
        display: inline-block;
        background-color: #eeeeee;
        width: 148px;
        height: 28px;
        line-height: 28px;
        font-size: 13px;
        padding: 0 10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: center;
        cursor: pointer;
        border: none;
        user-select: none;
    }
    button:hover {
        box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
    }
    button:active {
        background-color: #bdbdbd;
    }
    button.success {
        background-color: #4caf50;
        color: white;
    }
    button.success:active {
        background-color: #388e3c;
    }
</style>