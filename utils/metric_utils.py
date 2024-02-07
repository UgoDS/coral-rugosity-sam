import numpy as np

from utils.mask_utils import (find_contour_lenght, find_lowest_left_pixel,
                              find_lowest_right_pixel, get_max_contour_x,
                              get_min_contour_x)


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
        for y_sam in np.where(line_sam[:, 0][:, 0] == x_meter)[0]:
            sum += abs(line_sam[:, 0][y_sam, 1] - y_meter)
    error = sum / n
    print(f"Mean absolute error : {error:.2f}")
    return error


def compute_rugosity(mask, contour):
    contour_lenght = find_contour_lenght(contour)
    line_left_right = get_line_from_left_to_right(mask, contour)
    nb_pixels_left_right = len(line_left_right)
    rugosity_pixels = round(contour_lenght / nb_pixels_left_right, 3)
    return rugosity_pixels
