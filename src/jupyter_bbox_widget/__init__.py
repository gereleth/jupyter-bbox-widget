import importlib.metadata
from .bbox import BBoxWidget

try:
    __version__ = importlib.metadata.version("jupyter_bbox_widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
