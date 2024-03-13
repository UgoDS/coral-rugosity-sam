import pytest
from utils.sam_utils import find_best_background_mask


@pytest.fixture
def predictor():
    # Create a mock predictor object for testing
    class MockPredictor:
        def set_image(self, image):
            pass

        def predict(self, point_coords, point_labels, multimask_output):
            masks = [True, False, False]
            scores = [0.9, 0.5, 0.3]
            logits = [0.1, 0.2, 0.3]
            return masks, scores, logits

    return MockPredictor()


def test_find_best_background_mask(predictor):
    image = "test_image.jpg"
    list_points = [(10, 10), (20, 20), (30, 30)]

    mask, score = find_best_background_mask(predictor, image, list_points)

    assert mask == True
    assert score == 0.9


import numpy as np
import pytest
from utils.sam_utils import get_sam_inputs


def test_get_sam_inputs():
    # Test case 1: list_points is empty
    list_points = []
    expected_input_point = np.array([])
    expected_input_label = np.array([])
    input_point, input_label = get_sam_inputs(list_points)
    assert np.array_equal(input_point, expected_input_point)
    assert np.array_equal(input_label, expected_input_label)

    # Test case 2: list_points has one element
    list_points = [[1, 2, 3]]
    expected_input_point = np.array([[1, 2, 3]])
    expected_input_label = np.array([1])
    input_point, input_label = get_sam_inputs(list_points)
    assert np.array_equal(input_point, expected_input_point)
    assert np.array_equal(input_label, expected_input_label)

    # Test case 3: list_points has multiple elements
    list_points = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected_input_point = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    expected


import pytest
from utils.sam_utils import load_predictor


def test_load_predictor():
    model_type = "model_type"
    sam_checkpoint = "sam_checkpoint"

    # Mock the sam_model_registry dictionary
    sam_model_registry = {"model_type": MockSamModel}

    # Mock the SamPredictor class
    class MockSamPredictor:
        def __init__(self, sam):
            self.sam = sam

    # Mock the SamModel class
    class MockSamModel:
        def __init__(self, checkpoint):
            self.checkpoint = checkpoint

        def to(self, device):
            pass

    # Mock the DEVICE constant
    DEVICE = "device"

    # Call the load_predictor function
    predictor = load_predictor(model_type, sam_checkpoint)

    # Assert that the sam_model_registry is called with the correct arguments
    assert sam_model_registry[model_type].called_with(checkpoint=sam_checkpoint)

    # Assert that the SamModel is called with the correct arguments
    assert MockSamModel.called_with(checkpoint=sam_checkpoint)

    # Assert that the SamModel is called with the correct device
    assert MockSamModel.to.called_with(device=DEVICE)

    # Assert that the SamPredictor is
