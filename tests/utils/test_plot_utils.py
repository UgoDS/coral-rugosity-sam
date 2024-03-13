
import pytest
from utils.plot_utils import get_ellipse_coords

import pytest

from my_module import get_ellipse_coords

def test_get_ellipse_coords():
    # Test case 1: point = (0, 0)
    point = (0, 0)
    expected_coords = (-10, -10, 10, 10)
    assert get_ellipse_coords(point) == expected_coords

    # Test case 2: point = (5, 5)
    point = (5, 5)
    expected_coords = (-5, -5, 15, 15)
    assert get_ellipse_coords(point) == expected_coords

    # Test case 3: point = (-5, -5)
    point = (-5, -5)
    expected_coords = (-15, -15, 5, 5)
    assert get_ellipse_coords(point) == expected_coords

    # Test case 4: point = (100, 100)
    point = (100, 100)
    expected_coords = (90, 90, 110, 110)
    assert get_ellipse_coords(point) == expected_coords

    # Test case 5: point = (-100, -100)
    point = (-100, -100)
    expected_coords = (-
            
import pytest
from utils.plot_utils import plot_masks

To write an effective test for the `plot_masks` function using pytest, we can use the `pytest` library along with the `parametrize` decorator to test different scenarios.

Here's an example of how the test can be written:

```python
import pytest
import matplotlib.pyplot as plt

# Import the function to be tested
from your_module import plot_masks

# Define test cases using parametrize decorator
@pytest.mark.parametrize("image, image_path, mask, score", [
    (image1, "/content/images/image1.jpg", mask1, 0.75),
    (image2, "/content/images/image2.jpg", mask2, 0.85),
    (image3, "/content/images/image3.jpg", mask3, 0.90),
])
def test_plot_masks(image, image_path, mask, score):
    # Call the function to be tested
    plot_masks(image, image_path, mask, score)

    # Assert that the plot is displayed correctly
    assert plt.gcf().get_size_inches() == (10, 10)
    assert plt.gca().get_images()[0].get_array() == image
    assert plt.gca().get_images()[1].get_array() == mask
    assert plt.gca
            import matplotlib.pyplot as plt
import numpy as np
import pytest
from utils.plot_utils import plot_rugosity_results


@pytest.fixture
def sample_data():
    image = np.random.rand(10, 10)
    line_meter = [(1, 2), (3, 4), (5, 6)]
    line_sam = np.array([[(1, 2)], [(3, 4)], [(5, 6)]])
    rugosity_pixels = 10
    mae = 0.5
    return image, line_meter, line_sam, rugosity_pixels, mae


def test_plot_rugosity_results(sample_data):
    image, line_meter, line_sam, rugosity_pixels, mae = sample_data
    plt = plot_rugosity_results(image, line_meter, line_sam, rugosity_pixels, mae)

    assert plt is not None
    assert isinstance(plt, plt.Figure)
import numpy as np
import pytest
from utils.plot_utils import show_mask


def test_show_mask():
    mask = np.array([[1, 0, 1], [0, 1, 0]])
    ax = plt.subplot()

    # Test with random_color=False
    show_mask(mask, ax, random_color=False)
    assert ax.images[0].get_array().shape == (2, 3, 4)
    assert np.allclose(
        ax.images[0].get_array()[0, 0], [206 / 255, 144 / 255, 255 / 255, 0.6]
    )

    # Test with random_color=True
    show_mask(mask, ax, random_color=True)
    assert ax.images[1].get_array().shape == (2, 3, 4)
    assert np.allclose(ax.images[1].get_array()[0, 0], [0.6, 0.6, 0.6, 0.6])
