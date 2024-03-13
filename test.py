import streamlit as st
from PIL import Image, ImageDraw

from st_image_coordinates import streamlit_image_coordinates
from utils.image_utils import load_image
from utils.plot_utils import get_ellipse_coords

st.set_page_config(
    page_title="Streamlit Image Coordinates: Image Update",
    page_icon="🎯",
    layout="wide",
)

# Display Parameters
REDUCTION_IMAGE_FACTOR = 3

if "points_background" not in st.session_state:
    st.session_state["points_background"] = []

if "points_fish" not in st.session_state:
    st.session_state["points_fish"] = []

if "img_cv" not in st.session_state:
    st.session_state["img_cv"] = None

if "object_type" not in st.session_state:
    st.session_state["object_type"] = "background"

FILE_PATH = "/Users/ugo/Documents/rugosity/images/Ti18m2010.02.JPG"

st.session_state["img_cv"] = load_image(FILE_PATH)


def callback_object_type(object_type):
    st.session_state.object_type = object_type


cols = st.columns(2)
button_background = cols[0].button(
    "Background", on_click=callback_object_type, args=["background"]
)
button_fish = cols[1].button("Fish", on_click=callback_object_type, args=["fish"])


# @st.cache_resource
def load_image_pil(file_path):
    with Image.open(file_path) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size
    return img, w, h, draw


img, w, h, draw = load_image_pil(FILE_PATH)


for point in st.session_state["points_background"]:
    coords = get_ellipse_coords(point)
    draw.ellipse(coords, fill="red")

for point in st.session_state["points_fish"]:
    coords = get_ellipse_coords(point)
    draw.ellipse(coords, fill="blue")


def st_annotation_module(REDUCTION_IMAGE_FACTOR, _img, w, h):
    return streamlit_image_coordinates(
        _img,
        key="local",
        height=int(h / REDUCTION_IMAGE_FACTOR),
        width=int(w / REDUCTION_IMAGE_FACTOR),
    )


value = st_annotation_module(REDUCTION_IMAGE_FACTOR, img, w, h)

if value is not None:
    point = (
                value["x"] * REDUCTION_IMAGE_FACTOR,
                value["y"] * REDUCTION_IMAGE_FACTOR,
            )
    if (
        point
        not in st.session_state["points_background"] + st.session_state["points_fish"]
    ):
        st.session_state[f"points_{st.session_state.object_type}"].append(point)
        st.rerun()

st.write(st.session_state["points_background"])
st.write(st.session_state["points_fish"])
