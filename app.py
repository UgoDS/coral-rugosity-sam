import os
import sys
import subprocess

if not os.path.exists("sam_vit_b_01ec64.pth"):
    from urllib.request import urlretrieve

    url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
    urlretrieve(url, "sam_vit_b_01ec64.pth")


import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

from utils.image_utils import load_image
from utils.io_utils import create_zip_file, save_df_result, save_uploaded_file
from utils.mask_utils import find_contour_from_mask
from utils.metric_utils import (
    compute_mean_absolute_error,
    compute_rugosity,
    create_df_from_dict_result,
    get_line_from_left_to_right,
)
from utils.plot_utils import get_ellipse_coords, plot_rugosity_results
from utils.sam_utils import find_best_background_mask, load_predictor
from utils.st_utils import dl_button_zip, init_session_state


os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# Page Parameters
dict_keys = {
    "points": [],
    "img_cv": [],
    "mask": [],
    "score": None,
}
# Display Parameters
REDUCTION_IMAGE_FACTOR = 3


def clear_cache():
    for k, v in dict_keys.items():
        del sts[k]


st.set_page_config(page_title="rugosity", layout="wide")
sts = st.session_state
if "dict_result" not in sts:
    sts["dict_result"] = {}

if "idx_image" not in sts:
    sts["idx_image"] = 0


st.title("Rugosity Estimator")

# Session State
init_session_state(dict_keys)
if "predictor" not in sts:
    with st.spinner("Load predictor"):
        sts["predictor"] = load_predictor()


st.header("Load your images")
uploaded_files = st.file_uploader(
    "Several images might be loaded simultaneously",
    on_change=clear_cache,
    accept_multiple_files=True,
    type=[".JPG", ".jpeg", ".png"],
)
if uploaded_files != []:
    st.header("Annotate your image")
    uploaded_file = uploaded_files[sts["idx_image"]]
    uploaded_file_name = save_uploaded_file(uploaded_file)
    picture_name = f"{uploaded_file.name}"
    image_path = f"{picture_name}_rugosity.png"
    file_path = os.path.join("images", picture_name)

    with Image.open(file_path) as img:
        draw = ImageDraw.Draw(img)
        w, h = img.size

    if len(sts["img_cv"]) == 0:
        sts["img_cv"] = load_image(file_path)

    # Draw an ellipse at each coordinate in points
    for point in sts["points"]:
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="red")
    st.caption(
        "Click on the image to select background. Try with one point and add other if necessarly."
    )
    with st.spinner("Update image"):
        value = streamlit_image_coordinates(
            img,
            key=f"pil_{picture_name}",
            height=int(h / REDUCTION_IMAGE_FACTOR),
            width=int(w / REDUCTION_IMAGE_FACTOR),
        )

    if value is not None:
        point = value["x"] * REDUCTION_IMAGE_FACTOR, value["y"] * REDUCTION_IMAGE_FACTOR

        if point not in sts["points"]:
            sts["points"].append(point)
            st.rerun()

    if len(sts["points"]) > 0:
        with st.spinner(
            "Rugosity calculation (if using CPU, it can takes up to a minute...)"
        ):
            sts["mask"], sts["score"] = find_best_background_mask(
                sts["predictor"], sts["img_cv"], list_points=sts["points"]
            )
        line_sam = find_contour_from_mask(sts["mask"])
        line_meter = get_line_from_left_to_right(sts["mask"], line_sam)

        mae = compute_mean_absolute_error(line_meter, line_sam)
        rugosity_pixels, contour_len = compute_rugosity(sts["mask"], line_sam)
        final_image = plot_rugosity_results(
            sts["img_cv"], line_meter, line_sam, rugosity_pixels, mae
        )

        st.pyplot(final_image, use_container_width=True)
        plt.savefig(f"results/{image_path}")
        sts["dict_result"][picture_name] = [
            contour_len,
            len(line_meter),
            rugosity_pixels,
            mae,
            image_path,
        ]
        sts["idx_image"] += 1
        if sts["idx_image"] < len(uploaded_files):
            clear_cache()
            st.rerun()
        else:
            st.write(sts["dict_result"])
            df = create_df_from_dict_result(sts["dict_result"])
            save_df_result(df, "results/results.csv")
            create_zip_file("results", "results")
            dl_button_zip("results.zip")
            # clean_repo("results")
