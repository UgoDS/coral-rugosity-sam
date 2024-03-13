import cv2
import pytest
from utils.image_utils import load_image


@pytest.fixture
def image_path():
    return "path/to/image.jpg"


def test_load_image(image_path):
    image = load_image(image_path)
    assert isinstance(image, np.ndarray)
    assert image.shape[2] == 3
    assert image.dtype == np.uint8
    assert np.array_equal(
        image, cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    )


import matplotlib.pyplot as plt
import pytest
from utils.image_utils import mark_background


@pytest.fixture
def image_path():
    return "path/to/image.jpg"


def test_mark_background(image_path):
    points = mark_background(image_path)
    assert isinstance(points, list)
    assert len(points) == 0

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3], [4, 5, 6])
    fig.canvas.draw()

    event = (
        plt.figure().canvas.manager.toolbar._views[0].toolbar.mode_actions[""].triggered
    )
    event.emit(
        plt.figure().canvas.manager.toolbar._views[0].toolbar.mode_actions[""].data
    )

    points = mark_background(image_path)
    assert isinstance(points, list)
    assert len(points) == 1
    assert isinstance(points[0], list)
    assert len(points[0]) == 2
    assert isinstance(points[0][0], float)
    assert isinstance(points[0][1], float)
