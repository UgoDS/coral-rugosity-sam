import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np


def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )


def plot_rugosity_results(image, line_meter, line_sam, rugosity_pixels, mae):
    fig_final = plt.figure(constrained_layout=True)
    gs = gridspec.GridSpec(2, 1, figure=fig_final)
    gs.update(wspace=0.5)
    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(
        gs[1, 0],
    )

    # just plot things on each individual axes
    ax1.imshow(image, cmap="gray")
    ax1.set_title("Original Image")

    ax2.imshow(image)
    ax2.plot(
        [x[0] for x in line_sam[:, 0]], [x[1] for x in line_sam[:, 0]], color="yellow"
    )
    ax2.plot(
        [line[0] for line in line_meter], [line[1] for line in line_meter], color="red"
    )
    ax2.set_title(f"Pixel Method: {rugosity_pixels:.2f}, MAE Method: {mae:.2f}")

    return plt


def plot_masks(image, image_path, mask, score):
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    show_mask(mask, plt.gca())
    plt.title(
        f"{image_path.replace('/content/images/', '')} - Score: {score:.2f}",
        fontsize=18,
    )
    plt.show()


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([206 / 255, 144 / 255, 255 / 255, 0.6])  # purple
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
