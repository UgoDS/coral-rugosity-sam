import numpy as np
import pandas as pd
import similaritymeasures

from utils.mask_utils import (
    find_contour_lenght,
    find_lowest_left_pixel,
    find_lowest_right_pixel,
    get_max_contour_x,
    get_min_contour_x,
)
from data_model.similarities import Similarities


def get_line_from_left_to_right(mask, contour):
    left_y = find_lowest_left_pixel(mask, contour)
    right_y = find_lowest_right_pixel(mask, contour)
    left_x = get_min_contour_x(contour)
    right_x = get_max_contour_x(contour)
    diff_pixel_y = right_y - left_y
    diff_pixel_x = right_x - left_x
    slope = diff_pixel_y / diff_pixel_x
    return [
        (x, int(left_y + slope * idx)) for idx, x in enumerate(range(left_x, right_x))
    ]


def compute_mean_absolute_error(line_meter, line_sam):
    n = len(line_meter)
    sum = 0
    for x_meter in range(n):
        x_meter, y_meter = line_meter[x_meter]
        for y_sam in np.where(line_sam[:, 0] == x_meter)[0]:
            sum += abs(line_sam[y_sam, 1] - y_meter)
    error = sum / len(line_sam)
    return error


def compute_rugosity(line_left_right_size, contour_lenght):
    return round(contour_lenght / line_left_right_size, 3)


def create_df_from_dict_result(dict_result):
    df = pd.DataFrame(
        columns=[
            "PictureName",
            "ContourLength(chain)",
            "LinearLength(tape)",
            "Rugosity(chain/tape)",
            "MeanAbsoluteError",
            "PCM",
            "FrechetDistance",
            "AreaBetweenTwoCurves",
            "CurveLengthArc",
            "DynamicTimeWraping",
            "PointsCoordinates",
        ]
    )
    for idx, (k, v) in enumerate(dict_result.items()):
        df.loc[idx, :] = [k] + v
    return df


def compute_similarities(exp_data, num_data, line_left_right):
    pcm = similaritymeasures.pcm(exp_data, num_data)

    # frechet_dist = similaritymeasures.frechet_dist(exp_data, num_data)
    # TOO SLOW

    # area_between_two_curves = similaritymeasures.area_between_two_curves(
    #     exp_data, num_data
    # )
    # TOO SLOW

    curve_length_measure = similaritymeasures.curve_length_measure(exp_data, num_data)

    dtw, d = similaritymeasures.dtw(exp_data, num_data)

    mae = compute_mean_absolute_error(exp_data, num_data)
    contour_lenght = find_contour_lenght(num_data)
    nb_pixels_left_right = len(line_left_right)
    rugosity_pixels = compute_rugosity(nb_pixels_left_right, contour_lenght)
    return Similarities(
        pcm=pcm,
        frechet_dist=None,
        area_between_two_curves=None,
        curve_length_measure_arc=curve_length_measure,
        dtw=dtw,
        mae=mae,
        contour_lenght=contour_lenght,
        line_lenght=line_left_right,
        rugosity_pixels=rugosity_pixels,
    )
