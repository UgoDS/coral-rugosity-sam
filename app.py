import os

import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

from utils.image_utils import load_image
from utils.io_utils import save_uploaded_file
from utils.mask_utils import find_contour_from_mask
from utils.metric_utils import (
    compute_mean_absolute_error,
    compute_rugosity,
    get_line_from_left_to_right,
)
from utils.plot_utils import get_ellipse_coords, plot_masks, plot_rugosity_results
from utils.sam_utils import find_best_background_mask, load_predictor
from utils.st_utils import init_session_state

# Page Parameters
dict_keys = {
    "points": [],
    "img_cv": [],
    "mask": [],
    "score": None,
    "mae": None,
    "rugosity_pixels": None,
}


def clear_cache():
    for k, v in dict_keys.items():
        del sts[k]


st.set_page_config(page_title="rugosity", layout="wide")
sts = st.session_state


st.title("Rugosity Estimator")

# Session State
init_session_state(dict_keys)
if "predictor" not in sts:
    with st.spinner("Load predictor"):
        sts["predictor"] = load_predictor()


st.header("Load your image")
uploaded_file = st.file_uploader("Upload an image", on_change=clear_cache)
if uploaded_file is not None:
    uploaded_file_name = save_uploaded_file(uploaded_file)
    st.success("Saved File:{} to images".format(uploaded_file_name))

    image_path = f"{uploaded_file.name}_rugosity.png"
    file_path = os.path.join("images", uploaded_file.name)

    with Image.open(file_path) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size

    if sts["img_cv"] == []:
        sts["img_cv"] = load_image(file_path)

    # Draw an ellipse at each coordinate in points
    for point in sts["points"]:
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="red")
    st.success(
        "Click on the image to select background. Try with one point and add other if necessarly."
    )
    with st.spinner("Update image"):
        value = streamlit_image_coordinates(
            img, key="pil", height=int(h / 2), width=int(w / 2)
        )

    if value is not None:
        point = value["x"] * 2, value["y"] * 2

        if point not in sts["points"]:
            sts["points"].append(point)
            st.rerun()

    st.success(f"You marked {len(st.session_state['points'])} points")

with st.form("Rugosity calculation"):
    st.header("Rugosity calculation")
    button_rugosity = st.form_submit_button("Launch rugosity calculations")

if button_rugosity:
    sts["mask"], sts["score"] = find_best_background_mask(
        sts["predictor"], sts["img_cv"], list_points=sts["points"]
    )
    st.pyplot(
        plot_masks(sts["img_cv"], sts["mask"], sts["score"], sts["points"]),
        use_container_width=False,
    )
    line_sam = find_contour_from_mask(sts["mask"])
    line_meter = get_line_from_left_to_right(sts["mask"], line_sam)

    sts["mae"] = compute_mean_absolute_error(line_meter, line_sam)
    sts["rugosity_pixels"] = compute_rugosity(sts["mask"], line_sam)
    final_image = plot_rugosity_results(
        sts["img_cv"], line_meter, line_sam, sts["rugosity_pixels"], sts["mae"]
    )
    st.pyplot(final_image, use_container_width=False)
    plt.savefig(image_path)


if st.session_state["mae"]:
    with open(image_path, "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name=f"{uploaded_file.name}_rugosity.png",
            mime="image/png",
        )
        btn_results = st.download_button(
            "Download results",
            data=f"{uploaded_file.name};MAE_{st.session_state['mae']};Rugosity_{st.session_state['rugosity_pixels']}",
            file_name="test.txt",
        )
