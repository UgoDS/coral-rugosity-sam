import os
from google.colab import output, files


def save_uploaded_file(uploaded_file):
    file_path = os.path.join("images", uploaded_file.name)
    if os.path.exists(file_path):
        pass
    else:
        with open(os.path.join("images", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    return uploaded_file.name


def upload_images():
    uploaded = files.upload()
    list_images = []

    for fn in uploaded.keys():
        print(f'User uploaded file "{fn}" with length {len(uploaded[fn])} bytes')
        os.rename(f"/content/coral-rugosity-sam/{fn}", f"/content/coral-rugosity-sam/images/{fn}")
        list_images.append(f"/content/coral-rugosity-sam/images/{fn}")

    return list_images
