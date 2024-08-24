[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gereleth/jupyter-bbox-widget/HEAD?filepath=examples%2Fintroduction.ipynb&urlpath=tree%2Fexamples%2Fintroduction.ipynb)

# jupyter\_bbox\_widget

A Jupyter widget for annotating images with bounding boxes. **See a [live demo on Binder](https://mybinder.org/v2/gh/gereleth/jupyter-bbox-widget/HEAD?filepath=examples%2Fintroduction.ipynb&urlpath=tree%2Fexamples%2Fintroduction.ipynb).**

```python
from jupyter_bbox_widget import BBoxWidget
widget = BBoxWidget(
    image='fruit.jpg',
    classes=['apple', 'orange', 'pear'],
)
widget
```

![UI example](https://raw.githubusercontent.com/gereleth/jupyter-bbox-widget/main/examples/ui_example.jpg)

Create, edit, move, resize and delete bounding box annotations using the mouse.

Use `widget.bboxes` to get current annotations values:

```python
widget.bboxes
# [{'x': 377, 'y': 177, 'width': 181, 'height': 201, 'label': 'apple'},
#  {'x': 219, 'y': 142, 'width': 169, 'height': 171, 'label': 'orange'},
#  {'x': 43,  'y': 174, 'width': 234, 'height': 195, 'label': 'pear'}]
```

You can also assign to `widget.bboxes` to display any annotations. For example, use the output of an object detection model to do model-assisted labeling.

```python
widget.bboxes = [
    {'x': 377, 'y': 177, 'width': 181, 'height': 201, 'label': 'apple'},
    {'x': 219, 'y': 142, 'width': 169, 'height': 171, 'label': 'orange'},
    {'x': 43,  'y': 174, 'width': 234, 'height': 195, 'label': 'pear'}
]
```

*Fruit photo by <a href="https://unsplash.com/@umanoide?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Umanoide</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>*
  
## Installation

You can install using `pip`:

```bash
pip install jupyter_bbox_widget
```

A Jupyter server restart may be necessary for the widget to be properly discovered.

## Usage

### Create and edit annotations with the mouse

- click and drag to create a bbox
- click and drag corners or edges to resize a bbox
- click and drag inside a bbox to move it
- in order to change a label select a new label below the image and click on label text

### Keyboard shortcuts

When you click inside the widget area it will gain focus and start receiving keyboard events. An outline usually indicates that the element is focused. Normal Jupyter keyboard shortcuts won't work in this state. To unfocus the widget area click outside it or press `Esc`.

Some shortcuts act on the selected bbox. New bboxes are selected automatically when created. You can also select a bbox by clicking on it. Selected bbox is displayed on top of others and with a thicker border.

- Digit keys 1-9 and 0 select a class label.
- `Esc` unfocuses the widget
- `Enter` is the same as pressing Submit button
- `Space` is the same as pressing Skip button
- `Tab` / `Shift-Tab` select next/previous bbox.
- Keys acting on the selected bbox (assuming a QWERTY keyboard, other layouts should use any keys in the same locations):
    - `W` move up
    - `A` move left
    - `S` move down
    - `D` move right
    - `Q` shrink width
    - `E` grow width
    - `R` grow height
    - `F` shrink height
    - `C` assign selected class label
    - Holding `Shift` while pressing movement keys will increase step size

### Skip and Submit events

You can define functions that will be called automatically when you press Skip or Submit buttons. This is useful for creating a workflow for annotating multiple images. 

```python
@widget.on_skip
def skip():
    # move on to the next image

@widget.on_submit
def save():
    # do stuff to save current annotations and move on
```

There is an example of a simple annotation workflow in [`examples/introduction.ipynb`](https://github.com/gereleth/jupyter-bbox-widget/blob/main/examples/introduction.ipynb) notebook.

### Widget traits

Get or set widget state by using these traits.

- `image` - path to a local image file or a web link
- `bboxes` - list of bounding boxes
- `classes` - list of class labels
- `colors` - list of colors to use for different classes
- `label` - currently selected class label
- `selected_index` - index of currently selected bbox. Is `-1` when nothing is selected.
- `hide_buttons` - default False, remove Skip and Submit buttons
- `view_only` - default False, make bboxes non-editable. This is useful for viewing annotation outputs without accidentally changing them.
- `image_bytes` - binary data from the image file

It's also possible to react to state changes by using the widget's [`observe`](https://ipywidgets.readthedocs.io/en/8.1.5/examples/Widget%20Events.html#registering-callbacks-to-trait-changes-in-the-kernel) method. For example, the following code will make the function `on_bbox_change` run every time the user edits bounding boxes:

```python
def on_bbox_change(change):
    new_bboxes = change['new']
    # do whatever with them

widget.observe(on_bbox_change, names=['bboxes'])
```

### Displaying special images

Maybe your images aren't files in a common format or require special handling to load. One way to show them is to save the image into an in-memory bytes buffer and feed that to `widget.image_bytes`. I'm open to suggestions on how to make this more user-friendly.

```python
from io import BytesIO
bytes_io = BytesIO()
# for example, say img is a PIL image
img.save(bytes_io, format='png')
# feed that data to the widget
widget.image_bytes = bytes_io.getvalue()
```

### Recording additional data

Sometimes you need to record more info about an object than just a location and a class label. For example, you might want to specify whether the object is in focus or blurred, record its size or other properties.

Let's say we want to apply a rating on a scale from 1 to 5 to every object in the image. We create a slider widget to edit the rating values:

```python
w_rating = widgets.IntSlider(value=3, min=1, max=5, description='Rating')
```

And we attach it to the bbox widget.

```python
widget.attach(w_rating, name='rating')
```

As a result all bboxes created afterwards will have a `rating` property and the `w_rating` widget can be used to display and manipulate the rating of the currently selected bbox.

Any number and any kind of `ipywidgets` widgets may be used in this way for creating richer annotations - number inputs, text inputs, checkboxes and so on (see [widget list](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html)). 

The notebook in [`examples/introduction.ipynb`](https://github.com/gereleth/jupyter-bbox-widget/blob/main/examples/introduction.ipynb) has an example and a more detailed explanation of this feature.

## Changelog

- v0.6.0
    - rewritten to use [`anywidget`](https://github.com/manzt/anywidget) under the hood
    - improved the way images are sent to frontend - it's no longer necessary to base64-encode local files in order to show them in Jupyter lab
- v0.5.0 
    - enabled use of `widget.on_skip` and `widget.on_submit` methods as decorators
- v0.4.0
    - exposed selected class label to the python side as `widget.label`
- v0.3.4
    - set max-width: 100% on image so that it respects layout
- v0.3.3
    - fixed bboxes not updating after class change by keyboard shortcut
- v0.3.2
    - added `hide_buttons` option
    - fixed bbox delete icon not displayed properly
- v0.3.1
    - unselect a bbox on click outside in view only mode
    - fixed a bug with overwriting attached properties on unselect
- v0.3.0
    - added `view_only` mode
- v0.2.0
    - added Skip and Submit buttons
    - added attach widget functionality for recording extra properties
    - multiple fixes and improvements
- v0.1.0
    - initial release


## Development Installation

This project was originally inspired by a blogpost [Creating Reactive Jupyter Widgets With Svelte](https://cabreraalex.medium.com/creating-reactive-jupyter-widgets-with-svelte-ef2fb580c05) but is currently based on [`anywidget`](https://github.com/manzt/anywidget) which provides a very nice developer experience.

Follow the steps below to make changes to this widget.

1. Clone the repo, cd into its folder
2. Activate the python environment you will use
3. Install the python package with dev dependencies `pip install -e .[dev]`
4. Run `npm install` to install JS dependencies.
5. Run `npm run dev` to launch vite dev server. It will watch for any changes you make to the files in `svelte` folder.
6. In `src/jupyter_bbox_widget/bbox.py` change the `DEV` variable to `True` so that the widget gets its JS code from the vite dev server.
7. Launch jupyter lab with `ANYWIDGET_HMR=1 jupyter lab` to turn on anywidget's hot module reloading.
8. Open a notebook with the widget and have fun making changes - you should see them in the UI as soon as you save a file.
9. Run `hatch build` to build your widget when it's ready.