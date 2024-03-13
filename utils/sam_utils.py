import numpy as np
import torch
from segment_anything import SamPredictor, sam_model_registry

# SAM Parameters
SAM_CHECKPOINT = "sam_vit_b_01ec64.pth"
MODEL_TYPE = "vit_b"
DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda"
    MODEL_TYPE = "vit_h"
    SAM_CHECKPOINT = "sam_vit_h_4b8939.pth"


def find_best_background_mask(
    predictor, image, list_points_background, list_points_fish
):
    predictor.set_image(image)

    input_point, input_label = get_sam_inputs(list_points_background, list_points_fish)

    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=False,
    )
    return masks[0], scores[0]


def get_sam_inputs(list_points_background, list_points_fish):
    input_point = np.array(list_points_background + list_points_fish)
    input_label = np.array(
        [1 for x in range(len(list_points_background))]
        + [2 + x for x in range(len(list_points_fish))] # Each fish is different
    )
    return input_point, input_label


def load_predictor(model_type=MODEL_TYPE, sam_checkpoint=SAM_CHECKPOINT):
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=DEVICE)
    return SamPredictor(sam)
