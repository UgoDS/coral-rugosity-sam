import os

import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

from utils.image_utils import load_image
from utils.io_utils import create_zip_file, save_df_result, save_uploaded_file
from utils.mask_utils import find_contour_from_mask
from utils.metric_utils import (
    compute_similarities,
    create_df_from_dict_result,
    get_line_from_left_to_right,
)
from utils.plot_utils import get_ellipse_coords, plot_rugosity_results
from utils.sam_utils import find_best_background_mask, load_predictor
from utils.st_utils import dl_button_zip


os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# Display Parameters
REDUCTION_IMAGE_FACTOR = 3


st.set_page_config(page_title="rugosity", layout="wide")
sts = st.session_state
if "dict_result" not in sts:
    sts["dict_result"] = {}

if "dict_points" not in sts:
    sts["dict_points"] = {}

if "idx_image" not in sts:
    sts["idx_image"] = 0

if "annotation_is_done" not in sts:
    sts["annotation_is_done"] = False

if "calculation_is_done" not in sts:
    sts["calculation_is_done"] = False


st.title("Rugosity Estimator")

# Session State
if "predictor" not in sts:
    with st.spinner("Load predictor"):
        sts["predictor"] = load_predictor()


st.header("1. Load your images")
uploaded_files = st.file_uploader(
    "Several images might be loaded simultaneously",
    accept_multiple_files=True,
    type=[".JPG", ".jpeg", ".png"],
)
st.header("2. Annotate your images")
if uploaded_files == []:
    st.warning("You need to load images")
else:
    if uploaded_files != []:
        uploaded_file = uploaded_files[sts["idx_image"]]
        picture_name = f"{uploaded_file.name}"
        save_uploaded_file(uploaded_file)
        image_path = f"{picture_name}_rugosity.png"
        file_path = os.path.join("images", picture_name)
        if picture_name not in sts["dict_points"].keys():
            sts["dict_points"][picture_name] = []

        with Image.open(file_path) as img:
            draw = ImageDraw.Draw(img)
            w, h = img.size

        # Draw an ellipse at each coordinate in points
        for point in sts["dict_points"][picture_name]:
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="red")
        st.caption(
            f"""{picture_name} ({sts["idx_image"]}/{len(uploaded_files)})

            Click on the image to select background. Try with one point and add other if necessarly."""
        )
        with st.spinner("Update image"):
            value = streamlit_image_coordinates(
                img,
                key=f"pil_{picture_name}",
                height=int(h / REDUCTION_IMAGE_FACTOR),
                width=int(w / REDUCTION_IMAGE_FACTOR),
            )

        if value is not None:
            point = (
                value["x"] * REDUCTION_IMAGE_FACTOR,
                value["y"] * REDUCTION_IMAGE_FACTOR,
            )

            if point not in sts["dict_points"][picture_name]:
                sts["dict_points"][picture_name].append(point)
                st.rerun()

        button_validate = st.button("Validate Annotation")
        if button_validate:
            sts["idx_image"] += 1
            if sts["idx_image"] == len(uploaded_files):
                sts["annotation_is_done"] = True
                sts["idx_image"] = 0
            st.rerun()


st.header("3. Computation")
if sts["annotation_is_done"]:
    if st.button("Launch Rugosity Calculation"):
        st.caption(
            f"""It can take up to {len(uploaded_files)} minutes to compute if using cpu. 
                Meanwhile, check what is [Segment Anything Model](https://github.com/facebookresearch/segment-anything)"""
        )
        for idx, file_ in enumerate(uploaded_files):
            picture_name = file_.name
            with st.spinner(f"""{picture_name} ({idx}/{len(uploaded_files)})"""):
                file_path = os.path.join("images", picture_name)
                img_cv = load_image(file_path)
                points = sts["dict_points"][picture_name]
                mask, score = find_best_background_mask(
                    sts["predictor"], img_cv, list_points=points
                )
                line_sam = find_contour_from_mask(mask)
                line_meter = get_line_from_left_to_right(mask, line_sam)
                line_sam_simple = np.array([(x[0], x[1]) for x in line_sam[:, 0]])
                line_meter_simple = np.array(line_meter)

                similarities = compute_similarities(
                    line_meter_simple, line_sam_simple, line_meter
                )
                final_image = plot_rugosity_results(
                    img_cv, line_meter, line_sam, picture_name
                )

                st.pyplot(final_image, use_container_width=True)
                plt.savefig(f"results/{picture_name}")
                sts["dict_result"][picture_name] = [
                    similarities.contour_lenght,
                    len(line_meter),
                    similarities.rugosity_pixels,
                    similarities.mae,
                    similarities.pcm,
                    similarities.frechet_dist,
                    similarities.area_between_two_curves,
                    similarities.curve_length_measure_arc,
                    similarities.dtw,
                    points,
                ]
                df = create_df_from_dict_result(sts["dict_result"])
                st.write(df)
        sts["calculation_is_done"] = True
else:
    st.warning("You need to annotate images before running computation")
st.header("4. Save results")
if sts["calculation_is_done"]:
    df = create_df_from_dict_result(sts["dict_result"])
    save_df_result(df, "results/results.csv")
    create_zip_file("results", "results")
    dl_button_zip("results.zip")

    sts["idx_image"] = 0
    uploaded_files = []
    # clean_repo("results")
else:
    st.warning("You need to run computation before saving results")
