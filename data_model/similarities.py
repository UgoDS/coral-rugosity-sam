from dataclasses import dataclass


@dataclass
class Similarities:
    pcm: float = None
    frechet_dist: float = None
    area_between_two_curves: float = None
    curve_length_measure_pixel: float = None
    curve_length_measure_arc: float = None
    dtw: float = None
    mae: float = None
    mse: float = None
    contour_lenght: float = None
    line_lenght: float = None
    rugosity_pixels: float = None
