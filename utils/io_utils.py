import os
import shutil
import glob
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
        os.rename(
            f"/content/coral-rugosity-sam/{fn}",
            f"/content/coral-rugosity-sam/images/{fn}",
        )
        list_images.append(f"/content/coral-rugosity-sam/images/{fn}")

    return list_images


def create_zip_file(path_folder_to_zip, path_zipped_folder):
    shutil.make_archive(path_zipped_folder, "zip", path_folder_to_zip)


def clean_repo(path):
    files = glob.glob(path)
    for f in files:
        os.remove(f)


def save_df_result(df, path):
    df.to_csv(path, sep=";", index=False)
