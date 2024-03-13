import glob
import os

import pytest
from utils.io_utils import clean_repo


def clean_repo(path):
    files = glob.glob(path)
    for f in files:
        os.remove(f)


@pytest.fixture
def create_files():
    # Create some test files
    files = ["file1.txt", "file2.txt", "file3.txt"]
    for file in files:
        open(file, "w").close()
    yield
    # Clean up the test files
    for file in files:
        os.remove(file)


def test_clean_repo(create_files):
    # Define the path to the test files
    path = "*.txt"

    # Call the clean_repo function
    clean_repo(path)

    # Check if the files have been removed
    assert not glob.glob(path)


import os
import shutil

import pytest
from utils.io_utils import create_zip_file


def create_zip_file(path_folder_to_zip, path_zipped_folder):
    shutil.make_archive(path_zipped_folder, "zip", path_folder_to_zip)


@pytest.fixture
def test_files():
    # Create a temporary folder for testing
    test_folder = "test_folder"
    os.mkdir(test_folder)

    # Create some test files in the folder
    file1 = os.path.join(test_folder, "file1.txt")
    file2 = os.path.join(test_folder, "file2.txt")
    file3 = os.path.join(test_folder, "file3.txt")
    with open(file1, "w") as f:
        f.write("This is file 1")
    with open(file2, "w") as f:
        f.write("This is file 2")
    with open(file3, "w") as f:
        f.write("This is file 3")

    yield test_folder

    # Clean up the temporary folder after testing
    shutil.rmtree(test_folder)


def test_create_zip_file(test_files):
    # Define the paths for the test
    path_folder_to_zip = test_files
    path_zipped_folder = "test_zip"

    # Call the function to create the


import os

import pandas as pd
import pytest
from utils.io_utils import save_df_result


@pytest.fixture
def test_data():
    data = {
        "Name": ["John", "Alice", "Bob"],
        "Age": [25, 30, 35],
        "City": ["New York", "London", "Paris"],
    }
    return pd.DataFrame(data)


def test_save_df_result(test_data):
    path = "test.csv"
    save_df_result(test_data, path)
    assert os.path.exists(path)
    df = pd.read_csv(path, sep=";")
    assert df.equals(test_data)
    os.remove(path)


import os

import pytest
from utils.io_utils import save_uploaded_file


def save_uploaded_file(uploaded_file):
    file_path = os.path.join("images", uploaded_file.name)
    if os.path.exists(file_path):
        pass
    else:
        with open(os.path.join("images", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    return uploaded_file.name


def test_save_uploaded_file(tmpdir):
    uploaded_file = MockUploadedFile("test.jpg")
    save_uploaded_file(uploaded_file)

    file_path = os.path.join("images", uploaded_file.name)
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)
    assert os.path.basename(file_path) == "test.jpg"
    assert os.path.dirname(file_path) == "images"
    assert os.path.getsize(file_path) == len(uploaded_file.getbuffer())


class MockUploadedFile:
    def __init__(self, name):
        self.name = name
        self.buffer = b"test content"

    def getbuffer(self):
        return self.buffer


# Run the test
pytest.main()

import pytest
from utils.io_utils import upload_images

To write an effective pytest for the `upload_images` function, we need to mock the `files.upload()` function and verify that the correct file paths are added to the `list_images` list.

Here's an example of how the pytest can be written:

```python
import os
from unittest import mock
import pytest

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

def test_upload_images(monkeypatch):
    # Mock the files.upload() function
    mock_files_upload = mock.Mock(return_value={"image1.jpg", "image2.jpg"})
    monkeypatch.setattr(files, "upload", mock_files_upload)

    # Call the upload_images function
    result = upload_images()

    # Verify the list_images contains the correct file paths
    assert result == [
        "/content/coral-rugosity-sam/images/image1.jpg",
        "/content/coral-rugosity-sam/images/image2.jpg
            