import cv2
import matplotlib.pyplot as plt


def load_image(image_path):
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def mark_background(image_path):
    image = load_image(image_path)

    list_points = []

    fig, ax = plt.subplots()
    imgplot = ax.imshow(image)

    def onclick(event):
        ix, iy = event.xdata, event.ydata
        list_points.append([ix, iy])
        ax.plot(ix, iy, marker="v", color="red")

    cid = fig.canvas.mpl_connect("button_press_event", onclick)
    return list_points
