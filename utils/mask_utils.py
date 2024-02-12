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
    edges = cv2.Canny(np.asarray(mask*1, dtype=np.uint8), 0, 0)
    edges[edges != 0.0] = 1
    return np.asarray(edges, dtype=np.uint8)


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
    longest_contour = contours[longest_contour_index]
    return longest_contour


def find_contour_lenght(contour):
    #return cv2.arcLength(contour, True)
    return len(contour)


def get_matrix_from_contour(contour, img):
    contour_image = np.zeros(img.shape[:2])
    verts = contour.reshape(contour.shape[0], contour.shape[2])
    row_indices = verts[:, 1]
    col_indices = verts[:, 0]
    contour_image[row_indices, col_indices] = 1
    return contour_image


def get_thinner_contour(original_matrix):
    matrix = np.zeros(original_matrix.shape)
    indices = np.argmax(original_matrix == 1, axis=0)
    matrix[indices, np.arange(original_matrix.shape[1])] = 1
    return matrix


def from_image_to_contour(contour_image):
    coordinates = np.argwhere(contour_image == 1)
    return np.flip(coordinates).reshape((len(coordinates), 1, 2))

