import os
import shutil
import glob


def save_uploaded_file(uploaded_file):
    file_path = os.path.join("images", uploaded_file.name)
    if os.path.exists(file_path):
        pass
    else:
        with open(os.path.join("images", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    return uploaded_file.name


def create_zip_file(path_folder_to_zip, path_zipped_folder):
    shutil.make_archive(path_zipped_folder, "zip", path_folder_to_zip)


def clean_repo(path):
    files = glob.glob(path)
    for f in files:
        os.remove(f)


def save_df_result(df, path):
    df.to_csv(path, sep=";", index=False)
