import cv2
import numpy as np


def get_min_contour_x(contour):
    return min(contour[:, 0][:, 0])


def get_max_contour_x(contour):
    return max(contour[:, 0][:, 0])


def find_lowest_left_pixel(mask, contour):
    start_contour_pixel = get_min_contour_x(contour)
    return np.where(mask[:, start_contour_pixel + 1])[0][-1:][0]


def find_lowest_right_pixel(mask, contour):
    end_contour_pixel = get_max_contour_x(contour)
    return np.where(mask[:, end_contour_pixel - 1])[0][-1:][0]


def find_edges(mask):
    """
    Mathematical method to find the edge using np.gradient"""
    gx, gy = np.gradient(mask * 1)
    edges = gy * gy + gx * gx
    edges[edges != 0.0] = 1
    edges = np.asarray(edges, dtype=np.uint8)
    return edges


def find_contours(edges):
    contours, hierarchy = cv2.findContours(
        edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    return contours


def find_longest_contour_index(contours):
    """Find the longest contour with maximum perimeter"""
    perimeter = []
    for cnt in contours:
        perimeter.append(find_contour_lenght(cnt))
    max_index = perimeter.index(max(perimeter))
    return max_index


def find_contour_from_mask(mask):
    edges = find_edges(mask)
    contours = find_contours(edges)
    longest_contour_index = find_longest_contour_index(contours)
    return contours[longest_contour_index]


def find_contour_lenght(contour):
    return cv2.arcLength(contour, True)
