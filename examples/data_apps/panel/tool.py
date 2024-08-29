from io import StringIO

import pandas as pd
import panel as pn
import param
from jupyter_bbox_widget import BBoxWidget

pn.extension("ipywidgets", "tabulator")

IMAGES = [
    "https://github.com/gereleth/jupyter-bbox-widget/blob/main/examples/fruit/fruit.jpg?raw=true",
    "https://github.com/gereleth/jupyter-bbox-widget/blob/main/examples/fruit/fruit2.jpg?raw=true",
    "https://github.com/gereleth/jupyter-bbox-widget/blob/main/examples/fruit/fruit3.jpg",
]


def get_next_image(current, images):
    """Returns the image following the current image in a list of images"""
    index = images.index(current)
    if index == len(images) - 1:
        index = 0
    else:
        index += 1
    return images[index]


class BBoxViewer(pn.viewable.Viewer):
    """A Panel component for viewing a list of bounding boxes"""

    data = param.List(allow_None=True, doc="The list of bounding boxes.")

    _dataframe = param.DataFrame(doc="The data as a dataframe.")

    @param.depends("data", watch=True, on_init=True)
    def _update_dataframe(self):
        self._dataframe = pd.DataFrame(self.data).sort_index(ascending=False)

    @param.depends("data")
    def _get_data_file(self):
        sio = StringIO()
        df = pd.DataFrame(self.data)
        df.to_csv(sio)
        sio.seek(0)
        return sio

    def __panel__(self):
        filedownload = pn.widgets.FileDownload(self._get_data_file, filename="bboxes.csv")
        table = pn.widgets.Tabulator(self.param._dataframe, disabled=True)
        is_data_not_empty = self.param.data.rx().rx.bool()
        return pn.Column(filedownload, table, visible=is_data_not_empty)


widget = BBoxWidget(
    image=IMAGES[0],
    classes=["apple", "orange", "pear"],
)

bbox_viewer = BBoxViewer()


@widget.on_skip
def skip_image():
    widget.image = get_next_image(widget.image, IMAGES)


@widget.on_submit
def save():
    print("save")
    if widget.selected_index >= 0:
        widget._set_bbox_property(widget.selected_index, "image", widget.image)
    bbox_viewer.data = widget.bboxes


pn.Row(widget, bbox_viewer).servable()
