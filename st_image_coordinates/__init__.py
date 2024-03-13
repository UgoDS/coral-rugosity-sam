from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# Tell streamlit that there is a component called streamlit_image_coordinates,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_image_coordinates", path=str(frontend_dir)
)


# Create the python function that will be called
def streamlit_image_coordinates(
    source: str | Path | np.ndarray | object,
    height: int | None = None,
    width: int | None = None,
    key: str | None = None,
):
    """
    Take an image source and return the coordinates of the image clicked

    Parameters
    ----------
    source : str | Path | object
        The image source
    height : int | None
        The height of the image. If None, the height will be the original height
    width : int | None
        The width of the image. If None, the width will be the original width
    """

    if isinstance(source, Path) or isinstance(source, str):
        if not str(source).startswith("http"):
            content = Path(source).read_bytes()
            src = "data:image/png;base64," + base64.b64encode(content).decode("utf-8")
        else:
            src = str(source)
    elif hasattr(source, "save"):
        buffered = BytesIO()
        source.save(buffered, format="JPEG")  # type: ignore
        src = "data:image/jpg;base64,"
        src += base64.b64encode(buffered.getvalue()).decode("utf-8")  # type: ignore
        buffered.close()
    elif isinstance(source, np.ndarray):
        image = Image.fromarray(source)
        buffered = BytesIO()
        image.save(buffered, format="PNG")  # type: ignore
        src = "data:image/png;base64,"
        src += base64.b64encode(buffered.getvalue()).decode("utf-8")  # type: ignore
    else:
        raise ValueError(
            "Must pass a string, Path, numpy array or object with a save method"
        )

    component_value = _component_func(
        src=src,
        height=height,
        width=width,
        key=key,
    )

    return component_value
